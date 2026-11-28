// The companion's satellite session logic, portable (no Arduino headers) so it is tested on a PC with a fake
// boat (test/test_comms.cpp). The firmware (software/boat/comms) supplies the hardware through Hal.
//
// One session: fill the report, take the daily photo if one is due (or one the shore asked for), build one MO message
// (report, the acknowledgement of the last command message, the photo or the next part of a big one, diagnostics),
// send it, then listen for command messages, verify them, and apply them. Commands about the comms and the camera are
// handled here; route, mode, hold and the rest go to the mission manager through Hal::apply().
#pragma once
#include <stddef.h>
#include <stdint.h>
#include "dronemsg.h"

namespace comms {

using dronemsg::Command;
using dronemsg::Report;

struct Settings {             // kept in flash by the firmware (Hal::save) after every change
  uint32_t last_seq = 0;      // last command sequence applied
  uint16_t session = 0;       // MO counter
  uint16_t report_min = 240;  // SET_REPORT
  uint8_t photos_per_day = 1, photo_hour_utc = 16;  // SET_PHOTO; 16 UTC is about noon in the Caribbean, 4 pm in Cornwall
  uint16_t photo_max = 10000;
  uint32_t last_photo_slot = 0;  // index of the last daily-photo slot taken (time / slot length)
};

constexpr size_t MO_MAX = 100000;   // IMT message limit
constexpr size_t PART_MAX = 60000;  // largest photo part. The firmware's message buffer must match the RockBLOCK library's
                                    // IMT_PAYLOAD_SIZE (5,000 bytes by default on Arduino; set 12,000 for a 10 KB photo)
constexpr uint8_t CAM_PHOTO = 0x10, CAM_CLIP = 0x11;  // the camlink request types (camlink.h)
struct CameraRequest { uint8_t type = 0;  // CAM_PHOTO or CAM_CLIP
  uint8_t kind = 0; uint16_t stored = 0; uint32_t max_bytes = 0; uint8_t seconds = 0; };

struct Hal {
  virtual ~Hal() {}
  virtual bool fill_report(Report& r) = 0;                       // mission manager: position, wind, power, mode...
  virtual bool point_at_sea(int32_t lat, int32_t lon) = 0;       // mission manager's coastline mask
  virtual void apply(const Command& c) = 0;                      // SET_ROUTE, GOTO, MODE, HOLD, GEOFENCE, REBOOT autopilot
  virtual bool thruster_fitted() { return false; }
  // Power the camera, make the request, return the JPEG/MJPEG length in out (0 on failure, with err filled).
  virtual size_t camera(const CameraRequest& req, uint8_t* out, size_t cap, uint16_t* number, char* err, size_t errcap) = 0;
  virtual bool modem_send(const uint8_t* p, size_t n) = 0;       // true once the gateway has taken it
  virtual size_t modem_receive(uint8_t* out, size_t cap) = 0;    // one waiting MT message, or 0 when none come
  virtual void save(const Settings& s) = 0;
  virtual void reboot_companion() {}
  virtual void diag(char* out, size_t cap) { if (cap) out[0] = 0; }  // key=value;... for a DIAG request
  virtual void log(const char* line) { (void)line; }
};

class Comms {
 public:
  Comms(Hal& hal, Settings& s, const uint8_t* key, size_t key_len, uint8_t boat_id,
        uint8_t* mo_buf, size_t mo_cap, uint8_t* photo_buf, size_t photo_cap);

  // Seconds until the next scheduled session, from `now` (Unix s). The firmware sleeps that long.
  uint32_t seconds_to_next(uint32_t now) const;
  // Run one session. Returns true if the MO was sent. If a command asks for a photo, clip or diagnostics,
  // a second session follows at once (so the shore does not wait four hours for it).
  bool session(uint32_t now);

  uint32_t faults() const { return faults_; }
  uint32_t last_session() const { return last_session_; }

 private:
  bool one(uint32_t now);
  void handle_mt(const uint8_t* m, size_t n);
  bool photo_due(uint32_t now) const;
  uint32_t slot_seconds() const { return s_.photos_per_day ? 86400u / s_.photos_per_day : 86400u; }
  // photo bytes per message: what is left of the message buffer (the modem library's payload size) after the
  // report, an ACK, diagnostics and the section headers, and never more than PART_MAX
  size_t part_max() const { size_t lim = mo_cap_ < MO_MAX ? mo_cap_ : MO_MAX; return lim < 800 ? 0 : (lim - 500 < PART_MAX ? lim - 500 : PART_MAX); }

  Hal& hal_; Settings& s_; const uint8_t* key_; size_t key_len_; uint8_t boat_;
  uint8_t* mo_; size_t mo_cap_; uint8_t* ph_; size_t ph_cap_;
  // pending state carried to the next session
  bool ack_pending_ = false; uint32_t ack_seq_ = 0; uint8_t ack_res_ = 0, ack_idx_ = 0xFF;
  CameraRequest req_; bool req_pending_ = false, diag_pending_ = false, again_ = false, reboot_after_ = false;
  size_t ph_len_ = 0, ph_sent_ = 0; uint16_t ph_id_ = 0; uint8_t ph_part_ = 0, ph_parts_ = 0;  // photo being sent in parts
  uint32_t faults_ = 0, last_session_ = 0;
};


}  // namespace comms
