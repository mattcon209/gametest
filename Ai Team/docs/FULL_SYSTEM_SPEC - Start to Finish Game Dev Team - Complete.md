# FULL SYSTEM SPEC - Autonomous AI Game Dev Team - Idea to Playable Game
## Version: v6 - Complete - Any Language, Any Game Type, No Manual File Nonsense, Minimal GUI

**Date:** July 29, 2026  
**Purpose:** Define EVERY feature for a fully functional engine/game dev team that does `idea > builds > test > edit > compile to complete playable game` for ANY style (2D, 3D, text, GUI, etc.) in ANY language (Python, C++, C#, Lua, GDScript, Rust, JS, etc.) with industry standards, unique file splitting, and minimal GUI — no manual make/delete/edit file nonsense to operate.

**Core Invariant:** `4. GDD.md` is READ ONLY, never modified by system. All control via GUI or one-click batch files, not manual file deletion.

**Hardware:** 32GB RAM, RTX 5060 Ti 16GB (8GB variant via Q3), CPU fallback, 60GB models, offline after pull.

---

### 1. DIRECTORY STRUCTURE - Industry Standard - Automated

```
Ai Team/
  1. Install and Setup.bat           # One-click install, does NOT start team
  2. Start Team.bat                  # Starts team + IS live scrolling log
  3. Live Log Viewer.bat             # Second monitor tail (optional if GUI used)
  4. GDD.md                          # PROMPT FILE - READ ONLY - YOUR fine-tuned idea
  gui.py                             # MINIMAL GUI - Tkinter, offline, no deps - controls everything
  studio.py                          # Orchestrator v6 - language-agnostic, start>finish
  tasks.json                         # File memory - task queue - managed by GUI, not manually
  MEMORY.md                          # Summary memory - managed by system
  INBOX.txt                          # Deprecated - replaced by GUI input, kept for phone remote fallback
  inbox_history.txt                  # History of directives
  logs.txt                           # Full log
  live_status.txt                    # Last line for GUI/phone
  roles/
    aura.txt, forge.txt, spark.txt, lore.txt, pixel.txt, glitch.txt, integrator.txt, audio.txt
  output/                            # Fragments - auto-managed, user never manually deletes
    code/                            # Max 500 lines, 20KB, unique naming (see Section 3)
    lore/
    art/
    qa/
    audio/
  build/                             # FINAL PLAYABLE GAME - auto-generated, self-contained
    main.<ext>                       # Entry point extension matches Language in GDD: .py .cpp .cs .lua .gd .rs .js
    engine/                          # Custom engine core in detected language
    systems/                         # Merged systems
    assets/                          # Art/audio copied
    content/                         # Lore JSON
    run.bat / run.sh                 # Launcher auto-generated for detected language
    README.md
    DONE                             # Written after successful build+test - true finish flag
    test_results.txt
  repo_backup/                       # Preserved original repo (read-only backup)
  docs/
  tools/
```

**Rule:** User never manually `del tasks.json`, `del build/DONE`, `echo [] > tasks.json`, `mkdir output/code`. All via GUI buttons: Pause, Resume, Fresh Start, Force Rebuild, Edit GDD. GUI encapsulates file ops.

---

### 2. INDUSTRY STANDARDS - File Sizes, Lines, No Monoliths, Unique Splitting

**File Size Limits (language-agnostic, based on Google/Airbnb/AAA):**
- Source file max: 500 lines OR 25KB whichever smaller. Applies to .py .cpp .cs .lua .gd .rs .js .hpp
- If exceeds, AURA MUST split (see Unique Splitting below), not allow monolith
- Asset max: Image 2MB, Shader 50KB, Audio 5MB, Model 10MB - auto-compress
- Lore JSON max: 5KB / 100 lines per file - split into chapters

**Line Limits:**
- Max 100 chars per line (80 preferred) for ALL languages - readability + phone editing
- Function max 50 lines - if longer, SPARK/forge must split into helper functions
- Class max 300 lines - if longer, split into components
- Comment ratio min 15% for FORGE engine code, min 10% for gameplay

**Avoiding Monoliths:**
- No God Object: No `GameManager.cs`, `main.god`, `everything.py` doing all systems
- ECS/Component: FORGE must use Entity-Component-System or composition
- Single Responsibility: `output/code/` each file ONE system: Save System OR Tether System, not both
- Dependency: `systems/` may depend on `engine/`, never reverse. `engine/` is engine-only, no game logic.
- Interface Segregation: Shader files no gameplay logic, Lore no code

**UNIQUE SPLITTING - Fixes overwrite/repeat naming (your issue):**
- Problem old: `01_forge_Save_System.py` split into `01_forge_Save_System_Core.py` + `01_forge_Save_System_Utils.py` could overwrite `01_forge_Save_System_Utils.py` from another task with same title.
- Solution v6 - Unique ID + Random Suffix + Split Registry:

```
Original exceeds 500 lines: 07_forge_Save_System.py (620 lines)
AURA must split into:
  07_forge_Save_System_Core_A1B2.py
  07_forge_Save_System_Utils_C3D4.py
  07_forge_Save_System_API_E5F6.py

Where:
- 07 = original task ID (global auto-increment, never reused)
- forge = role
- Save_System = safe_title (sanitized GDD title)
- Core/Utils/API = split part name describing responsibility
- A1B2 = 4-char hex random suffix generated once per split file, guarantees uniqueness even if same title split twice
- tasks.json tracks: {"id":7, "split_into":["07_forge_Save_System_Core_A1B2.py", ...], "original_deprecated":true}

Original file then becomes facade:
07_forge_Save_System.py now contains only:
  from .Save_System_Core_A1B2 import *
  from .Save_System_Utils_C3D4 import *
  # Deprecated facade - split for monolith avoidance

No file is ever overwritten - new files always get new random suffix. If same title appears again, new random suffix ensures different filename.
```

- Global ID counter: `next_id = max(existing IDs in tasks.json + output/ filenames) + 1`, never reuses ID, even after deletion
- Split registry in `MEMORY.md`: `Split 07 -> 07_forge_Save_System_Core_A1B2.py + Utils_C3D4.py`
- Validation: GLITCH checks file size >500 lines = FAIL and requests split with unique suffix
- AURA validation checks imports >5 project files = FAIL monolith risk

**Naming (language-agnostic):**
- `ID_role_SafeTitle_Part_Random.ext` where ext matches Language field in GDD
- Example GDD Language: `C++` -> `01_forge_Save_System_Core_A1B2.cpp` + `.h`
- Example Language: `Lua` -> `01_forge_Save_System_Core_A1B2.lua`
- Example Language: `Python + Lua` -> main.py that embeds Lua via lupa, or separate .py + .lua files - integrator decides based on language list
- No spaces in code filenames, use `_`, GDD can have spaces

---

### 3. LANGUAGE SUPPORT - Any Language Defined in GDD (fixes Python-only)

**GDD Language Field Required:**
```md
LANGUAGE: Python
# OR
LANGUAGE: C++
# OR
LANGUAGE: C# + Lua
# OR
LANGUAGE: GDScript
# OR
LANGUAGE: Rust
# OR
LANGUAGE: Python + C++ + Lua
```

**Detection (v6):**
- `detect_language(gdd_text)` parses LANGUAGE line, fallback to `LANGUAGE: Python` if missing
- Supports: Python, C++, C#, Lua, GDScript, Rust, JavaScript, TypeScript, Java, Go - any string, system respects it
- If multiple languages listed, primary is first, secondary are bindings (e.g., Python main that loads Lua scripts)

**Role Prompts Language-Aware:**
- FORGE system prompt + engine_instruction injected: `Build in LANGUAGE: C++ with SDL/OpenGL - NO Unity C#, NO Python import if GDD says C++`
- Example if GDD says `LANGUAGE: Lua`: FORGE prompt becomes `Build custom engine in Lua with LÖVE2D or Raylib Lua bindings, not Python pygame`
- Example if `LANGUAGE: C++`: extension `.cpp` + `.h`, build system generates `CMakeLists.txt`, entry `main.cpp`, run via `run.bat` that calls `g++` or `cmake`

**File Extensions Mapping:**
- Python -> .py, main.py, run.bat = `python main.py`
- C++ -> .cpp/.h, main.cpp, CMakeLists.txt, run.bat = `cmake --build build && build\game.exe`
- C# -> .cs, main.cs, .csproj, run.bat = `dotnet run`
- Lua -> .lua, main.lua, run.bat = `lua main.lua` or `love .` if LÖVE
- GDScript -> .gd, project.godot, run.bat calls Godot binary if present else fallback
- Rust -> .rs, Cargo.toml, run.bat = `cargo run`
- JS/TS -> .js/.ts, package.json, run.bat = `node main.js`

**Line limits adjusted per language:**
- C++: 500 lines still, but header + source split considered one logical file (e.g., SaveSystem.h + SaveSystem.cpp = one system, but each file <500)
- Lua: 400 lines max (Lua tends to be more compact)

**Build System Language-Aware:**
- Integrator reads LANGUAGE field and generates appropriate entry point and launcher
- `build/` always self-contained with correct extension and launcher for detected language
- Fallback: If LLM fails to produce correct language, `ensure_build_runnable()` creates minimal hello-world in detected language so build is ALWAYS runnable

---

### 4. MINIMAL GUI - Fixes "make this file, delete that file" Nonsense

**Requirement:** User should never need to `echo pause > PAUSE`, `del tasks.json`, `type logs.txt`, `dir output/code` manually to operate. All via GUI.

**gui.py - Tkinter, offline, no deps, built-in Python:**

Features (single window, 800x600):
- Top bar: Shows `4. GDD.md` path, Engine mode (CUSTOM/STANDARD), Language (Python/C++/Lua...), Game Type (2D/3D/Text/GUI)
- Left panel - Controls (buttons, not file ops):
  - Start Team (calls 2. Start Team.bat logic via subprocess)
  - Pause Team (creates PAUSE file via code, not manual echo)
  - Resume Team (deletes PAUSE via code)
  - Fresh Start (backs up output/ to output_backup_, clears tasks.json to [], clears MEMORY.md, deletes build/DONE and build/main.<ext> via code - user clicks one button, no manual del)
  - Force Rebuild (deletes build/DONE + build/main.<ext> and triggers integrator)
  - Edit GDD (opens 4. GDD.md in notepad or internal editor)
  - Open Build Folder (explorer build/)
  - Open Output Folder (explorer output/)
- Center - Live Log: Scrolling text widget tailing logs.txt in real-time (replaces 3. Live Log Viewer.bat)
- Right - Tasks: List from tasks.json with status colors (pending yellow, in_progress blue, done green, failed red)
- Bottom - Build Status: Shows if build/main.<ext> exists, DONE exists, last test result, Run Build button (calls build/run.bat)
- Status bar: live_status.txt content + Ollama ps + nvidia-smi summary

**Implementation:**
- `gui.py` in Ai Team root, run via `python gui.py` or double-click `4. GUI - Minimal Control Panel.bat` (new file to be added)
- Uses only `tkinter` (built-in), `pathlib`, `json`, `subprocess` - no internet, offline
- All file operations encapsulated in functions: `pause_team()` creates PAUSE file, `fresh_start()` does backup + clear, etc.
- No manual `echo > INBOX.txt` - GUI has input box "Send directive to Director" that writes to inbox_history.txt and injects into AURA prompt (GDD untouched)

**Replaces Manual Nonsense:**
- Old: `echo pause > PAUSE` -> New: GUI Pause button
- Old: `del PAUSE` -> GUI Resume button
- Old: `echo [] > tasks.json` + `del build/DONE` -> GUI Fresh Start button
- Old: `type logs.txt` -> GUI Live Log panel auto-scrolls
- Old: `dir output/code` -> GUI Output file list panel
- Old: `notepad 4. GDD.md` -> GUI Edit GDD button

**Batch files still work for phone remote fallback, but GUI is primary for PC use.**

---

### 5. ROLES - Full Diverse Team (8 roles)

1. **AURA - Director / Supervisor / Planner**
   - qwen3:14b Q4, Apache 2.0, reasoning + tool use
   - Reads: GDD (read-only, first 4500 chars), MEMORY.md, tasks.json, output_index, inbox directive (from GUI, not GDD)
   - Outputs: JSON array 3-5 tasks OR [] for finish
   - Must enforce: Role diversity (at least 1 FORGE, 1 SPARK, 1 LORE, 1 PIXEL, 1 GLITCH per cycle if missing in output), Engine respect, Language respect, Dedup, Scope limit max 25 tasks then [], Unique split naming with random suffix

2. **FORGE - Lead Engine / Server / Steam API**
   - devstral:24b Q4, agentic coding
   - Respects Language field - builds in detected language, not always Python
   - If GDD says custom engine, builds from scratch in detected language with SDL/Raylib/OpenGL, no Unity

3. **SPARK - Gameplay Scripter**
   - qwen2.5-coder:14b, FIM
   - Rapid 50-150 line prototypes in detected language

4. **LORE - Narrative Designer**
   - gemma3:12b, multimodal, creative writing
   - Dialogue JSON, quests, personality DB

5. **PIXEL - Tech Artist**
   - gemma3:12b, vision capable
   - Shaders, palette, VFX, reads screenshots

6. **GLITCH - QA / Debugger**
   - deepseek-r1:14b, reasoning
   - Edge cases, monolith check (>500 lines FAIL), import count >5 FAIL, exploits

7. **AUDIO - Audio Designer**
   - gemma3:4b lightweight
   - SFX, music stubs, stress audio feedback

8. **INTEGRATOR - Final Builder**
   - qwen3:14b, merges fragments into build/ in detected language ext, ensures build always runnable fallback, writes DONE

**Role Isolation:** Each worker gets ONLY GDD snippet + its task + its role.txt + engine instruction + language instruction. Never sees other roles. System prompt: `You are FORGE ONLY in LANGUAGE: C++ - Do not do LORE/PIXEL work. Stay scope: Title. GDD read-only.`

---

### 6. CORE ENGINE ARCHITECTURE - Any Game Type, Any Language

**Pluggable Backends - Language Agnostic:**

```
engine/
  core.<ext>         # Window, main loop, delta, pause, quit - in detected language
  input.<ext>        # Keyboard/mouse/gamepad abstract
  renderer.<ext>     # Interface
    renderer_2d.<ext>   # 2D: Pygame, Raylib 2D, SDL
    renderer_3d.<ext>   # 3D: Raylib 3D, Panda3D, PyOpenGL, Godot-style Node3D (your repo), custom 3D with global_transform.distance_to
    renderer_text.<ext> # Text adventure: console print
    renderer_gui.<ext>  # GUI puzzle: Tkinter, Dear PyGui, ImGui
  physics.<ext>
    physics_2d.<ext>    # AABB, tether distance constraint
    physics_3d.<ext>    # Bullet, custom Node3D, apply_central_impulse
  audio_engine.<ext>
```

**Game Type Detection:**
- If GDD contains `3D, Node3D, physics, tether, ragdoll, diving, global_transform` -> 3D + physics_3d + renderer_3d
- If `2D, platformer, fishing, roguelike, sprite` -> 2D + physics_2d + renderer_2d
- If `text based, adventure, dialogue, parser` -> text + renderer_text
- If `GUI only, puzzle, clicker, editor` -> GUI + renderer_gui

**Language Detection:**
- Parse `LANGUAGE:` line in GDD, supports single or multiple like `C++ + Lua` -> main in C++ that embeds Lua via sol2
- If no LANGUAGE line, default `Python` but respect GDD Engine phrase `from scratch` still Python

**Steam & Server Stubs:**
- `systems/steam_api_stub.<ext>` - Init, achievement, stat, cloud save - logs, no SDK needed, in detected language
- `systems/server_stub.<ext>` - start, sync_tether, dedicated server authoritative, TCP/UDP stubs

---

### 7. GDD SPECIFICATION - Read Only, Never Touched, Language Field Required

**4. GDD.md must contain:**

```md
# GAME DESIGN DOCUMENT
PROJECT: Name
GENRE: 2D/3D/Text/GUI - e.g., 3D Tether Physics
ENGINE: Custom from scratch / Unity / Godot / None
LANGUAGE: Python / C++ / C# + Lua / GDScript / Rust / JS (REQUIRED - fixes Python-only)
ELEVATOR PITCH: One sentence
CORE LOOP: 1. ... -> 2. ... -> 3. ...
FEATURES: 5-15 core features, each maps to one role
TECH: Engine, Art Style, Scope: 2 weeks, 1 human + AI team
...
```

**Size Limit:** 10KB / 300 lines max, critical Engine/Language/Core Systems at top (AURA reads first 4500 chars)

**GDD Patch for Start>Finish (optional but recommended):**
- Scope limit: Max 25 tasks then DONE
- Core Systems list: Finite 12 systems, when all exist in output/, output []
- Role diversity: Must include 1 FORGE, 1 SPARK, 1 LORE, 1 PIXEL, 1 GLITCH, 1 AUDIO per cycle
- Finish condition: When core systems exist + DONE → IDLE until GDD mtime changes
- This patch is added to GDD content but system never modifies GDD file itself

---

### 8. TASK MANAGEMENT - Unique Splitting, No Overwrite

**tasks.json - Externalized Brain:**
```json
[
  {"id":1, "role":"forge", "title":"Save System", "prompt":"...", "status":"done", "attempts":1, "output_file":"output/code/01_forge_Save_System_Core_A1B2.py", "split_into":["01_forge_Save_System_Core_A1B2.py","01_forge_Save_System_Utils_C3D4.py"], "original_deprecated":true},
  {"id":2, "role":"spark", "title":"Tether Movement", "status":"pending"}
]
```

**ID:** Global auto-increment `next_id = max(all IDs in tasks.json + output filenames) +1`, never reused, even after deletion

**Unique Splitting (fixes overwrite):**
- If file >500 lines or 25KB, AURA must split into 2-3 files
- New files: `{ID}_{role}_{SafeTitle}_{Part}_{Random4}.{ext}` where Random4 = 4-char hex e.g., A1B2, ensures uniqueness even if same title split twice
- Example: `07_forge_Save_System_Core_A1B2.cpp` + `07_forge_Save_System_Utils_C3D4.cpp` + facade `07_forge_Save_System.cpp` that includes both
- tasks.json tracks `split_into` array, marks original as deprecated
- No file ever overwritten - new files always new random suffix

**Statuses:** pending, in_progress, failed, done
**Attempts:** Max 3, then loop breaker forces done with note

**Dedup:**
- Scan output/ for existing titles, build existing_titles set
- If new task title fuzzy matches existing >70% similarity, skip unless GDD says IMPROVE/REDO/REBUILD
- If output/ emptied but tasks.json still has done tasks, dedup would still skip - GUI Fresh Start button clears both output/ (backup) + tasks.json + MEMORY.md + build/DONE in one click, no manual del

---

### 9. MEMORY AND PERSISTENCE - No Manual File Nonsense

- `MEMORY.md` - Summary, engine mode, language, existing files count - AURA reads each wakeup
- `tasks.json` - Task queue - managed by system/GUI, not manually edited
- `live_status.txt` + `logs.txt` - Displayed in GUI Live Log panel, not via `type logs.txt`
- `inbox_history.txt` - INBOX directives history, GDD never touched
- `output/` - Fragments, auto-managed
- `build/` + `build/DONE` - Final game + finish flag, managed by integrator, GUI shows status
- All survives VRAM unload, PC crash, 8:30am restart

**GUI replaces manual file ops:**
- Old manual: `echo pause > PAUSE`, `del PAUSE`, `echo [] > tasks.json`, `del build/DONE`, `dir output/code` -> New: GUI buttons Pause, Resume, Fresh Start, Force Rebuild, Output file list panel

---

### 10. VALIDATION AND QA

**After each worker, AURA validates:**
- Role lane? Engine respect? Language respect? No haywire? File size <=500 lines? Imports <=5? Random suffix unique?
- PASS -> done, FAIL + attempts<3 -> re-queue with correction, FAIL + attempts>=3 -> loop breaker forced done

**GLITCH checks:** Monolith, import count, edge cases from qa/, stress test, language-specific lint (e.g., C++ compile check if g++ available)

---

### 11. INTEGRATION AND BUILD - Language-Aware, Guaranteed Runnable

**Trigger:** No pending AND (no main.<ext> OR GDD changed after DONE OR no DONE) AND existing_files >=1

**Steps:**
1. Collect code_files = output/code/*.* (max 15 files, 1500 chars each to fit LLM context, regardless of language)
2. Call INTEGRATOR with GDD + code_bundle + engine_mode + language + game_type
3. Parse LLM output for code block in detected language: ```python / ```cpp / ```lua etc -> build/main.<ext>
4. Fallback: `ensure_build_runnable()` creates minimal hello-world in detected language if LLM fails, so build ALWAYS runnable
5. Generate launcher: `run.bat` + `run.sh` with correct command for language (python main.py, g++ main.cpp -o game && game, lua main.lua, dotnet run, etc.)
6. Test: Run `build/run.bat` or `main.<ext>` with 5s timeout, save to `test_results.txt`
7. Write `build/DONE` with timestamp, engine, language, fragment count - true finish
8. IDLE until GDD mtime changes

**Build Self-Contained:** No absolute paths, includes engine/, systems/, assets/, content/, works offline

---

### 12. LOOP PREVENTION AND FINISH GUARANTEE

- Dedup skips existing titles
- Loop breaker skips after 3 fails
- Scope limit max 25 tasks then [] (GDD patch + code cap)
- Core Systems finite list - when all exist, AURA must output [] (cannot invent new)
- DONE file prevents rebuild unless GDD changes
- After DONE, goes IDLE 15s loop checking GDD mtime, not planning new tasks

**True Finish:** tasks.json pending=0 + output has core systems + build/main.<ext> exists + test run + DONE written -> IDLE

---

### 13. LOGGING AND MONITORING - GUI, Not Manual

- 2. Start Team.bat IS live scrolling log (real-time)
- 3. Live Log Viewer.bat optional second monitor tail
- gui.py Live Log panel auto-scrolls logs.txt, no need type logs.txt
- live_status.txt for phone quick check
- GUI shows Ollama ps + nvidia-smi summary

---

### 14. RECOVERY FROM CRASH

- PC crash at 8:30am: Ollama VRAM cleared, but tasks.json, MEMORY.md, output/, build/ remain on disk (file memory)
- On reboot, run 2. Start Team.bat -> starts ollama serve, loads tasks.json, resumes
- v2 gap: No DONE, no build, replanned from scratch - v6 fix: DONE + build preserved, resumes and IDLEs if done

---

### 15. MINIMAL GUI SPEC - Fixes Nonsense Manual File Ops

**gui.py - Tkinter offline, no pip deps:**

Window 800x600, 4 sections:

- Top: GDD path, Engine mode (CUSTOM/STANDARD), Language (Python/C++/Lua...), Game Type (2D/3D/Text/GUI), Build status (DONE exists? main.<ext> exists?)
- Left - Controls (buttons, no manual file commands):
  - Start Team (subprocess 2. Start Team.bat logic)
  - Pause / Resume (creates/deletes PAUSE file via code)
  - Fresh Start (backs up output/ to output_backup_, clears tasks.json to [], clears MEMORY.md, deletes build/DONE + build/main.<ext> via code - one click, no manual del)
  - Force Rebuild (deletes build/DONE + build/main.<ext> and triggers integrator)
  - Edit GDD (opens 4. GDD.md in notepad or internal editor)
  - Open Build Folder / Output Folder (explorer)
  - Send Directive (input box -> writes to inbox_history.txt and injects into AURA prompt, not GDD)
- Center - Live Log: Text widget tailing logs.txt real-time
- Right - Tasks: Listbox from tasks.json with colors, Output Files: Listbox from output/
- Bottom - Build: Shows main.<ext> exists, DONE exists, test_results.txt, Run Build button (calls build/run.bat)

All file ops encapsulated - user never types echo > PAUSE etc.

---

### 16. GAME TYPE DIVERSITY

- detect_game_type(): 3D if Node3D/physics/tether/ragdoll/diving, 2D if platformer/fishing/sprite, text if adventure/dialogue/parser, GUI if puzzle/clicker/editor
- detect_language(): Parses LANGUAGE: line, supports any language, primary first
- Renderer selection: renderer_2d.py (Pygame), renderer_3d.py (Raylib/Panda3D), renderer_text.py, renderer_gui.py (Tkinter/Dear PyGui) - in detected language
- Role adaptation: Text adventure -> SPARK writes parser, PIXEL writes ASCII palette, etc.

---

### 17. FINAL CHECKLIST - Via GUI, Not Manual File Nonsense

- [ ] Copy fixed Ai Team folder to PC, put fine-tuned 4. GDD.md back (overwrite template) - GUI will show GDD path
- [ ] 1. Install and Setup.bat once (or GUI Install button)
- [ ] 2. Start Team.bat or GUI Start Team button - watch live log in GUI center panel, should see FORGE, SPARK, LORE, PIXEL, GLITCH, AUDIO (not just FORGE) after GDD patch
- [ ] After 20-25 tasks, GUI should show Build Status: DONE exists, main.<ext> exists, IDLE
- [ ] GUI Run Build button -> launches game (install pygame/raylib via GUI if needed: button calls pip install)
- [ ] Edit GDD via GUI Edit GDD button to add IMPROVE: ... -> GUI detects mtime change, deletes DONE, rebuilds

No manual del, echo, mkdir, type needed - all via GUI buttons.

---

**END OF SPEC v6 - READY FOR IMPLEMENTATION**
