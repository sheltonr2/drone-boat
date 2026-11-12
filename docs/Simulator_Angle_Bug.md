# Simulator bug: every heading sailed at the dead-downwind speed

Found 12 November 2026 while checking the wing study against John's team's model. Fixed in `simulator/drone_sim/sim.py`.

## What was wrong

The speed table (`Polar` in `vpp.py`) takes the wind angle in radians. The voyage simulator passed it in degrees. Any angle above 3.14 was clipped to the table's last row, which is dead downwind (180°). So from the first version of the simulator (8 November) until this fix, **the boat sailed every heading at its dead-downwind speed**, with the wing angle from that row too. Spying on a short voyage showed 96% of lookups clipped.

What that did:
- **Upwind and close reaching were far too fast.** At 7 m/s of wind the true speed at 50° is about 0.28 m/s against 0.43 m/s dead downwind.
- **Broad reaching was too slow.** At 7 m/s the true speed at 90–150° is 0.52–0.56 m/s, 20–30% faster than dead downwind.
- **Routing and arrival times are therefore off in both directions.** Every Monte Carlo result before 12 November is affected: arrival rates, crossing times, the launch-point comparison and the Rev B / C / C1 / C5 comparisons. Failure counts are mostly time-based and less affected, but they depend on time at sea.

The wing shape study made the same mistake in its own script, so its −4% was the dead-downwind change only (see [Wing_Shape_Study.md](Wing_Shape_Study.md)).

## The fix

- `sim.py` converts the angle to radians in both places that look up the table.
- `Polar.__call__` now raises an error for any angle above 3.2, so this mistake cannot come back silently.
- The speed-table cache key now includes a model version, so stale tables are rebuilt.

Also changed in the same update: the wing's stall angle now follows its lift (the wing stalls where its straight-line lift coefficient reaches 1.03), so a stubbier wing stalls later, as real ones do. The old rule made it stall sooner. John's team found this in their port of our foil model (boat-sim PR #325).

## Reruns

`simulator/run_fixed_compare_2023.bat` (Rev C5 against Rev C as first drawn, 2023) is the first run on the corrected simulator. Earlier results should be treated as superseded until rerun.
