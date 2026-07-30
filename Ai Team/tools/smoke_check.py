#!/usr/bin/env python3
"""
SMOKE CHECK - post-build verification (Audits 3/4 recommendation, made permanent)

The two highest-signal checks from five audit rounds, automated:
  1. build/main.* must NOT be the "Fallback Build" placeholder (N1 regressions)
  2. every .py fragment in output/code must pass py_compile (C5 regressions)

Also reports: build/DONE presence, per-role folder counts, and compiles
build/main.py itself when it is Python.

Exit code 0 = all checks pass, 1 = at least one failure.
Runs standalone (python tools/smoke_check.py) and is auto-invoked by studio.py
after every completed build.
"""

import py_compile
import sys
import tempfile
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
BUILD_DIR = BASE / "build"
OUTPUT_DIR = BASE / "output"

failures = []

def check(cond, ok_msg, fail_msg):
    if cond:
        print(f"PASS  {ok_msg}")
    else:
        print(f"FAIL  {fail_msg}")
        failures.append(fail_msg)

# 1. build/main.* exists and is not the placeholder
main_candidates = [p for p in BUILD_DIR.glob("main.*") if p.suffix not in (".md", ".txt")]
check(len(main_candidates) > 0, f"build entry exists: {[m.name for m in main_candidates]}", "no build/main.* found")

for m in main_candidates:
    try:
        text = m.read_text(encoding="utf-8", errors="replace")
        check("Fallback Build" not in text,
              f"{m.name} is real LLM output",
              f"{m.name} is the FALLBACK PLACEHOLDER - integrator output was lost")
    except Exception as e:
        check(False, "", f"could not read {m.name}: {e}")

# 2. every .py fragment passes py_compile
code_py = sorted((OUTPUT_DIR / "code").glob("*.py")) if (OUTPUT_DIR / "code").exists() else []
compiled, failed = 0, []
for f in code_py:
    try:
        with tempfile.NamedTemporaryFile(suffix=".pyc", delete=False) as tmp:
            py_compile.compile(str(f), cfile=tmp.name, doraise=True)
        compiled += 1
    except py_compile.PyCompileError as e:
        failed.append(f.name)
check(not failed, f"output/code fragments compile: {compiled}/{len(code_py)} OK", f"fragments FAIL py_compile: {failed}")

# 3. build/main.py itself compiles (if python)
main_py = BUILD_DIR / "main.py"
if main_py.exists():
    try:
        with tempfile.NamedTemporaryFile(suffix=".pyc", delete=False) as tmp:
            py_compile.compile(str(main_py), cfile=tmp.name, doraise=True)
        check(True, "build/main.py compiles", "")
    except py_compile.PyCompileError:
        check(False, "", "build/main.py FAILS py_compile")

# 4. informational: DONE flag + role coverage
print(f"INFO  build/DONE exists: {(BUILD_DIR / 'DONE').exists()}")
role_dirs = ["code", "lore", "art", "qa", "audio"]
counts = {d: len(list((OUTPUT_DIR / d).glob('*.*'))) if (OUTPUT_DIR / d).exists() else 0 for d in role_dirs}
print(f"INFO  output coverage: {counts}")

print("SMOKE RESULT:", "ALL PASS" if not failures else f"{len(failures)} FAILURE(S)")
sys.exit(1 if failures else 0)
