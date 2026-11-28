// Camera firmware for the drone boat's stern-post pod (Rev F): Seeed XIAO ESP32S3 Sense, OV3660 (or OV2640), microSD.
//
// The companion switches the camera's 5 V on through a load switch, asks for one thing over the UART (camlink.h),
// and switches it off again. The camera never decides anything for itself and keeps no state but the SD card and a
// photo counter, so a crash costs one photo, not the boat.
//
// Every photo is saved three ways on the SD card, under its number:
//   /photos/NNNNN_full.jpg   full resolution (QXGA 2048 x 1536 on the OV3660), for recovery after the voyage
//   /photos/NNNNN_large.jpg  XGA 1024 x 768, about 60-100 KB, sent only on request (PHOTO kind 2)
//   the standard still, VGA 640 x 480, made as small as the request allows (10 KB by default), sent at once
//
// Written 28 Nov 2026, not yet built or run on hardware. Pin map: Seeed's camera_pins.h for CAMERA_MODEL_XIAO_ESP32S3.
#include <Arduino.h>
#include <FS.h>
#include <SD.h>
#include <SPI.h>
#include <Preferences.h>
#include <esp_sleep.h>
#include "esp_camera.h"
#include "camlink.h"

using namespace camlink;

// ---- pins (XIAO ESP32S3 Sense)
#define PWDN_GPIO_NUM -1
#define RESET_GPIO_NUM -1
#define XCLK_GPIO_NUM 10
#define SIOD_GPIO_NUM 40
#define SIOC_GPIO_NUM 39
#define Y9_GPIO_NUM 48
#define Y8_GPIO_NUM 11
#define Y7_GPIO_NUM 12
#define Y6_GPIO_NUM 14
#define Y5_GPIO_NUM 16
#define Y4_GPIO_NUM 18
#define Y3_GPIO_NUM 17
#define Y2_GPIO_NUM 15
#define VSYNC_GPIO_NUM 38
#define HREF_GPIO_NUM 47
#define PCLK_GPIO_NUM 13
#define SD_CS 21
#define LINK_TX 43   // D6, to the companion's RX
#define LINK_RX 44   // D7, from the companion's TX
#define LINK_BAUD 921600

static HardwareSerial& port = Serial1;
static uint8_t rxbuf[64];
static Parser parser(rxbuf, sizeof rxbuf);
static bool sd_ok = false;
static uint16_t sensor_pid = 0;
static Preferences prefs;

// ---------------------------------------------------------------- link output
static void send_frame(Type t, const uint8_t* a, uint32_t na, const uint8_t* b = nullptr, uint32_t nb = 0) {
  uint8_t h[7], tr[4];
  uint32_t c = header(h, t, na + nb);
  c = crc32_update(c, a, na); if (nb) c = crc32_update(c, b, nb);
  trailer(tr, c);
  port.write(h, 7); if (na) port.write(a, na); if (nb) port.write(b, nb); port.write(tr, 4); port.flush();
}
static void send_error(Error e, const char* text) {
  uint8_t p[64]; p[0] = e; size_t n = strnlen(text, 62); memcpy(p + 1, text, n);
  send_frame(ERROR, p, 1 + n);
}
static void send_hello() {
  uint8_t p[6]; p[0] = VERSION; p[1] = sd_ok; put16(p + 2, prefs.getUShort("photo_no", 0)); put16(p + 4, sensor_pid);
  send_frame(HELLO, p, sizeof p);
}

// ---------------------------------------------------------------- camera
static bool camera_init() {
  camera_config_t c = {};
  c.ledc_channel = LEDC_CHANNEL_0; c.ledc_timer = LEDC_TIMER_0;
  c.pin_d0 = Y2_GPIO_NUM; c.pin_d1 = Y3_GPIO_NUM; c.pin_d2 = Y4_GPIO_NUM; c.pin_d3 = Y5_GPIO_NUM;
  c.pin_d4 = Y6_GPIO_NUM; c.pin_d5 = Y7_GPIO_NUM; c.pin_d6 = Y8_GPIO_NUM; c.pin_d7 = Y9_GPIO_NUM;
  c.pin_xclk = XCLK_GPIO_NUM; c.pin_pclk = PCLK_GPIO_NUM; c.pin_vsync = VSYNC_GPIO_NUM; c.pin_href = HREF_GPIO_NUM;
  c.pin_sccb_sda = SIOD_GPIO_NUM; c.pin_sccb_scl = SIOC_GPIO_NUM; c.pin_pwdn = PWDN_GPIO_NUM; c.pin_reset = RESET_GPIO_NUM;
  c.xclk_freq_hz = 20000000; c.pixel_format = PIXFORMAT_JPEG;
  c.frame_size = FRAMESIZE_UXGA;  // the largest both sensors take; raised to QXGA below for the OV3660
  c.jpeg_quality = 10; c.fb_count = 1; c.fb_location = CAMERA_FB_IN_PSRAM; c.grab_mode = CAMERA_GRAB_LATEST;
  if (esp_camera_init(&c) != ESP_OK) return false;
  sensor_t* s = esp_camera_sensor_get();
  sensor_pid = s->id.PID;
  // the pod looks aft and 10 degrees down through a window: keep auto exposure and white balance on
  s->set_whitebal(s, 1); s->set_awb_gain(s, 1); s->set_exposure_ctrl(s, 1); s->set_gain_ctrl(s, 1);
  return true;
}

static framesize_t full_size() { return sensor_pid == OV3660_PID ? FRAMESIZE_QXGA : FRAMESIZE_UXGA; }

// Frames after a size change or a cold start are badly exposed: throw some away.
static void settle(int frames) {
  for (int i = 0; i < frames; i++) { camera_fb_t* fb = esp_camera_fb_get(); if (fb) esp_camera_fb_return(fb); }
}

// One JPEG at a size, lowering the quality (raising the number) until it fits max_bytes. Caller returns the fb.
static camera_fb_t* grab_fitting(framesize_t size, uint32_t max_bytes, int q0) {
  sensor_t* s = esp_camera_sensor_get();
  s->set_framesize(s, size); settle(2);
  for (int q = q0; q <= 63; q += (q < 30 ? 4 : 8)) {
    s->set_quality(s, q);
    camera_fb_t* fb = esp_camera_fb_get();
    if (!fb) return nullptr;
    if (fb->len <= max_bytes) return fb;
    esp_camera_fb_return(fb);
  }
  return nullptr;
}

static bool save(const char* path, const uint8_t* p, size_t n) {
  if (!sd_ok) return false;
  File f = SD.open(path, FILE_WRITE);
  if (!f) return false;
  size_t w = f.write(p, n); f.close();
  return w == n;
}

static void result(uint16_t number, uint8_t kind, const uint8_t* p, uint32_t n) {
  uint8_t h[3]; put16(h, number); h[2] = kind;
  send_frame(RESULT, h, 3, p, n);
}

// ---------------------------------------------------------------- requests
static void do_photo(uint8_t kind, uint16_t stored, uint32_t max_bytes) {
  char path[40];
  if (kind == 2) {  // a stored photo's large version
    snprintf(path, sizeof path, "/photos/%05u_large.jpg", stored);
    File f = sd_ok ? SD.open(path, FILE_READ) : File();
    if (!f) return send_error(E_NO_SUCH_PHOTO, path);
    size_t n = f.size();
    if (n > max_bytes || n > MAX_PAYLOAD) { f.close(); return send_error(E_TOO_BIG, path); }
    uint8_t* buf = (uint8_t*)ps_malloc(n);
    if (!buf) { f.close(); return send_error(E_CAMERA, "no memory"); }
    f.read(buf, n); f.close();
    result(stored, 0, buf, n); free(buf);
    return;
  }
  uint16_t no = prefs.getUShort("photo_no", 0) + 1;
  prefs.putUShort("photo_no", no);
  // full resolution to the card first, while the exposure is settled
  sensor_t* s = esp_camera_sensor_get();
  s->set_framesize(s, full_size()); s->set_quality(s, 10); settle(4);
  camera_fb_t* fb = esp_camera_fb_get();
  if (!fb) return send_error(E_CAMERA, "capture failed");
  snprintf(path, sizeof path, "/photos/%05u_full.jpg", no);
  bool saved = save(path, fb->buf, fb->len); esp_camera_fb_return(fb);
  // the large version, kept for a later request
  fb = grab_fitting(FRAMESIZE_XGA, 100000, 12);
  if (fb) { snprintf(path, sizeof path, "/photos/%05u_large.jpg", no); saved &= save(path, fb->buf, fb->len); }
  if (kind == 1) {
    if (fb && fb->len <= max_bytes) { result(no, 0, fb->buf, fb->len); esp_camera_fb_return(fb); return; }
    if (fb) esp_camera_fb_return(fb);
    fb = grab_fitting(FRAMESIZE_XGA, max_bytes, 20);
  } else {
    if (fb) esp_camera_fb_return(fb);
    fb = grab_fitting(FRAMESIZE_VGA, max_bytes, 12);
    if (!fb) fb = grab_fitting(FRAMESIZE_QVGA, max_bytes, 12);  // a very small limit: drop to 320 x 240
  }
  if (!fb) return send_error(E_TOO_BIG, "could not fit the limit");
  result(no, 0, fb->buf, fb->len); esp_camera_fb_return(fb);
  (void)saved;  // a failed save shows as sd_ok = 0 in the next HELLO only if the card is gone; logged by the companion
}

static void do_clip(uint8_t seconds, uint32_t max_bytes) {
  // A clip is a run of QVGA JPEG frames (MJPEG), about 2 a second, each made small enough for the whole to fit.
  const int fps = 2; int frames = seconds * fps;
  uint32_t per = max_bytes / frames;
  if (per < 1500) return send_error(E_TOO_BIG, "clip limit too small");
  uint8_t* buf = (uint8_t*)ps_malloc(max_bytes);
  if (!buf) return send_error(E_CAMERA, "no memory");
  uint32_t n = 0; sensor_t* s = esp_camera_sensor_get();
  s->set_framesize(s, FRAMESIZE_QVGA); settle(3);
  int q = 20;
  for (int i = 0; i < frames; i++) {
    uint32_t t0 = millis();
    s->set_quality(s, q);
    camera_fb_t* fb = esp_camera_fb_get();
    if (!fb) break;
    if (fb->len > per && q < 63) q += 6;  // too big: the next frames get smaller; this one goes if it fits overall
    if (n + fb->len <= max_bytes) { memcpy(buf + n, fb->buf, fb->len); n += fb->len; }
    esp_camera_fb_return(fb);
    while (millis() - t0 < 1000 / fps) delay(5);
  }
  uint16_t no = prefs.getUShort("photo_no", 0) + 1; prefs.putUShort("photo_no", no);
  char path[40]; snprintf(path, sizeof path, "/photos/%05u_clip.mjpeg", no); save(path, buf, n);
  if (n == 0) send_error(E_CAMERA, "no frames"); else result(no, 1, buf, n);
  free(buf);
}

// ---------------------------------------------------------------- main
void setup() {
  port.setRxBufferSize(512);
  port.begin(LINK_BAUD, SERIAL_8N1, LINK_RX, LINK_TX);
  prefs.begin("camera", false);
  sd_ok = SD.begin(SD_CS);
  if (sd_ok && !SD.exists("/photos")) SD.mkdir("/photos");
  if (!camera_init()) { send_error(E_CAMERA, "camera init failed"); }
  settle(6);  // auto exposure needs a few frames after power-up
}

void loop() {
  static uint32_t last_hello = 0, start = millis();
  static bool answered = false;
  if (!answered && millis() - last_hello > 1000) { send_hello(); last_hello = millis(); }
  while (port.available()) {
    if (!parser.push(port.read())) continue;
    const uint8_t* p = parser.payload(); uint32_t n = parser.length();
    switch (parser.type()) {
      case PHOTO:
        if (n != 7) { send_error(E_BAD_REQUEST, "PHOTO length"); break; }
        do_photo(p[0], get16(p + 1), get32(p + 3)); answered = true; start = millis(); break;
      case CLIP:
        if (n != 5) { send_error(E_BAD_REQUEST, "CLIP length"); break; }
        do_clip(p[0], get32(p + 1)); answered = true; start = millis(); break;
      case DONE:
        esp_deep_sleep_start();  // the companion is about to cut the power anyway
        break;
      default:
        send_error(E_BAD_REQUEST, "unexpected frame");
    }
  }
  // the companion should cut the power within a minute; if it doesn't, stop drawing current
  if (millis() - start > 120000) esp_deep_sleep_start();
}
