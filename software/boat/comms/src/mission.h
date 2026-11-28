// The mission manager's side of the companion, as the comms code sees it. Not written yet: the mission manager
// (route, weather avoidance, safe mode, watchdog, MAVLink to the Pixhawk, docs/Build_Plan.md "Software plan") will
// implement these. mission_stub.cpp stands in for it on the bench.
#pragma once
#include <stdint.h>
#include "dronemsg.h"

void mission_begin();
void mission_loop();                                        // called every 50 ms between sessions
bool mission_clock_ok();                                    // true once the clock is set from GPS
bool mission_fill_report(dronemsg::Report& r);             // position, wind, power, mode, faults: everything but the comms fields
bool mission_point_at_sea(int32_t lat_e7, int32_t lon_e7);  // the coastline mask; false rejects the whole command message
void mission_apply(const dronemsg::Command& c);             // SET_ROUTE, GOTO, MODE, HOLD, GEOFENCE, REBOOT (autopilot)
void mission_log(const char* line);                         // to the SD log
