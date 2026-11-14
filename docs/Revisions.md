# Revision convention

Adopted 12 Nov 2026.

- **A new letter (Rev D, Rev E, ...)** when we add or remove a system, or change how the parts connect: wiring, power, controllers, sensors, comms. Also when a drawing set is frozen for building, so whatever we build first carries a clean letter.
- **A numbered sub-revision (D1, D2, ...)** for fixes and changes to parts inside that design: a stronger part, a new size, a better material, a note on the drawings.
- **The letter alone (Rev D)** is the first issue of a letter, the same as D0.
- Every drawing sheet shows the revision in its title block. The cover sheet D00 lists every revision and what changed. Each letter has its own design note (`docs/Design_RevX.md`) and simulator design file (`designs/revX_design.json`); sub-revisions keep their own file too (`designs/revC5_design.json`).
- The simulator's `revision` key holds the letter. Results files name the revision they were run on.

## History

| Rev | Date | What it was |
|---|---|---|
| B | 8 Nov 2026 | First full design; wing counterweight on a forward arm |
| C | 10 Nov 2026 | After the first real-weather runs: bulkheads and foam fill, sealed battery box, twin rudders, bigger spar and bulb, YB3 backup tracker |
| C1 | 11 Nov | Electronics box raised above the flood level |
| C2 | 11 Nov | Keel fin rebuilt (hardwood core, tenon, floors) |
| C3 | 11 Nov | Structural review: YB3 to the foredeck, fibreglass post and counterweight arm, servo-savers, 30 × 22 spar |
| C4 | 11 Nov | Acetal mast bearings; build notes |
| C5 | 11 Nov | Shorter, wider wing (0.80 × 0.375 m) |
| D | 12 Nov | Limp-home controller, potting, RockBLOCK Plus in the hatch lid, main GPS to the stern post ([Design_RevD.md](Design_RevD.md)). Drafted as "C6" |
| **E** | 13 Nov | Bilge pump and keep-sailing leak response, vents and a pressure-test valve, humidity sensor; sealed rudder servos, potted tail servo with a detent, wave-filtered steering (was "deadband steering", corrected the same day); weed fairing ([Design_RevE.md](Design_RevE.md)). Proposed as "D1": a new letter because it adds a system (the pump) and a sensor |
