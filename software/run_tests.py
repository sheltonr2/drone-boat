"""Run every software test: the Python protocol and shore tests, and the C++ boat-code tests if a C++ compiler is found.
    python software/run_tests.py
"""
import os, shutil, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
ok = True


def run(cmd, cwd):
    global ok
    print("$", " ".join(cmd)); r = subprocess.run(cmd, cwd=cwd)
    ok &= r.returncode == 0


run([sys.executable, "-m", "unittest", "-q", "test_dronemsg"], os.path.join(HERE, "protocol"))
run([sys.executable, "-m", "unittest", "-q", "test_shore"], os.path.join(HERE, "shore"))
cxx = shutil.which("g++") or shutil.which("clang++")
if not cxx:
    print("no C++ compiler found: skipped the boat-code tests (install g++ or clang++ to run them)")
else:
    lib = os.path.join(HERE, "boat", "lib"); out = tempfile.mkdtemp()
    tests = [("dronemsg", ["dronemsg/src/dronemsg.cpp", "dronemsg/test/test_host.cpp"], ["dronemsg/src", "dronemsg/test"]),
             ("camlink", ["camlink/test/test_camlink.cpp"], ["camlink/src"]),
             ("comms_core", ["comms_core/src/comms_core.cpp", "dronemsg/src/dronemsg.cpp", "comms_core/test/test_comms.cpp"],
              ["comms_core/src", "dronemsg/src", "dronemsg/test"])]
    for name, srcs, incs in tests:
        exe = os.path.join(out, name)
        run([cxx, "-std=c++17", "-Wall", "-Wextra", *[f"-I{os.path.join(lib, i)}" for i in incs], *[os.path.join(lib, s) for s in srcs], "-o", exe], lib)
        if os.path.exists(exe): run([exe], lib)
print("ALL PASSED" if ok else "SOME TESTS FAILED")
sys.exit(0 if ok else 1)
