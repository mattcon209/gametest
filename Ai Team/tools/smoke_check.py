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
    except py_compile.PyCompileError:
        failed.append(f.name)
check(not failed, f"output/code fragments compile: {compiled}/{len(code_py)} OK", f"fragments FAIL py_compile: {failed}")

# 2b. LANGUAGE-AGNOSTIC fragment sanity (Audit6 gap fix).
# py_compile only covers Python. On a C++/Lua/GDScript/Rust project the checker
# previously inspected ZERO files and still printed "ALL PASS" - a broken build
# was indistinguishable from a good one. These checks need no toolchain: they
# catch the two regressions that actually recur (raw markdown fences and
# deepseek <think> blocks leaking into source, i.e. C5/F9-class failures).
SRC_EXTS = {".cpp", ".hpp", ".h", ".cs", ".lua", ".gd", ".rs", ".js", ".ts", ".go", ".java", ".shader"}
non_py = sorted(p for p in (OUTPUT_DIR / "code").glob("*.*")
                if p.suffix.lower() in SRC_EXTS) if (OUTPUT_DIR / "code").exists() else []
polluted = []
for f in non_py:
    try:
        t = f.read_text(encoding="utf-8", errors="replace")
    except Exception:
        continue
    if "```" in t or "<think>" in t.lower():
        polluted.append(f.name)
if non_py:
    check(not polluted,
          f"non-Python fragments clean of fences/<think>: {len(non_py) - len(polluted)}/{len(non_py)} OK",
          f"fragments contain raw markdown/<think>: {polluted}")

# 2d. Audit7 gap: .md role output (lore/, qa/) was covered by NO check at all.
# Audit6 added source-extension checks; .md fell through both, so a LORE/GLITCH
# file could carry deepseek <think> reasoning and still report ALL PASS.
# <think> in a deliverable is always a defect. Fenced code inside .md is normal
# markdown, so it is reported as INFO only, not a failure.
md_files = []
for sub in ("lore", "qa", "code", "art", "audio"):
    d = OUTPUT_DIR / sub
    if d.exists():
        md_files.extend(sorted(d.glob("*.md")))
md_think = [f.name for f in md_files
            if "<think>" in f.read_text(encoding="utf-8", errors="replace").lower()]
if md_files:
    check(not md_think,
          f"markdown deliverables free of <think> reasoning: {len(md_files) - len(md_think)}/{len(md_files)} OK",
          f"markdown contains <think> reasoning blocks: {md_think}")
    md_fenced = [f.name for f in md_files
                 if "```" in f.read_text(encoding="utf-8", errors="replace")]
    if md_fenced:
        print(f"INFO  markdown with fenced blocks (normal for .md): {len(md_fenced)}/{len(md_files)}")

# 2c. the build entry point itself must be clean source, whatever the language.
for m in main_candidates:
    try:
        t = m.read_text(encoding="utf-8", errors="replace")
    except Exception:
        continue
    check("```" not in t and "<think>" not in t.lower(),
          f"{m.name} is clean source (no fences/<think>)",
          f"{m.name} contains raw markdown fences or <think> blocks - extraction failed")
    check(len(t.strip()) >= 10,
          f"{m.name} is non-trivial ({len(t.strip())} chars)",
          f"{m.name} is effectively empty ({len(t.strip())} chars)")

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
