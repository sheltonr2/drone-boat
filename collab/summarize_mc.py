"""Print the headline numbers of a Monte Carlo result file.  python summarize_mc.py <result.json>"""
import json, sys
s = json.load(open(sys.argv[1]))["result"]["summary"]
keys = ("runs", "errors", "success_percent", "success_ci95", "reporting_percent", "any_arrival_percent", "position_known_at_end_percent", "percent", "arrival_days",
        "failure_causes", "by_launch_month", "mean_airtime_usd", "mean_knockdowns")
out = {k: s.get(k) for k in keys}
if isinstance(out.get("arrival_days"), dict): out["arrival_days"].pop("all", None)
print(json.dumps(out, indent=1, default=str))
