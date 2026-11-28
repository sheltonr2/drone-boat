// Host test of the session logic with a fake boat, fake camera and fake modem.
//   g++ -std=c++17 -Wall -Wextra -I../src -I../../dronemsg/src -I../../dronemsg/test ../src/comms_core.cpp ../../dronemsg/src/dronemsg.cpp test_comms.cpp -o t && ./t
#include <stdio.h>
#include <string.h>
#include <vector>
#include "comms_core.h"
#include "vectors.h"
using namespace comms;
using namespace dronemsg;

static int fails = 0;
#define CHECK(c) do { if (!(c)) { printf("FAIL %s:%d  %s\n", __FILE__, __LINE__, #c); fails++; } } while (0)

struct Fake : Hal {
  std::vector<std::vector<uint8_t>> sent, inbox; std::vector<uint8_t> applied;
  size_t photo_size = 5000; bool send_ok = true, camera_ok = true; int camera_calls = 0, saves = 0, reboots = 0;
  bool fill_report(Report& r) override { r.time = 1840000000; r.lat = 181000000; r.lon = -644000000; r.mode = STATION; return true; }
  bool point_at_sea(int32_t, int32_t) override { return true; }
  void apply(const Command& c) override { applied.push_back(c.op); }
  size_t camera(const CameraRequest& q, uint8_t* out, size_t cap, uint16_t* no, char* err, size_t ec) override {
    camera_calls++;
    if (!camera_ok) { snprintf(err, ec, "no HELLO"); return 0; }
    size_t n = photo_size < cap ? photo_size : cap;
    for (size_t i = 0; i < n; i++) out[i] = (uint8_t)(i + q.kind);
    *no = 42; return n;
  }
  bool modem_send(const uint8_t* p, size_t n) override { if (!send_ok) return false; sent.emplace_back(p, p + n); return true; }
  size_t modem_receive(uint8_t* out, size_t cap) override {
    if (inbox.empty()) return 0;
    auto m = inbox.front(); inbox.erase(inbox.begin());
    if (m.size() > cap) return 0;
    memcpy(out, m.data(), m.size()); return m.size();
  }
  void save(const Settings&) override { saves++; }
  void reboot_companion() override { reboots++; }
};

struct Sec { uint8_t type; std::vector<uint8_t> p; };
static std::vector<Sec> sections(const std::vector<uint8_t>& m, Report* r = nullptr) {
  std::vector<Sec> out;
  if (m.size() < MO_OVERHEAD || crc32(m.data(), m.size() - 4) != (uint32_t)(m[m.size() - 4] | m[m.size() - 3] << 8 | m[m.size() - 2] << 16 | (uint32_t)m[m.size() - 1] << 24)) {
    printf("bad MO\n"); fails++; return out;
  }
  if (r) decode_report(m.data() + 4, *r);
  for (size_t i = 4 + REPORT_LEN; i + 4 < m.size();) {
    uint16_t n = m[i + 1] | m[i + 2] << 8;
    out.push_back(Sec{m[i], std::vector<uint8_t>(m.begin() + i + 3, m.begin() + i + 3 + n)}); i += 3 + n;
  }
  return out;
}

int main() {
  static uint8_t mo[MO_MAX], ph[200000];
  const uint32_t day = 21296, now = day * 86400u + 16 * 3600 + 600;  // 10 minutes after the 16:00 UTC photo slot

  {  // daily photo, then a command message asking for another photo: answered in an immediate second session
    Fake f; Settings s; Comms c(f, s, VEC_KEY, 32, 1, mo, sizeof mo, ph, sizeof ph);
    f.inbox.emplace_back(VEC_MT, VEC_MT + sizeof VEC_MT);
    CHECK(c.session(now));
    CHECK(f.sent.size() == 2 && f.camera_calls == 2);
    auto s1 = sections(f.sent[0]);
    CHECK(s1.size() == 1 && s1[0].type == SEC_PHOTO && s1[0].p.size() == 8 + 5000);
    Report r2; auto s2 = sections(f.sent[1], &r2);
    CHECK(s2.size() == 2 && s2[0].type == SEC_ACK && s2[0].p[0] == 8 && s2[0].p[4] == APPLIED && s2[1].type == SEC_PHOTO);
    CHECK(r2.last_cmd_seq == 8);
    CHECK(f.applied.size() == 3 && f.applied[0] == HOLD && f.applied[1] == SET_ROUTE && f.applied[2] == MODE);
    CHECK(s.last_seq == 8 && s.report_min == 240 && s.session == 2 && s.last_photo_slot == day);
    // the same message again is a replay: rejected, reported at once with the fault bit
    f.inbox.emplace_back(VEC_MT, VEC_MT + sizeof VEC_MT);
    CHECK(c.session(now + 4 * 3600));
    CHECK(f.sent.size() == 4);
    Report r4; auto s4 = sections(f.sent[3], &r4);
    CHECK(s4.size() == 1 && s4[0].type == SEC_ACK && s4[0].p[4] == OLD_SEQUENCE && (r4.faults & F_COMMAND_REJECTED));
    CHECK(f.applied.size() == 3 && s.last_seq == 8);
    // no photo before the next day's slot; next session in 4 h (report interval), not at a photo slot
    CHECK(c.seconds_to_next(now + 4 * 3600) == 4 * 3600);
  }
  {  // a failed send keeps the photo and the acknowledgement for the next session
    Fake f; Settings s; Comms c(f, s, VEC_KEY, 32, 1, mo, sizeof mo, ph, sizeof ph);
    f.send_ok = false;
    CHECK(!c.session(now));
    CHECK(c.faults() & F_MODEM_RETRY);
    f.send_ok = true;
    CHECK(c.session(now + 3600));
    Report r; auto ss = sections(f.sent[0], &r);
    CHECK(f.camera_calls == 1 && ss.size() == 1 && ss[0].type == SEC_PHOTO && (r.faults & F_MODEM_RETRY));
    CHECK(!(c.faults() & F_MODEM_RETRY));
  }
  {  // a 150 KB photo goes in three parts, one per session
    Fake f; Settings s; Comms c(f, s, VEC_KEY, 32, 1, mo, sizeof mo, ph, sizeof ph);
    f.photo_size = 150000;
    for (int i = 0; i < 4; i++) c.session(now + i * 14400);
    CHECK(f.sent.size() == 4 && f.camera_calls == 1);
    size_t total = 0;
    for (int i = 0; i < 3; i++) {
      auto ss = sections(f.sent[i]);
      CHECK(ss.size() == 1 && ss[0].type == SEC_PHOTO && ss[0].p[2] == i && ss[0].p[3] == 3);
      total += ss[0].p.size() - 8;
    }
    CHECK(total == 150000 && sections(f.sent[3]).empty());
  }
  {  // a small modem buffer (the library's IMT_PAYLOAD_SIZE at 12,000): a 30 KB photo goes in 3 parts
    static uint8_t small[12000];
    Fake f; Settings s; Comms c(f, s, VEC_KEY, 32, 1, small, sizeof small, ph, sizeof ph);
    f.photo_size = 30000;
    for (int i = 0; i < 3; i++) c.session(now + i * 14400);
    size_t total = 0;
    for (auto& m : f.sent) { CHECK(m.size() <= sizeof small); auto ss = sections(m); if (!ss.empty()) total += ss[0].p.size() - 8; }
    CHECK(f.sent.size() == 3 && total == 30000);
  }
  {  // a camera that does not answer: the report goes anyway, with the camera fault
    Fake f; Settings s; Comms c(f, s, VEC_KEY, 32, 1, mo, sizeof mo, ph, sizeof ph);
    f.camera_ok = false;
    CHECK(c.session(now));
    Report r; auto ss = sections(f.sent[0], &r);
    CHECK(ss.empty() && (r.faults & F_CAMERA) && f.sent[0].size() == MO_OVERHEAD);
  }
  {  // a bad signature is rejected and nothing is applied
    Fake f; Settings s; Comms c(f, s, VEC_KEY, 32, 1, mo, sizeof mo, ph, sizeof ph);
    std::vector<uint8_t> bad(VEC_MT, VEC_MT + sizeof VEC_MT); bad[bad.size() - 1] ^= 1;
    f.inbox.push_back(bad); s.photos_per_day = 0;
    CHECK(c.session(now));
    auto ss = sections(f.sent.back());
    CHECK(f.applied.empty() && s.last_seq == 0 && ss.size() == 1 && ss[0].p[4] == BAD_SIGNATURE);
  }
  printf(fails ? "%d FAILED\n" : "comms host tests passed\n", fails);
  return fails != 0;
}
