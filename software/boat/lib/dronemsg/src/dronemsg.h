// Boat side of the boat <-> shore protocol, version 1 (software/protocol/PROTOCOL.md).
// Portable C++ (no Arduino or ESP-IDF headers), so the same code is tested on a PC against the Python codec's vectors
// (test/test_host.cpp) and built into the companion firmware. No heap use.
#pragma once
#include <stddef.h>
#include <stdint.h>

namespace dronemsg {

constexpr uint8_t MO_MAGIC = 0xD1, MT_MAGIC = 0xD2;
constexpr size_t REPORT_LEN = 43, TAG_LEN = 16, MO_OVERHEAD = 4 + REPORT_LEN + 4;

struct Report {  // field order and units as PROTOCOL.md
  uint32_t time; int32_t lat, lon;              // Unix s; 1e-7 deg
  uint16_t sog_cms, cog_cdeg, heading_cdeg;
  int16_t awa_ddeg; uint16_t aws_cms, batt_mv;
  uint8_t soc; uint16_t solar_dw;
  int8_t wing_deg, rudder_deg; uint8_t humidity; int8_t temp_c;
  uint8_t leak, mode, wp_index, pump_runs;
  uint32_t last_cmd_seq, faults;
};

enum Mode : uint8_t { SAIL = 0, SAIL_THRUST = 1, STATION = 2, DRIFT = 3, SAFE = 4, LIMP_HOME = 5 };
enum Fault : uint32_t {
  F_MAIN_GPS = 1u << 0, F_COMPASS = 1u << 1, F_WIND_VANE = 1u << 2, F_AUTOPILOT_LINK = 1u << 3, F_RUDDER_PORT = 1u << 4,
  F_RUDDER_STBD = 1u << 5, F_TAIL_SERVO = 1u << 6, F_PUMP = 1u << 7, F_CAMERA = 1u << 8, F_SD_CARD = 1u << 9,
  F_MODEM_RETRY = 1u << 10, F_LOW_BATTERY = 1u << 11, F_LIMP_HOME = 1u << 12, F_WATCHDOG_RESET = 1u << 13,
  F_COMMAND_REJECTED = 1u << 14, F_HUMIDITY_HIGH = 1u << 15
};
enum Section : uint8_t { SEC_ACK = 1, SEC_PHOTO = 2, SEC_DIAG = 3, SEC_LOG = 4 };
enum AckResult : uint8_t { APPLIED = 0, BAD_SIGNATURE = 1, OLD_SEQUENCE = 2, BAD_VALUE = 3, UNKNOWN_COMMAND = 4, WRONG_BOAT = 5 };
enum Op : uint8_t {
  SET_ROUTE = 1, GOTO = 2, MODE = 3, SET_REPORT = 4, HOLD = 5, GEOFENCE = 6, DIAG = 7, REBOOT = 8, PHOTO = 9, CLIP = 10, SET_PHOTO = 11
};

uint32_t crc32(const uint8_t* p, size_t n, uint32_t crc = 0);
void hmac_sha256(const uint8_t* key, size_t key_len, const uint8_t* msg, size_t n, uint8_t out[32]);

void encode_report(const Report& r, uint8_t out[REPORT_LEN]);
bool decode_report(const uint8_t in[REPORT_LEN], Report& r);

// Builds one MO message in a caller's buffer. Every add_ returns false (and adds nothing) if it would not fit.
class MoBuilder {
 public:
  MoBuilder(uint8_t* buf, size_t cap) : b_(buf), cap_(cap) {}
  bool begin(uint8_t boat_id, uint16_t session, const Report& r);
  bool add_ack(uint32_t seq, AckResult result, uint8_t index = 0xFF);
  bool add_photo(uint16_t photo_id, uint8_t part, uint8_t parts, uint32_t total, const uint8_t* data, size_t n);
  bool add_text(Section kind, const char* text);
  size_t finish();            // appends the CRC; returns the message length (0 if it does not fit)
  size_t room() const;        // bytes left for section payloads, after the CRC and one section header
 private:
  bool header(uint8_t kind, size_t n);
  uint8_t* b_; size_t cap_, n_ = 0;
};

// ---- MT: verify, then walk the commands
struct Point { int32_t lat, lon; };
struct Command {
  Op op;
  union {
    struct { uint8_t n; Point pts[50]; } route;                 // SET_ROUTE
    Point go;                                                   // GOTO
    uint8_t mode;                                               // MODE
    uint16_t minutes;                                           // SET_REPORT
    struct { Point p; uint16_t radius_m; } hold;                // HOLD
    struct { uint8_t action, n; Point pts[20]; } fence;         // GEOFENCE
    uint8_t target;                                             // REBOOT
    struct { uint8_t kind; uint16_t stored; uint32_t max_bytes; } photo;   // PHOTO
    struct { uint8_t seconds; uint32_t max_bytes; } clip;                  // CLIP
    struct { uint8_t per_day, hour_utc; uint16_t max_bytes; } set_photo;   // SET_PHOTO
  } a;
};

// Called for every point in a command before anything is applied: return false if the point is on land or
// otherwise unacceptable (the coastline mask lives in the mission manager). May be null.
typedef bool (*PointCheck)(int32_t lat, int32_t lon, void* ctx);

struct MtResult {
  AckResult result; uint8_t bad_index;   // bad_index: the failing command, or 0xFF
  uint32_t seq, issued_at; uint8_t count; // count: commands parsed (all checked) when result == APPLIED
};

// Checks the signature, boat id, sequence and every command's values. Applies nothing: on APPLIED, call
// mt_command() for i < count to get each command, then apply them all.
MtResult mt_verify(const uint8_t* key, size_t key_len, const uint8_t* msg, size_t n, uint8_t boat_id, uint32_t last_seq,
                   PointCheck check = nullptr, void* ctx = nullptr, bool thruster_fitted = false);
bool mt_command(const uint8_t* msg, size_t n, uint8_t index, Command& out);

}  // namespace dronemsg
