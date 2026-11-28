// See comms_core.h.
#include "comms_core.h"
#include <stdio.h>
#include <string.h>

namespace comms {
using namespace dronemsg;

static bool at_sea(int32_t lat, int32_t lon, void* ctx) { return static_cast<Hal*>(ctx)->point_at_sea(lat, lon); }

Comms::Comms(Hal& hal, Settings& s, const uint8_t* key, size_t key_len, uint8_t boat_id, uint8_t* mo_buf, size_t mo_cap,
             uint8_t* photo_buf, size_t photo_cap)
    : hal_(hal), s_(s), key_(key), key_len_(key_len), boat_(boat_id), mo_(mo_buf), mo_cap_(mo_cap), ph_(photo_buf), ph_cap_(photo_cap) {}

static uint32_t slot_index(uint32_t t, uint8_t hour, uint32_t slot) {
  uint32_t off = (uint32_t)hour * 3600u;
  return t < off ? 0 : (t - off) / slot;
}

bool Comms::photo_due(uint32_t now) const {
  return s_.photos_per_day && slot_index(now, s_.photo_hour_utc, slot_seconds()) > s_.last_photo_slot;
}

uint32_t Comms::seconds_to_next(uint32_t now) const {
  uint32_t next = last_session_ ? last_session_ + 60u * s_.report_min : now;
  if (s_.photos_per_day) {
    uint32_t slot = slot_seconds(), t = (s_.last_photo_slot + 1) * slot + 3600u * s_.photo_hour_utc;
    if (t < next) next = t;
  }
  return next > now ? next - now : 0;
}

bool Comms::session(uint32_t now) {
  bool ok = one(now);
  for (int i = 0; i < 2 && again_; i++) { again_ = false; ok = one(now) && ok; }
  again_ = false;
  if (reboot_after_ && !ack_pending_) { reboot_after_ = false; hal_.save(s_); hal_.reboot_companion(); }
  return ok;
}

bool Comms::one(uint32_t now) {
  char line[96];
  Report r; memset(&r, 0, sizeof r);
  if (!hal_.fill_report(r)) r.time = now;

  // the photo: carry on with a big one in parts, else what the shore asked for, else the daily one if due
  if (ph_len_ == 0 && (req_pending_ || photo_due(now))) {
    CameraRequest q = req_;
    if (!req_pending_) { q = CameraRequest(); q.type = CAM_PHOTO; q.kind = 0; q.max_bytes = s_.photo_max; s_.last_photo_slot = slot_index(now, s_.photo_hour_utc, slot_seconds()); }
    req_pending_ = false;
    char err[48] = {0}; uint16_t number = 0;
    size_t n = hal_.camera(q, ph_, ph_cap_, &number, err, sizeof err);
    if (n) {
      ph_len_ = n; ph_sent_ = 0; ph_id_ = number; ph_part_ = 0;
      size_t pm = part_max();
      ph_parts_ = n <= pm ? 1 : (uint8_t)((n + pm - 1) / pm);
      faults_ &= ~F_CAMERA;
    } else {
      faults_ |= F_CAMERA; snprintf(line, sizeof line, "camera: %s", err); hal_.log(line);
    }
  }

  r.last_cmd_seq = s_.last_seq;
  r.faults |= faults_;
  MoBuilder b(mo_, mo_cap_ < MO_MAX ? mo_cap_ : MO_MAX);
  b.begin(boat_, s_.session, r);
  if (ack_pending_) b.add_ack(ack_seq_, (AckResult)ack_res_, ack_idx_);
  if (diag_pending_) {
    char d[400]; int k = snprintf(d, sizeof d, "seq=%lu;rep=%u;ph=%u@%u;phmax=%u;", (unsigned long)s_.last_seq, s_.report_min,
                                  s_.photos_per_day, s_.photo_hour_utc, s_.photo_max);
    if (k > 0 && (size_t)k < sizeof d) hal_.diag(d + k, sizeof d - k);
    b.add_text(SEC_DIAG, d);
  }
  size_t part = 0;
  if (ph_len_) {
    size_t pm = part_max();
    part = ph_len_ - ph_sent_ < pm ? ph_len_ - ph_sent_ : pm;
    if (!b.add_photo(ph_id_, ph_part_, ph_parts_, (uint32_t)ph_len_, ph_ + ph_sent_, part)) { part = 0; hal_.log("photo part did not fit"); }
  }
  size_t n = b.finish();
  last_session_ = now;
  if (!n || !hal_.modem_send(mo_, n)) {
    faults_ |= F_MODEM_RETRY; hal_.log("send failed; will retry next session");
    hal_.save(s_);
    return false;
  }
  s_.session++;
  ack_pending_ = diag_pending_ = false;
  faults_ &= ~(F_MODEM_RETRY | F_COMMAND_REJECTED);
  if (part) { ph_sent_ += part; ph_part_++; if (ph_sent_ >= ph_len_) ph_len_ = 0; }  // one part per session
  hal_.save(s_);

  // commands waiting at the gateway come down after the send; the MO buffer is free again
  for (int i = 0; i < 4; i++) {
    size_t m = hal_.modem_receive(mo_, mo_cap_);
    if (!m) break;
    handle_mt(mo_, m);
  }
  return true;
}

void Comms::handle_mt(const uint8_t* m, size_t n) {
  MtResult res = mt_verify(key_, key_len_, m, n, boat_, s_.last_seq, at_sea, &hal_, hal_.thruster_fitted());
  ack_pending_ = true; ack_res_ = res.result; ack_idx_ = res.bad_index;
  ack_seq_ = res.seq ? res.seq : (n >= 6 ? (uint32_t)m[2] | (uint32_t)m[3] << 8 | (uint32_t)m[4] << 16 | (uint32_t)m[5] << 24 : 0);
  char line[80];
  if (res.result != APPLIED) {
    faults_ |= F_COMMAND_REJECTED;
    snprintf(line, sizeof line, "command message %lu rejected (%u at %u)", (unsigned long)ack_seq_, res.result, res.bad_index);
    hal_.log(line); again_ = true;  // tell the shore now rather than in four hours
    return;
  }
  Command c;
  for (uint8_t i = 0; i < res.count; i++) {
    if (!mt_command(m, n, i, c)) break;
    switch (c.op) {
      case SET_REPORT: s_.report_min = c.a.minutes; break;
      case SET_PHOTO: s_.photos_per_day = c.a.set_photo.per_day; s_.photo_hour_utc = c.a.set_photo.hour_utc; s_.photo_max = c.a.set_photo.max_bytes; break;
      case PHOTO: req_ = CameraRequest(); req_.type = CAM_PHOTO; req_.kind = c.a.photo.kind; req_.stored = c.a.photo.stored;
                  req_.max_bytes = c.a.photo.max_bytes; req_pending_ = true; ph_len_ = 0; again_ = true; break;
      case CLIP: req_ = CameraRequest(); req_.type = CAM_CLIP; req_.seconds = c.a.clip.seconds; req_.max_bytes = c.a.clip.max_bytes;
                 req_pending_ = true; ph_len_ = 0; again_ = true; break;
      case DIAG: diag_pending_ = true; again_ = true; break;
      case REBOOT:
        if (c.a.target == 0) { reboot_after_ = true; again_ = true; }  // after the acknowledgement has gone
        else if (c.a.target == 1) hal_.apply(c);
        break;  // target 2, the camera: it is switched off after every session anyway
      default: hal_.apply(c);
    }
  }
  s_.last_seq = res.seq;
  hal_.save(s_);
  snprintf(line, sizeof line, "command message %lu applied (%u commands)", (unsigned long)res.seq, res.count);
  hal_.log(line);
}

}  // namespace comms
