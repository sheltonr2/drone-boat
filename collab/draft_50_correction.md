DRAFT for issue #50, not posted. Needs Randolph's approval.

A correction to our post earlier today. We said the strike simulation bent the stern post on most voyages and broke the counterweight arm. Those two results came from modelling a plunging breaker as a solid wall hitting the whole hull side at once (slamming coefficient up to 2π). That is right for a fixed pile and too harsh for a 27 kg floating hull.

We have since checked the model against measured buoy data: a 40 cm, 18 kg sphere in real 1-2 m breakers recorded mean peak sideways accelerations of 0.80 g (spilling) and 1.18 g (plunging), and rotation rates of 4.2 and 8.7 rad/s (J. Mar. Sci. Eng. 2021, 9(2), 214, Table 2; accelerations low-pass filtered at 10 Hz). Our spilling model matched. Our plunging model gave about 37 g. Matched to the data it gives 2.5 g for our hull, and reaches half the water's speed in about 0.08 s, not 0.01 s.

With that change the 1-in-1,000 load on the stern post falls from 194 to 40 N·m (strength 115) and on the counterweight arm from 61 to 20 N·m (strength 53). Neither is a fail point. The wing spar and rudder-servo results do not change, because they depend on speed and roll rate. Please disregard the 16 g / 68 g acceleration figures in our table; use about 1-3 g. The hull pick-up of roughly 75% of the water's speed and the roll rates stand, with the caution that the buoy rolled two to three times faster than our simulated boat.

Details: docs/Research_Review.md and the correction at the top of docs/Structural_Review.md.
