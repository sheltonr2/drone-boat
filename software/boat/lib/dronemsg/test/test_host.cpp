// Host test for the boat codec against the Python reference's vectors (vectors.h, from dronemsg.py --vectors).
// Build and run on a PC:  g++ -std=c++17 -Wall -Wextra -I../src ../src/dronemsg.cpp test_host.cpp -o test_host && ./test_host
#include <stdio.h>
#include <string.h>
#include "dronemsg.h"
#include "vectors.h"
using namespace dronemsg;

static int fails = 0;
#define CHECK(c) do { if (!(c)) { printf("FAIL %s:%d  %s\n", __FILE__, __LINE__, #c); fails++; } } while (0)

static bool sea_east_of(int32_t, int32_t lon, void* ctx) { return lon > *(int32_t*)ctx; }

int main() {
  // SHA-256 / HMAC: RFC 4231 test case 2
  {
    const char* key = "Jefe"; const char* msg = "what do ya want for nothing?"; uint8_t out[32];
    hmac_sha256((const uint8_t*)key, 4, (const uint8_t*)msg, strlen(msg), out);
    const uint8_t want[8] = {0x5b, 0xdc, 0xc1, 0x46, 0xbf, 0x60, 0x75, 0x4e};
    CHECK(memcmp(out, want, 8) == 0);
  }
  CHECK(crc32((const uint8_t*)"123456789", 9) == 0xCBF43926u);

  // MO: build the same messages as the Python reference
  uint8_t buf[2048];
  {
    MoBuilder b(buf, sizeof buf);
    CHECK(b.begin(1, 513, VEC_REPORT));
    size_t n = b.finish();
    CHECK(n == sizeof VEC_MO_REPORT_ONLY && memcmp(buf, VEC_MO_REPORT_ONLY, n) == 0);
  }
  {
    MoBuilder b(buf, sizeof buf);
    CHECK(b.begin(1, 513, VEC_REPORT));
    CHECK(b.add_ack(7, APPLIED));
    CHECK(b.add_photo(12, 0, 1, sizeof VEC_PHOTO, VEC_PHOTO, sizeof VEC_PHOTO));
    CHECK(b.add_text(SEC_DIAG, "v=1.0;up=86400"));
    size_t n = b.finish();
    CHECK(n == sizeof VEC_MO && memcmp(buf, VEC_MO, n) == 0);
    Report r; CHECK(decode_report(buf + 4, r));
    CHECK(r.lat == VEC_REPORT.lat && r.lon == VEC_REPORT.lon && r.awa_ddeg == -1350 && r.faults == VEC_REPORT.faults);
  }
  {  // a buffer too small refuses the photo and keeps the message valid
    MoBuilder b(buf, 100);
    CHECK(b.begin(1, 1, VEC_REPORT));
    CHECK(!b.add_photo(1, 0, 1, sizeof VEC_PHOTO, VEC_PHOTO, sizeof VEC_PHOTO));
    CHECK(b.finish() == MO_OVERHEAD);
  }

  // MT: verify and walk the commands signed by the Python reference
  {
    MtResult r = mt_verify(VEC_KEY, 32, VEC_MT, sizeof VEC_MT, 1, 7);
    CHECK(r.result == APPLIED && r.seq == 8 && r.count == 5);
    Command c;
    CHECK(mt_command(VEC_MT, sizeof VEC_MT, 0, c) && c.op == HOLD && c.a.hold.p.lat == 181022000 && c.a.hold.p.lon == -644051000 && c.a.hold.radius_m == 1000);
    CHECK(mt_command(VEC_MT, sizeof VEC_MT, 1, c) && c.op == SET_REPORT && c.a.minutes == 240);
    CHECK(mt_command(VEC_MT, sizeof VEC_MT, 2, c) && c.op == SET_ROUTE && c.a.route.n == 3 && c.a.route.pts[1].lat == 489000000);
    CHECK(mt_command(VEC_MT, sizeof VEC_MT, 3, c) && c.op == PHOTO && c.a.photo.max_bytes == 10000);
    CHECK(mt_command(VEC_MT, sizeof VEC_MT, 4, c) && c.op == MODE && c.a.mode == STATION);
    CHECK(!mt_command(VEC_MT, sizeof VEC_MT, 5, c));
  }
  {
    CHECK(mt_verify(VEC_KEY, 32, VEC_MT, sizeof VEC_MT, 1, 8).result == OLD_SEQUENCE);
    CHECK(mt_verify(VEC_KEY, 32, VEC_MT, sizeof VEC_MT, 2, 0).result == WRONG_BOAT);
    uint8_t wrong[32] = {0};
    CHECK(mt_verify(wrong, 32, VEC_MT, sizeof VEC_MT, 1, 0).result == BAD_SIGNATURE);
    uint8_t t[sizeof VEC_MT]; memcpy(t, VEC_MT, sizeof t); t[12] ^= 1;
    CHECK(mt_verify(VEC_KEY, 32, t, sizeof t, 1, 0).result == BAD_SIGNATURE);
    // the point check: everything west of 100W is "land": all points pass; west of 50W: the HOLD point (64.4W) fails
    int32_t w100 = -1000000000, w50 = -500000000;
    CHECK(mt_verify(VEC_KEY, 32, VEC_MT, sizeof VEC_MT, 1, 0, sea_east_of, &w100).result == APPLIED);
    MtResult r = mt_verify(VEC_KEY, 32, VEC_MT, sizeof VEC_MT, 1, 0, sea_east_of, &w50);
    CHECK(r.result == BAD_VALUE && r.bad_index == 0);
  }
  printf(fails ? "%d FAILED\n" : "all host tests passed\n", fails);
  return fails != 0;
}
