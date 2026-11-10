# Rev C on open water: interactive 3D view

`index.html` is one self-contained page: the Rev C boat on a moving sea, with sliders for wind speed, heading off the wind, wave height and period, and sun height, plus buttons that hit the boat with a breaking wave.

**To use it:** download `index.html` (or the whole repo) and open the file in a browser. It needs an internet connection the first time, to load the three.js library from cdnjs. GitHub shows the file as source code; it does not run it from the repo page.

The boat is built from the Rev C dimensions in `build-files/source/design.py`. Its motion uses the simulator's Rev C mass, righting-arm curve (`docs/data/revC_gz_curve.csv`), speed model and breaking-wave strike rate. It is a visual aid, not a second simulator: the boat follows the wave surface and rolls on its stability curve, and the sea is a sum of 8 trochoidal waves.
