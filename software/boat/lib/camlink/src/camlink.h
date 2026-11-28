// Camera link: framing for the UART between the companion ESP32 and the camera (XIAO ESP32S3 Sense). Header-only and
// portable, used by both firmwares and tested on a PC (test/test_camlink.cpp).
//
// Frame:  0xA5 0x5A | type u8 | length u32 LE | payload | CRC-32 (IEEE) of type, length and payload, u32 LE
//
// Session: the companion switches the camera on; the camera sends HELLO; the companion sends one request (PHOTO or
// CLIP); the camera answers with RESULT (or ERROR), waits for DONE, then the companion switches it off.
#pragma once
#include <stddef.h>
#include <stdint.h>
#include <string.h>

namespace camlink {

enum Type : uint8_t {
  HELLO = 0x01,   // camera -> companion: u8 version, u8 sd_ok, u16 photos stored, u16 sensor PID
  PHOTO = 0x10,   // companion -> camera: u8 kind (0 standard, 1 large, 2 stored), u16 stored number, u32 max bytes
  CLIP = 0x11,    // companion -> camera: u8 seconds, u32 max bytes
  RESULT = 0x20,  // camera -> companion: u16 photo number (on the SD card), u8 kind (0 photo, 1 clip), then the JPEG/MJPEG bytes
  ERROR = 0x21,   // camera -> companion: u8 code (below), then text
  DONE = 0x30     // companion -> camera: received, you may be switched off
};
enum Error : uint8_t { E_CAMERA = 1, E_SD = 2, E_TOO_BIG = 3, E_NO_SUCH_PHOTO = 4, E_BAD_REQUEST = 5 };
constexpr uint8_t VERSION = 1;
constexpr uint32_t MAX_PAYLOAD = 120000;

inline uint32_t crc32_update(uint32_t crc, const uint8_t* p, size_t n) {  // crc starts at 0xFFFFFFFF; final value is ~crc
  while (n--) {
    crc ^= *p++;
    for (int k = 0; k < 8; k++) crc = (crc >> 1) ^ (0xEDB88320u & (0u - (crc & 1u)));
  }
  return crc;
}

// Writes the header (7 bytes) for a payload of n bytes; returns the running CRC to continue over the payload.
inline uint32_t header(uint8_t out[7], Type t, uint32_t n) {
  out[0] = 0xA5; out[1] = 0x5A; out[2] = t;
  out[3] = n; out[4] = n >> 8; out[5] = n >> 16; out[6] = n >> 24;
  return crc32_update(0xFFFFFFFFu, out + 2, 5);
}
inline void trailer(uint8_t out[4], uint32_t running_crc) {
  uint32_t c = ~running_crc; out[0] = c; out[1] = c >> 8; out[2] = c >> 16; out[3] = c >> 24;
}

// Whole frame into a buffer (for small frames). Returns the length, or 0 if it does not fit.
inline size_t frame(uint8_t* out, size_t cap, Type t, const uint8_t* p, uint32_t n) {
  if (cap < (size_t)n + 11) return 0;
  uint32_t c = header(out, t, n);
  if (n) memcpy(out + 7, p, n);
  c = crc32_update(c, p, n);
  trailer(out + 7 + n, c);
  return n + 11;
}

// Byte-at-a-time receiver. Feed every byte; when push() returns true a complete, CRC-checked frame is in
// type()/payload()/length(). The caller owns the payload buffer (in PSRAM on the companion for clips).
class Parser {
 public:
  Parser(uint8_t* buf, uint32_t cap) : buf_(buf), cap_(cap) {}
  void reset() { st_ = 0; }
  Type type() const { return (Type)t_; }
  const uint8_t* payload() const { return buf_; }
  uint32_t length() const { return n_; }
  uint32_t errors = 0;
  bool push(uint8_t b) {
    switch (st_) {
      case 0: if (b == 0xA5) st_ = 1; return false;
      case 1: st_ = (b == 0x5A) ? 2 : (b == 0xA5 ? 1 : 0); return false;
      case 2: t_ = b; crc_ = crc32_update(0xFFFFFFFFu, &b, 1); n_ = 0; k_ = 0; st_ = 3; return false;
      case 3:
        crc_ = crc32_update(crc_, &b, 1); n_ |= (uint32_t)b << (8 * k_);
        if (++k_ == 4) {
          if (n_ > cap_ || n_ > MAX_PAYLOAD) { errors++; st_ = 0; return false; }
          i_ = 0; k_ = 0; got_ = 0; st_ = n_ ? 4 : 5;
        }
        return false;
      case 4:
        buf_[i_++] = b; crc_ = crc32_update(crc_, &b, 1);
        if (i_ == n_) { st_ = 5; k_ = 0; got_ = 0; }
        return false;
      case 5:
        got_ |= (uint32_t)b << (8 * k_);
        if (++k_ < 4) return false;
        st_ = 0;
        if (got_ != ~crc_) { errors++; return false; }
        return true;
    }
    st_ = 0; return false;
  }
 private:
  uint8_t* buf_; uint32_t cap_, n_ = 0, i_ = 0, crc_ = 0, got_ = 0; uint8_t st_ = 0, t_ = 0, k_ = 0;
};

inline void put16(uint8_t* p, uint16_t v) { p[0] = v; p[1] = v >> 8; }
inline void put32(uint8_t* p, uint32_t v) { p[0] = v; p[1] = v >> 8; p[2] = v >> 16; p[3] = v >> 24; }
inline uint16_t get16(const uint8_t* p) { return p[0] | (uint16_t)p[1] << 8; }
inline uint32_t get32(const uint8_t* p) { return p[0] | (uint32_t)p[1] << 8 | (uint32_t)p[2] << 16 | (uint32_t)p[3] << 24; }

}  // namespace camlink
