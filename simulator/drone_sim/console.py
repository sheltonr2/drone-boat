"""Progress lines that reach the person's console window even when stdout and stderr are redirected to a log file."""
import os, sys, time

_con = None


def _open():
    global _con
    if _con is None:
        for dev in (("CON",) if os.name == "nt" else ("/dev/tty",)):
            try:
                _con = open(dev, "w"); break
            except OSError:
                continue
        else:
            _con = sys.stderr
    return _con


def say(msg, end="\n"):
    try:
        c = _open(); c.write(msg + end); c.flush()
    except Exception:
        pass


class Progress:
    """One updating line: 'Voyages 120 of 250 (48%)  elapsed 12 min, about 13 min left  arrived so far: 47'."""
    def __init__(self, what, total):
        self.what, self.total, self.t0, self.last = what, total, time.time(), 0.0
        say(f"{what}: starting {total} ... (this window updates as it goes)")

    def update(self, done, extra=""):
        now = time.time()
        if done < self.total and now - self.last < 2.0:
            return
        self.last = now
        el = now - self.t0; left = el/done*(self.total - done) if done else 0
        fmt = lambda s: f"{s/60:.0f} min" if s >= 90 else f"{s:.0f} s"
        say(f"\r  {self.what} {done} of {self.total} ({100*done/self.total:.0f}%)  elapsed {fmt(el)}, about {fmt(left)} left  {extra}      ",
            end="" if done < self.total else "\n")
