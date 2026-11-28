// Boat side of the protocol, version 1. See dronemsg.h and software/protocol/PROTOCOL.md.
#include "dronemsg.h"
#include <string.h>

namespace dronemsg {

// ------------------------------------------------------------------ little-endian helpers
static inline void put16(uint8_t* p, uint16_t v) { p[0] = v; p[1] = v >> 8; }
static inline void put32(uint8_t* p, uint32_t v) { p[0] = v; p[1] = v >> 8; p[2] = v >> 16; p[3] = v >> 24; }
static inline uint16_t get16(const uint8_t* p) { return p[0] | (uint16_t)p[1] << 8; }
static inline uint32_t get32(const uint8_t* p) { return p[0] | (uint32_t)p[1] << 8 | (uint32_t)p[2] << 16 | (uint32_t)p[3] << 24; }

// ------------------------------------------------------------------ CRC-32 (IEEE, same as zlib.crc32)
uint32_t crc32(const uint8_t* p, size_t n, uint32_t crc) {
  crc = ~crc;
  while (n--) {
    crc ^= *p++;
    for (int k = 0; k < 8; k++) crc = (crc >> 1) ^ (0xEDB88320u & (0u - (crc & 1u)));
  }
  return ~crc;
}

// ------------------------------------------------------------------ SHA-256 and HMAC (FIPS 180-4, RFC 2104)
namespace {
const uint32_t K256[64] = {
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5, 0xd807aa98, 0x12835b01,
    0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174, 0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc,
    0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da, 0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147,
    0x06ca6351, 0x14292967, 0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070, 0x19a4c116, 0x1e376c08,
    0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3, 0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
    0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2};
inline uint32_t ror(uint32_t x, int n) { return (x >> n) | (x << (32 - n)); }

struct Sha256 {
  uint32_t h[8]; uint8_t buf[64]; uint64_t len = 0; size_t used = 0;
  Sha256() {
    const uint32_t iv[8] = {0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19};
    memcpy(h, iv, sizeof h);
  }
  void block(const uint8_t* p) {
    uint32_t w[64];
    for (int i = 0; i < 16; i++) w[i] = (uint32_t)p[4 * i] << 24 | (uint32_t)p[4 * i + 1] << 16 | (uint32_t)p[4 * i + 2] << 8 | p[4 * i + 3];
    for (int i = 16; i < 64; i++) {
      uint32_t s0 = ror(w[i - 15], 7) ^ ror(w[i - 15], 18) ^ (w[i - 15] >> 3), s1 = ror(w[i - 2], 17) ^ ror(w[i - 2], 19) ^ (w[i - 2] >> 10);
      w[i] = w[i - 16] + s0 + w[i - 7] + s1;
    }
    uint32_t a = h[0], b = h[1], c = h[2], d = h[3], e = h[4], f = h[5], g = h[6], k = h[7];
    for (int i = 0; i < 64; i++) {
      uint32_t t1 = k + (ror(e, 6) ^ ror(e, 11) ^ ror(e, 25)) + ((e & f) ^ (~e & g)) + K256[i] + w[i];
      uint32_t t2 = (ror(a, 2) ^ ror(a, 13) ^ ror(a, 22)) + ((a & b) ^ (a & c) ^ (b & c));
      k = g; g = f; f = e; e = d + t1; d = c; c = b; b = a; a = t1 + t2;
    }
    h[0] += a; h[1] += b; h[2] += c; h[3] += d; h[4] += e; h[5] += f; h[6] += g; h[7] += k;
  }
  void update(const uint8_t* p, size_t n) {
    len += n;
    while (n) {
      size_t take = 64 - used < n ? 64 - used : n;
      memcpy(buf + used, p, take); used += take; p += take; n -= take;
      if (used == 64) { block(buf); used = 0; }
    }
  }
  void final(uint8_t out[32]) {
    uint64_t bits = len * 8; uint8_t pad = 0x80, zero = 0, lb[8];
    update(&pad, 1);
    while (used != 56) update(&zero, 1);
    for (int i = 0; i < 8; i++) lb[i] = bits >> (56 - 8 * i);
    update(lb, 8);
    for (int i = 0; i < 8; i++) { out[4 * i] = h[i] >> 24; out[4 * i + 1] = h[i] >> 16; out[4 * i + 2] = h[i] >> 8; out[4 * i + 3] = h[i]; }
  }
};
}  // namespace

void hmac_sha256(const uint8_t* key, size_t key_len, const uint8_t* msg, size_t n, uint8_t out[32]) {
  uint8_t k[64] = {0}, pad[64], inner[32];
  if (key_len > 64) { Sha256 s; s.update(key, key_len); s.final(k); } else memcpy(k, key, key_len);
  for (int i = 0; i < 64; i++) pad[i] = k[i] ^ 0x36;
  { Sha256 s; s.update(pad, 64); s.update(msg, n); s.final(inner); }
  for (int i = 0; i < 64; i++) pad[i] = k[i] ^ 0x5c;
  { Sha256 s; s.update(pad, 64); s.update(inner, 32); s.final(out); }
}

// ------------------------------------------------------------------ report
void encode_report(const Report& r, uint8_t o[REPORT_LEN]) {
  put32(o + 0, r.time); put32(o + 4, (uint32_t)r.lat); put32(o + 8, (uint32_t)r.lon);
  put16(o + 12, r.sog_cms); put16(o + 14, r.cog_cdeg); put16(o + 16, r.heading_cdeg);
  put16(o + 18, (uint16_t)r.awa_ddeg); put16(o + 20, r.aws_cms); put16(o + 22, r.batt_mv);
  o[24] = r.soc; put16(o + 25, r.solar_dw); o[27] = (uint8_t)r.wing_deg; o[28] = (uint8_t)r.rudder_deg;
  o[29] = r.humidity; o[30] = (uint8_t)r.temp_c; o[31] = r.leak; o[32] = r.mode; o[33] = r.wp_index; o[34] = r.pump_runs;
  put32(o + 35, r.last_cmd_seq); put32(o + 39, r.faults);
}

bool decode_report(const uint8_t i[REPORT_LEN], Report& r) {
  r.time = get32(i); r.lat = (int32_t)get32(i + 4); r.lon = (int32_t)get32(i + 8);
  r.sog_cms = get16(i + 12); r.cog_cdeg = get16(i + 14); r.heading_cdeg = get16(i + 16);
  r.awa_ddeg = (int16_t)get16(i + 18); r.aws_cms = get16(i + 20); r.batt_mv = get16(i + 22);
  r.soc = i[24]; r.solar_dw = get16(i + 25); r.wing_deg = (int8_t)i[27]; r.rudder_deg = (int8_t)i[28];
  r.humidity = i[29]; r.temp_c = (int8_t)i[30]; r.leak = i[31]; r.mode = i[32]; r.wp_index = i[33]; r.pump_runs = i[34];
  r.last_cmd_seq = get32(i + 35); r.faults = get32(i + 39);
  return true;
}

// ------------------------------------------------------------------ MO builder
bool MoBuilder::begin(uint8_t boat_id, uint16_t session, const Report& r) {
  n_ = 0;
  if (cap_ < MO_OVERHEAD) return false;
  b_[0] = MO_MAGIC; b_[1] = boat_id; put16(b_ + 2, session);
  encode_report(r, b_ + 4); n_ = 4 + REPORT_LEN;
  return true;
}
size_t MoBuilder::room() const { return n_ + 3 + 4 <= cap_ ? cap_ - n_ - 3 - 4 : 0; }
bool MoBuilder::header(uint8_t kind, size_t n) {
  if (n_ == 0 || n > 0xFFFF || n_ + 3 + n + 4 > cap_) return false;
  b_[n_] = kind; put16(b_ + n_ + 1, (uint16_t)n); n_ += 3;
  return true;
}
bool MoBuilder::add_ack(uint32_t seq, AckResult res, uint8_t index) {
  if (!header(SEC_ACK, 6)) return false;
  put32(b_ + n_, seq); b_[n_ + 4] = res; b_[n_ + 5] = index; n_ += 6;
  return true;
}
bool MoBuilder::add_photo(uint16_t id, uint8_t part, uint8_t parts, uint32_t total, const uint8_t* d, size_t n) {
  if (!header(SEC_PHOTO, 8 + n)) return false;
  put16(b_ + n_, id); b_[n_ + 2] = part; b_[n_ + 3] = parts; put32(b_ + n_ + 4, total);
  memcpy(b_ + n_ + 8, d, n); n_ += 8 + n;
  return true;
}
bool MoBuilder::add_text(Section kind, const char* t) {
  size_t n = strlen(t);
  if (!header(kind, n)) return false;
  memcpy(b_ + n_, t, n); n_ += n;
  return true;
}
size_t MoBuilder::finish() {
  if (n_ == 0 || n_ + 4 > cap_) return 0;
  put32(b_ + n_, crc32(b_, n_)); n_ += 4;
  size_t n = n_; n_ = 0;
  return n;
}

// ------------------------------------------------------------------ MT
static Point pt(const uint8_t* p) { return Point{(int32_t)get32(p), (int32_t)get32(p + 4)}; }
static bool pt_ok(const Point& q, PointCheck chk, void* ctx) {
  if (q.lat < -900000000 || q.lat > 900000000 || q.lon < -1800000000 || q.lon > 1800000000) return false;
  return !chk || chk(q.lat, q.lon, ctx);
}

// Parses command at offset *off; on success advances *off. Returns BAD_VALUE, UNKNOWN_COMMAND or APPLIED.
static AckResult parse(const uint8_t* m, size_t end, size_t* off, Command& c, PointCheck chk, void* ctx, bool thruster) {
  if (*off + 3 > end) return BAD_VALUE;
  uint8_t op = m[*off]; uint16_t n = get16(m + *off + 1); const uint8_t* p = m + *off + 3;
  if (*off + 3 + n > end) return BAD_VALUE;
  c.op = (Op)op;
  switch (op) {
    case SET_ROUTE:
      if (n < 1 || p[0] < 1 || p[0] > 50 || n != 1 + 8 * p[0]) return BAD_VALUE;
      c.a.route.n = p[0];
      for (int i = 0; i < p[0]; i++) { c.a.route.pts[i] = pt(p + 1 + 8 * i); if (!pt_ok(c.a.route.pts[i], chk, ctx)) return BAD_VALUE; }
      break;
    case GOTO:
      if (n != 8) return BAD_VALUE;
      c.a.go = pt(p); if (!pt_ok(c.a.go, chk, ctx)) return BAD_VALUE;
      break;
    case MODE:
      if (n != 1 || p[0] > SAFE || (p[0] == SAIL_THRUST && !thruster)) return BAD_VALUE;
      c.a.mode = p[0];
      break;
    case SET_REPORT:
      if (n != 2) return BAD_VALUE;
      c.a.minutes = get16(p); if (c.a.minutes < 30 || c.a.minutes > 1440) return BAD_VALUE;
      break;
    case HOLD:
      if (n != 10) return BAD_VALUE;
      c.a.hold.p = pt(p); c.a.hold.radius_m = get16(p + 8);
      if (!pt_ok(c.a.hold.p, chk, ctx) || c.a.hold.radius_m < 200 || c.a.hold.radius_m > 5000) return BAD_VALUE;
      break;
    case GEOFENCE:
      if (n < 2 || p[0] > 1 || n != 2 + 8 * p[1] || p[1] > 20 || (p[0] == 1 && p[1] < 3)) return BAD_VALUE;
      c.a.fence.action = p[0]; c.a.fence.n = p[1];
      for (int i = 0; i < p[1]; i++) c.a.fence.pts[i] = pt(p + 2 + 8 * i);  // fence points may be on land
      break;
    case DIAG:
      if (n != 0) return BAD_VALUE;
      break;
    case REBOOT:
      if (n != 1 || p[0] > 2) return BAD_VALUE;
      c.a.target = p[0];
      break;
    case PHOTO:
      if (n != 7 || p[0] > 2) return BAD_VALUE;
      c.a.photo.kind = p[0]; c.a.photo.stored = get16(p + 1); c.a.photo.max_bytes = get32(p + 3);
      if (c.a.photo.max_bytes < 2000 || c.a.photo.max_bytes > 100000) return BAD_VALUE;
      break;
    case CLIP:
      if (n != 5) return BAD_VALUE;
      c.a.clip.seconds = p[0]; c.a.clip.max_bytes = get32(p + 1);
      if (c.a.clip.seconds < 1 || c.a.clip.seconds > 10 || c.a.clip.max_bytes > 100000) return BAD_VALUE;
      break;
    case SET_PHOTO:
      if (n != 4) return BAD_VALUE;
      c.a.set_photo.per_day = p[0]; c.a.set_photo.hour_utc = p[1]; c.a.set_photo.max_bytes = get16(p + 2);
      if (p[0] > 4 || p[1] > 23 || c.a.set_photo.max_bytes < 2000 || c.a.set_photo.max_bytes > 20000) return BAD_VALUE;
      break;
    default:
      return UNKNOWN_COMMAND;
  }
  *off += 3 + n;
  return APPLIED;
}

static bool ct_equal(const uint8_t* a, const uint8_t* b, size_t n) {
  uint8_t d = 0;
  for (size_t i = 0; i < n; i++) d |= a[i] ^ b[i];
  return d == 0;
}

MtResult mt_verify(const uint8_t* key, size_t key_len, const uint8_t* m, size_t n, uint8_t boat_id, uint32_t last_seq,
                   PointCheck chk, void* ctx, bool thruster) {
  MtResult r{BAD_VALUE, 0xFF, 0, 0, 0};
  if (n < 10 + TAG_LEN) return r;
  size_t body = n - TAG_LEN; uint8_t mac[32];
  hmac_sha256(key, key_len, m, body, mac);
  if (!ct_equal(mac, m + body, TAG_LEN)) { r.result = BAD_SIGNATURE; return r; }
  if (m[0] != MT_MAGIC) return r;
  r.seq = get32(m + 2); r.issued_at = get32(m + 6);
  if (m[1] != boat_id) { r.result = WRONG_BOAT; return r; }
  if (r.seq <= last_seq) { r.result = OLD_SEQUENCE; return r; }
  size_t off = 10; uint8_t i = 0; Command c;
  while (off < body) {
    AckResult a = parse(m, body, &off, c, chk, ctx, thruster);
    if (a != APPLIED) { r.result = a; r.bad_index = i; return r; }
    if (++i == 0xFF) { r.result = BAD_VALUE; r.bad_index = i; return r; }
  }
  r.result = APPLIED; r.count = i;
  return r;
}

bool mt_command(const uint8_t* m, size_t n, uint8_t index, Command& c) {
  if (n < 10 + TAG_LEN) return false;
  size_t body = n - TAG_LEN, off = 10;
  for (uint8_t i = 0; off < body; i++) {
    if (parse(m, body, &off, c, nullptr, nullptr, true) != APPLIED) return false;
    if (i == index) return true;
  }
  return false;
}

}  // namespace dronemsg
