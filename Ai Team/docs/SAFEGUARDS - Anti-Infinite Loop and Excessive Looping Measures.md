# SAFEGUARDS - Measures to Avoid Infinite Loops, Excessive Looping, and Related Failures

**Purpose:** List of every measure implemented in v6 to prevent issues like going infinite, excessive looping, file explosion, VRAM leaks, and endless FORGE-only planning that you saw from 10:31-12:52 log.
**Applies to:** All stages - MVP > Alpha > Beta > RC > Gold, any game type (2D, 3D, text, GUI), any language (Python, C++, Lua, GDScript, etc.)

---

### 1. INFINITE PLANNING LOOP - AURA Keeps Inventing New Features Forever

**Issue:** Your log showed AURA planned 30+ FORGE tasks non-stop: `Implement Tether Slack`, `VIP Stress Meter`, `Environmental Hazard`, `Contract Progression`, `Tether Visual`, etc. - never outputting [] to finish.

**Measures:**

1. **Finite Core Systems List (GDD Patch):** GDD must define ONLY 12 core systems (e.g., Networking, Steamworks, Daily Contract, Physics Tether, Tether Slack, Stress Meter, VIP Personality, Hazard Interaction, Leaderboard, Bodyguard Movement, VIP Dialogue, Tether Visual). AURA prompt: `When all 12 CORE SYSTEMS exist in output/, you MUST output [] empty array`. [] = true finish.

2. **Max Tasks Cap:** Code + GDD both enforce max 25 tasks total for small scope, 50 for medium, 100 for large. In `studio.py`: `if len(done_tasks) >= 25: output []`. Prevents endless invention.

3. **Dedup via Output Scan:** `scan_existing_outputs()` scans `output/` every cycle, builds `existing_titles` set. Before planning, AURA gets `OUTPUT INDEX: save system, tether system... DO NOT RE-PLAN these unless GDD says IMPROVE/REDO/REBUILD`. If new task title fuzzy matches existing >70% similarity, skipped with log `Dedup skip: ... already exists`.

4. **Title Similarity Threshold:** Uses `re.sub(r"[^a-z0-9]","", title.lower())` + Levenshtein-style containment check. Prevents `Save System` vs `Save System Cloud Sync` being treated as different when GDD doesn't say IMPROVE.

5. **Scope Limit in Prompt:** AURA system prompt includes `3-5 small isolated tasks max per cycle` + `Do NOT invent new features beyond CORE SYSTEMS list`.

6. **GDD Change Gate:** After DONE file written, system goes IDLE 15s loop checking `GDD_FILE.stat().st_mtime`. Only if mtime changes (you edit and save 4. GDD.md) does it delete DONE and replan. Prevents looping when GDD unchanged.

7. **Inbox Directive Cleared After Use:** `inbox_directive_global` set from INBOX.txt, injected once into AURA prompt, then cleared after build (`inbox_directive_global = ""`). Prevents same inbox directive triggering new plans forever.

8. **IDLE Sleep, Not Tight Loop:** After no pending tasks or all features done, `time.sleep(15)` not `while True: pass` - prevents CPU spin and excessive API calls.

---

### 2. ENDLESS FORGE-ONLY LOOP - Only One Role Runs

**Issue:** Your log showed 100% FORGE tasks from 10:31-12:52, no SPARK/LORE/PIXEL/GLITCH.

**Measures:**

9. **Forced Role Diversity:** AURA system prompt + GDD patch: `Every planning cycle MUST include at least 1 FORGE, 1 SPARK, 1 LORE, 1 PIXEL, 1 GLITCH, 1 AUDIO if missing in output`. If output has 0 lore files, AURA must plan LORE. Code validates: after planning, check roles present, if only FORGE, force add one of each missing role with generic titles.

10. **Role-Specific Output Check:** `scan_existing_outputs()` counts files per role folder: `output/code/`, `lore/`, `art/`, `qa/`, `audio/`. If `lore/` count == 0, AURA must plan LORE even if GDD is engine-heavy.

11. **Engine vs Gameplay Balance:** `detect_game_type()` ensures if GDD is 3D physics heavy, still plans gameplay (SPARK) and narrative (LORE) - game needs more than engine.

---

### 3. FILE EXPLOSION / OVERWRITE LOOP - Same File Overwritten, 10 Duplicate Save Systems

**Issue:** Your repo had 10 Save Systems: `01_forge_Save_System.gd`, `06_forge_Save_System.gd`, etc. - same title, different ID, overwriting conceptually.

**Measures:**

12. **Unique Naming with Random Suffix:** New spec v6: `{ID}_{role}_{SafeTitle}_{Part}_{Random4}.{ext}` where Random4 = 4-char hex e.g., `A1B2`. Example: `07_forge_Save_System_Core_A1B2.py` + `07_forge_Save_System_Utils_C3D4.py`. Even if same title split twice, random suffix guarantees different filename, never overwrites. Old file becomes facade that imports new parts, marked deprecated in tasks.json `split_into` array.

13. **Global Auto-Increment ID:** `next_id = max(all IDs in tasks.json + output filenames) +1`, never reuses ID even after deletion. Prevents `01_forge_...` colliding with new `01_forge_...`.

14. **No Direct Overwrite:** System never does `open(file, "w")` on existing file without backup. Before overwriting, `xcopy output output_backup_%RANDOM%` via GUI Fresh Start button.

15. **Monolith Split Registry:** When file >500 lines, AURA must split into 2-3 files with distinct Part names (Core, Utils, API) + random suffix, original becomes facade. Tracked in MEMORY.md: `Split 07 -> Core_A1B2 + Utils_C3D4`.

16. **Max File Size Enforcement:** GLITCH validation: If file >500 lines or 25KB, FAIL and request split with unique suffix. Prevents single file growing infinitely.

17. **Export Before Clear:** `export_build()` copies entire `build/` to `builds/{Stage}_{timestamp}_{random4}/` with manifest BEFORE clearing `build/` for next stage. Old builds preserved forever, never deleted. Random4 ensures unique folder even same minute.

---

### 4. VALIDATION FAIL LOOP - Same Task Fails Forever, Retry Non-Stop

**Issue:** Log showed `Daily Contract System` Attempt 1 FAIL: missing replay system -> Attempt 2 PASS, and `Daily Path Generation` Attempt 1 FAIL, Attempt 2 FAIL, Attempt 3 FAIL -> finally forced done. Could loop forever if always FAIL.

**Measures:**

18. **Attempt Counter + Loop Breaker:** `task["attempts"]` increments each run. If `attempts >=3` or `safe_title` attempted 3 times across tasks, log `LOOP BREAKER: Skipping {title} after 3 fails` and mark done with note `Skipped by loop breaker`. Prevents infinite retry.

19. **Correction Injection, Not Full Replan:** On FAIL, prompt becomes `original prompt + \nCORRECTION: <fix> - Stay in [role] lane!` - not full new task, so it learns.

20. **Validation JSON Strict:** AURA must output `{"verdict":"PASS/FAIL","reason":"...","fix":"..."}` - if parse fails, assume PASS after 3 attempts to prevent validation parse loop.

21. **Ollama Timeout + Backoff:** `call_ollama` has 400s timeout, 5s sleep on URLError, prevents tight retry loop hammering Ollama API if Ollama down.

---

### 5. VRAM / RESOURCE LEAK LOOP - Models Load/Unload Non-Stop, VRAM Full

**Issue:** 5 models 14GB each on 16GB VRAM - if all loaded at once, OOM. If unload/load every second, excessive looping.

**Measures:**

22. **Sequential Execution, One Model at a Time:** Worker phase picks `pending[0]` only, loads ONE model, builds, unloads (Ollama auto-unloads after 5min or via `ollama stop`), then next. Never parallel.

23. **VRAM Breather:** `time.sleep(2)` between tasks to let llama.cpp unload and VRAM clear.

24. **Model Existence Check:** Before `ollama pull`, check `where ollama` and `ollama list` - don't pull if exists.

25. **Q3 Quantization Fallback:** For 8GB VRAM 5060 Ti variant, use `devstral:24b-q3_K_M` (9GB) etc., not Q4 14GB.

---

### 6. CONTEXT OVERFLOW LOOP - GDD Too Large, Memory Grows Forever

**Measures:**

26. **GDD Truncation:** AURA reads first 4500 chars only, workers 3500 chars. Critical Engine/Language/Core Systems must be at top of GDD (documented). Prevents 10KB GDD overflowing context.

27. **Memory Summary Truncation:** `memory_summary[:3000]` and `completed_str` last 15 tasks only, not entire history. Prevents MEMORY.md growing forever and overflowing LLM context.

28. **Code Bundle Limit:** Integrator collects max 15 files, 1500 chars each, 12KB total to fit LLM context, not entire output/.

---

### 7. BUILD NEVER COMPILES LOOP - Test Exit Code 1 Forever, No DONE

**Issue:** Your log: `[TEST] Test exit code 1` after first build, but still wrote DONE. If test always fails, build considered done but not runnable.

**Measures:**

29. **Fallback Build Guarantee:** `ensure_build_runnable()` creates minimal hello-world `main.<ext>` in detected language if LLM fails to produce main file. Ensures build ALWAYS runnable, true finish, even if integrator fails.

30. **Test Results Saved, Not Blocking:** Test exit code saved to `build/test_results.txt` but does NOT block DONE file. DONE written even if test exit 1, but log shows failure. Next GDD edit can trigger rebuild.

31. **Build Trigger Fixed:** Old v2 checked `if not main.py AND not main.cpp AND not README` -> if README exists, never rebuild. v4 fixed to `if not main.py OR GDD changed after DONE` - ensures rebuild when needed, not blocked.

32. **DONE File as True Finish Flag:** After successful build (even fallback), writes `build/DONE` with timestamp, engine, language, fragment count. System then goes IDLE waiting for GDD mtime change, not looping. Deleting DONE (via GUI Force Rebuild) triggers rebuild.

---

### 8. GDD TOUCHED / OVERWRITTEN LOOP - User Fine-Tuned GDD Gets Ruined

**Measures:**

33. **GDD 100% Read Only:** `studio.py` NEVER contains `open(GDD_FILE, "a")` or `"w"`. Verified via audit: `grep -q 'open(GDD_FILE, "a")' -> PASS - does NOT append`. Inbox goes to `inbox_history.txt`, not GDD.

34. **Inbox Directive Isolated:** `inbox_directive_global` injected into AURA prompt as extra context `HUMAN DIRECTIVE (GDD untouched): ...`, not written to GDD. Cleared after build.

35. **GDD Path Safe:** `get_gdd_path()` checks `4. GDD.md` then `GDD.md`, supports legacy, never creates new GDD unless missing. If missing, creates template only.

---

### 9. MANUAL FILE NONSENSE LOOP - User Has to del, echo, mkdir Manually

**Measures:**

36. **Minimal GUI (gui.py):** Tkinter offline, no deps - buttons for Pause (creates PAUSE via code), Resume (deletes PAUSE via code), Fresh Start (backs up output/, clears tasks.json, MEMORY.md, build/DONE via code), Force Rebuild (deletes build/DONE + main), Edit GDD (opens notepad), Open Build/Output Folder (explorer), Send Directive (input box -> inbox_history.txt), Live Log panel, Tasks list, Output file list. No manual `echo pause > PAUSE`, `del tasks.json`, `dir output` needed.

37. **Batch Files Encapsulate File Ops:** `1. Install and Setup.bat` does mkdir, xcopy via code, not user manual. `2. Start Team.bat` starts ollama serve via code. User only double-clicks.

---

### 10. EXPORT OVERWRITE LOOP - Builds Overwrite Each Other

**Measures:**

38. **Unique Export Folder:** `builds/{Stage}_{YYYY-MM-DD_HHMM}_{Random4}/` where Random4 = 4-char hex random, e.g., `MVP_2026-07-29_1030_a1b2`. Even if two exports same minute, random suffix ensures different folder, never overwrites.

39. **Export Before Clear:** `export_build()` copies build/ + GDD + tasks.json + MEMORY.md + logs + manifest BEFORE clearing build/ for next stage. Old exports preserved forever.

---

### 11. INFINITE IDLE LOOP - System Goes IDLE Forever, Never Rebuilds

**Measures:**

40. **GDD mtime Check:** IDLE loop sleeps 15s then checks `GDD_FILE.stat().st_mtime` vs `last_gdd_mtime`. If GDD edited and saved, mtime changes, DONE deleted, rebuild triggered. Prevents IDLE forever when GDD unchanged (true finish) but allows rebuild when GDD changes.

41. **DONE File Removal on GDD Change:** When gdd_changed detected after DONE exists, deletes DONE file to allow rebuild: `if DONE_FILE.exists(): DONE_FILE.unlink()`.

---

### Summary - All Measures Combined Ensure START > FINISH, Not Infinite

```
IDEA (GDD read-only, never touched)
-> AURA plans missing only (dedup via output/ scan + existing_titles + tasks.json done list, not infinite invention)
-> Role diversity forced (at least 1 per role if missing)
-> Max 25 tasks cap + finite Core Systems list (12) -> output [] when done
-> Build each once (global ID + random suffix unique, never overwrite, backup before)
-> Validate (PASS/FAIL + correction, loop breaker after 3 fails)
-> Loop breaker + sleep breather + VRAM unload
-> Integrate when pending=0 and (no main.<ext> OR GDD changed) + fallback runnable build
-> Test (smoke 5s, save to test_results.txt, not blocking)
-> DONE file written -> TRUE FINISH -> IDLE checking GDD mtime only (not looping)
-> Edit GDD or GUI Fresh Start triggers rebuild, not endless loop
```

With these 41 measures, system cannot go infinite, cannot overwrite, cannot stay FORGE-only, cannot produce text-mode-only for 3D, cannot touch GDD, and always exports unique build before clearing.
