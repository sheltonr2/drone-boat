// Host test for the camera link framing.  g++ -std=c++17 -Wall -Wextra -I../src test_camlink.cpp -o t && ./t
#include <stdio.h>
#include <stdlib.h>
#include "camlink.h"
using namespace camlink;

static int fails = 0;
#define CHECK(c) do { if (!(c)) { printf("FAIL %s:%d  %s\n", __FILE__, __LINE__, #c); fails++; } } while (0)

int main() {
  static uint8_t jpg[30000], wire[40000], rx[60000];
  for (size_t i = 0; i < sizeof jpg; i++) jpg[i] = (uint8_t)(i * 131 + 7);
  // a frame written in pieces (header, payload, trailer), as the camera streams a big photo
  uint8_t h[7], t[4]; uint32_t c = header(h, RESULT, sizeof jpg); c = crc32_update(c, jpg, sizeof jpg); trailer(t, c);
  size_t n = 0;
  memcpy(wire + n, "\x00\xa5\x11", 3); n += 3;  // noise before the frame
  memcpy(wire + n, h, 7); n += 7; memcpy(wire + n, jpg, sizeof jpg); n += sizeof jpg; memcpy(wire + n, t, 4); n += 4;
  n += frame(wire + n, sizeof wire - n, DONE, nullptr, 0);
  Parser p(rx, sizeof rx); int got = 0;
  for (size_t i = 0; i < n; i++) {
    if (p.push(wire[i])) {
      got++;
      if (got == 1) CHECK(p.type() == RESULT && p.length() == sizeof jpg && memcmp(p.payload(), jpg, sizeof jpg) == 0);
      if (got == 2) CHECK(p.type() == DONE && p.length() == 0);
    }
  }
  CHECK(got == 2 && p.errors == 0); if (got != 2 || p.errors) printf("got %d errors %u\n", got, (unsigned)p.errors);
  // a corrupted byte is caught by the CRC
  uint8_t small[64]; uint8_t req[7] = {0, 0, 0, 0x10, 0x27, 0, 0};
  size_t m = frame(small, sizeof small, PHOTO, req, 7); small[9] ^= 0x40;
  Parser q(rx, sizeof rx); bool ok = false;
  for (size_t i = 0; i < m; i++) ok |= q.push(small[i]);
  CHECK(!ok && q.errors == 1);
  // a frame longer than the buffer is dropped
  Parser r(rx, 100); ok = false;
  for (size_t i = 0; i < n; i++) ok |= (r.push(wire[i]) && r.type() == RESULT);
  CHECK(!ok && r.errors >= 1);
  printf(fails ? "%d FAILED\n" : "camlink host tests passed\n", fails);
  return fails != 0;
}
