#!/usr/bin/env python3
"""Post-run regression gate for the Ai Team orchestrator.

Added per Audit 3/4/5 recommendation. These two checks would have caught the
C5 prose-leak (3 audits) and the N1 placeholder-overwrite (2 audits) instantly,
without any manual review:

  1. build/main.py must NOT be the auto-generated fallback placeholder
  2. every generated source fragment in output/ must actually parse

Exit code 0 = healthy, 1 = regression. Safe to run any time; read-only.
"""
import sys, py_compile, tempfile
from pathlib import Path

BASE = Path(__file__).resolve().parent
BUILD = BASE / "build"
OUTPUT = BASE / "output"
fails = []

# --- Gate 1: build is a real game, not the fallback placeholder -------------
mains = [p for p in BUILD.glob("main.*") if p.is_file()]
if not mains:
    fails.append("no build/main.* found - integrator never produced an entry point")
else:
    for m in mains:
        try:
            if "Fallback Build" in m.read_text(encoding="utf-8", errors="ignore"):
                fails.append(f"{m.name} is the fallback PLACEHOLDER, not the LLM's game "
                             "(check integrator extraction gates / ensure_build_runnable st_size)")
        except Exception as e:
            fails.append(f"cannot read {m.name}: {e}")

# --- Gate 2: generated fragments are syntactically valid -------------------
checked = 0
for py in OUTPUT.rglob("*.py"):
    checked += 1
    try:
        with tempfile.NamedTemporaryFile(suffix=".pyc", delete=True) as tmp:
            py_compile.compile(str(py), cfile=tmp.name, doraise=True)
    except py_compile.PyCompileError:
        fails.append(f"{py.relative_to(BASE)} does not parse - raw LLM prose/fences leaked "
                     "(check extract_code_from_response length gates)")
    except Exception as e:
        fails.append(f"{py.relative_to(BASE)} check error: {e}")

print(f"[VERIFY] build entry points: {len(mains)} | python fragments checked: {checked}")
if fails:
    print(f"[VERIFY] {len(fails)} REGRESSION(S):")
    for f in fails:
        print(f"  - {f}")
    sys.exit(1)
print("[VERIFY] PASS - build is a real game and all fragments parse")
sys.exit(0)
