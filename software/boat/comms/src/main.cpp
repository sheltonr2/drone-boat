// Companion comms firmware (Rev F): Adafruit Feather ESP32-S3 in the main box.
//
// This is the satellite and camera half of the companion's job. The session logic itself is in
// lib/comms_core (tested on a PC); this file connects it to the hardware:
//   - the RockBLOCK Plus 9704 on RS-232 through a MAX3232, powered through its own load switch (fuse F6, D30),
//     driven with Ground Control's RockBLOCK-9704 library (JSPR);
//   - the camera (XIAO ESP32S3 Sense) on UART1 behind the fifth load switch, spoken to with lib/camlink;
//   - settings and the command key in flash (Preferences).
// The mission manager (route, wind, autopilot over MAVLink) is not written yet: mission.h is its interface, and
// mission_stub.cpp stands in for it on the bench.
//
// Bench console on USB (115200): "key <64 hex digits>" stores the command key; "now" runs a session at once;
// "status" prints the settings. The key never appears in this repository or in the console's replies.
//
// Written 28 Nov 2026, not yet built or run on hardware. Pins are placeholders until the wiring sheet (D30) gives them.
#include <Arduino.h>
#include <Preferences.h>
#include <esp_sleep.h>
#include <sys/time.h>
#include "rockblock_9704.h"
#include "camlink.h"
#include "comms_core.h"
#include "mission.h"

// ---- pins (placeholders; take them from D30 when the box is wired)
static const int PIN_MODEM_EN = 5;     // load switch for the RockBLOCK Plus 9704 (12 V)
static const int PIN_CAM_EN = 6;       // load switch for the camera (5 V)
static const int PIN_CAM_RX = 15, PIN_CAM_TX = 16;     // UART1 to the camera (its D6 TX -> our RX, its D7 RX <- our TX)
static const int PIN_MODEM_RX = 38, PIN_MODEM_TX = 39; // UART2 to the MAX3232
static const uint32_t MODEM_BAUD = 230400;             // the library's examples use 230400
static const uint32_t CAM_BAUD = 921600;
static const uint8_t BOAT_ID = 1;

static Preferences prefs;
static comms::Settings settings;
static uint8_t key[32]; static bool have_key = false;
static uint8_t* mo_buf; static uint8_t* photo_buf;
static const size_t MO_CAP = IMT_PAYLOAD_SIZE, PHOTO_CAP = 120000;

// ---------------------------------------------------------------- settings in flash
static void load_settings() {
  prefs.begin("comms", false);
  if (prefs.getBytesLength("settings") == sizeof settings) prefs.getBytes("settings", &settings, sizeof settings);
  have_key = prefs.getBytes("key", key, sizeof key) == sizeof key;
}

// ---------------------------------------------------------------- the hardware behind comms::Hal
struct BoatHal : comms::Hal {
  bool fill_report(dronemsg::Report& r) override { return mission_fill_report(r); }
  bool point_at_sea(int32_t lat, int32_t lon) override { return mission_point_at_sea(lat, lon); }
  void apply(const dronemsg::Command& c) override { mission_apply(c); }
  bool thruster_fitted() override { return false; }  // no thruster since Rev C

  size_t camera(const comms::CameraRequest& q, uint8_t* out, size_t cap, uint16_t* number, char* err, size_t ec) override {
    using namespace camlink;
    digitalWrite(PIN_CAM_EN, HIGH);
    Serial1.begin(CAM_BAUD, SERIAL_8N1, PIN_CAM_RX, PIN_CAM_TX);
    Parser p(out, cap < MAX_PAYLOAD ? cap : MAX_PAYLOAD);
    size_t got = 0; bool asked = false; uint32_t t0 = millis(), limit = 20000;
    while (millis() - t0 < limit) {
      while (Serial1.available()) {
        if (!p.push(Serial1.read())) continue;
        if (p.type() == HELLO && !asked) {
          uint8_t req[7], f[32]; size_t n;
          if (q.type == comms::CAM_CLIP) { req[0] = q.seconds; put32(req + 1, q.max_bytes); n = frame(f, sizeof f, CLIP, req, 5); limit = 20000 + 1000u * q.seconds; }
          else { req[0] = q.kind; put16(req + 1, q.stored); put32(req + 3, q.max_bytes); n = frame(f, sizeof f, PHOTO, req, 7); }
          Serial1.write(f, n); asked = true; t0 = millis();
        } else if (p.type() == RESULT && p.length() >= 3) {
          *number = get16(p.payload()); got = p.length() - 3;
          memmove(out, out + 3, got);  // the parser wrote into out: drop the 3-byte header
          uint8_t f[16]; Serial1.write(f, frame(f, sizeof f, DONE, nullptr, 0)); Serial1.flush();
          goto done;
        } else if (p.type() == ERROR) {
          snprintf(err, ec, "camera error %u: %.*s", p.payload()[0], (int)(p.length() - 1), (const char*)p.payload() + 1);
          goto done;
        }
      }
      delay(2);
    }
    snprintf(err, ec, asked ? "no result in time" : "no HELLO (power or wiring?)");
  done:
    delay(50);
    Serial1.end(); digitalWrite(PIN_CAM_EN, LOW);
    return got;
  }

  bool modem_on = false;
  bool modem_up() {
    modem_on = true;
    digitalWrite(PIN_MODEM_EN, HIGH); delay(1500);  // up to 6.7 W for about 30 s at start-up: F6 is a slow-blow
    Serial2.begin(MODEM_BAUD, SERIAL_8N1, PIN_MODEM_RX, PIN_MODEM_TX);
    // How rbBegin() names the port on Arduino: check ArduinoBasicSendandReceive.ino in the library before the bench test.
    return rbBegin("Serial2");
  }
  void modem_down() {
    if (!modem_on) return;
    rbEnd(); Serial2.end(); digitalWrite(PIN_MODEM_EN, LOW); modem_on = false;
  }

  bool modem_send(const uint8_t* m, size_t n) override {
    if (!modem_up()) { modem_down(); return false; }
    bool ok = rbSendMessage((const char*)m, n, 600);  // up to 10 minutes for a clear sky
    if (!ok) modem_down();
    return ok;  // left on for modem_receive()
  }
  size_t modem_receive(uint8_t* out, size_t cap) override {
    // listen for up to 60 s after a send; the gateway pushes queued command messages within seconds
    uint32_t t0 = millis();
    while (millis() - t0 < 60000) {
      char* buf = nullptr;
      size_t n = rbReceiveMessage(&buf);
      if (n && buf) {
        if (n > cap) n = 0; else memcpy(out, buf, n);  // the library reuses its buffer: copy now
        return n;
      }
      delay(10);
    }
    modem_down();
    return 0;
  }
  void save(const comms::Settings& s) override { prefs.putBytes("settings", &s, sizeof s); }
  void reboot_companion() override { modem_down(); delay(200); ESP.restart(); }
  void diag(char* out, size_t cap) override {
    snprintf(out, cap, "fw=comms-1;heap=%u;psram=%u;up=%lu;sig=%d;", (unsigned)ESP.getFreeHeap(), (unsigned)ESP.getFreePsram(),
             (unsigned long)(millis() / 1000), (int)rbGetSignal());
  }
  void log(const char* line) override { Serial.printf("[comms] %s\n", line); mission_log(line); }
} hal;

static comms::Comms* sat;

// ---------------------------------------------------------------- bench console
static void console() {
  static char line[96]; static size_t n = 0;
  while (Serial.available()) {
    char c = Serial.read();
    if (c != '\n' && c != '\r') { if (n < sizeof line - 1) line[n++] = c; continue; }
    line[n] = 0; n = 0;
    if (!strncmp(line, "key ", 4) && strlen(line) == 4 + 64) {
      for (int i = 0; i < 32; i++) { char h[3] = {line[4 + 2 * i], line[5 + 2 * i], 0}; key[i] = strtoul(h, nullptr, 16); }
      prefs.putBytes("key", key, sizeof key); have_key = true;
      memset(line, 0, sizeof line);
      Serial.println("key stored");
    } else if (!strncmp(line, "time ", 5)) {
      struct timeval tv = {(time_t)strtoul(line + 5, nullptr, 10), 0}; settimeofday(&tv, nullptr);
      Serial.println("clock set");
    } else if (!strcmp(line, "now")) {
      sat->session((uint32_t)time(nullptr)); hal.modem_down();
    } else if (!strcmp(line, "status")) {
      Serial.printf("key %s; last seq %lu; session %u; reports every %u min; photos %u a day from %02u UTC, %u bytes\n",
                    have_key ? "set" : "NOT SET", (unsigned long)settings.last_seq, settings.session, settings.report_min,
                    settings.photos_per_day, settings.photo_hour_utc, settings.photo_max);
    }
  }
}

void setup() {
  Serial.begin(115200);
  pinMode(PIN_MODEM_EN, OUTPUT); digitalWrite(PIN_MODEM_EN, LOW);
  pinMode(PIN_CAM_EN, OUTPUT); digitalWrite(PIN_CAM_EN, LOW);
  load_settings();
  mo_buf = (uint8_t*)ps_malloc(MO_CAP); photo_buf = (uint8_t*)ps_malloc(PHOTO_CAP);
  if (!mo_buf || !photo_buf) Serial.println("PSRAM allocation failed: use the Feather ESP32-S3 with PSRAM");
  sat = new comms::Comms(hal, settings, key, sizeof key, BOAT_ID, mo_buf, MO_CAP, photo_buf, PHOTO_CAP);
  mission_begin();
  if (!have_key) Serial.println("No command key: type  key <64 hex digits>  (from software/shore/make_key.py)");
}

void loop() {
  console();
  mission_loop();  // the mission manager's own work between sessions
  uint32_t now = (uint32_t)time(nullptr);  // the mission manager sets the clock from GPS
  if (have_key && mission_clock_ok() && sat->seconds_to_next(now) == 0) {
    sat->session(now);
    hal.modem_down();  // whatever happened in the session, the modem is off afterwards
  }
  delay(50);
}
