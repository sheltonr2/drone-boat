// Bench stand-in for the mission manager: no GPS, no autopilot. The clock is set by hand on the console
// ("time <unix seconds>"), the report carries that time and a fixed position, and commands are printed.
// Replace with the real mission manager; nothing here goes to sea.
#include <Arduino.h>
#include <sys/time.h>
#include "mission.h"

static bool clock_set = false;

void mission_begin() { Serial.println("mission stub: bench mode. Set the clock with  time <unix seconds>"); }

void mission_loop() {
  // the comms console reads Serial; the stub only peeks for "time ..." lines it was handed (see comms main.cpp)
}

bool mission_clock_ok() {
  if (!clock_set && time(nullptr) > 1700000000) clock_set = true;
  return clock_set;
}

bool mission_fill_report(dronemsg::Report& r) {
  r.time = (uint32_t)time(nullptr);
  r.lat = 181022000; r.lon = -644051000;  // 20 km ESE of the Norman offing, a bench placeholder
  r.mode = dronemsg::STATION; r.soc = 99; r.batt_mv = 13300;
  return true;
}

bool mission_point_at_sea(int32_t, int32_t) { return true; }

void mission_apply(const dronemsg::Command& c) { Serial.printf("mission stub: would apply command op %u\n", c.op); }

void mission_log(const char* line) { (void)line; }
