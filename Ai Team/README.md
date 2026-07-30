# Ai Team - v6 FINAL - Start to Finish - Any Language, Any Game Type, Minimal GUI

**This folder is now rebuilt to v6 spec - meets all flexibility, structure, industry standards**
**GDD SAFE - 5. GDD.md NEVER modified by system, only read - No manual file nonsense**

## Top Files (Windows sorts to top) - Use GUI, no manual file ops:

1. **1. Install and Setup.bat** - One-click install Ollama + Python + 6 LLMs (~53GB), does NOT start team
2. **2. Start Team.bat** - Starts autonomous team, IS the live scrolling log (real-time)
3. **3. Live Log Viewer.bat** - Second monitor tail (optional, GUI has live log panel)
4. **4. GUI - Minimal Control Panel.bat** - MINIMAL GUI - Tkinter offline, no deps - controls everything without manual file ops
5. **5. GDD.md** - YOUR PROMPT FILE - Fine-tuned game idea - Team watches constantly - READ ONLY, NEVER touched by system

**gui.py** - Minimal GUI: Start/Pause/Resume/Fresh Start/Force Rebuild/Edit GDD/Open Build/Output/Builds Archive/Send Directive/Live Log/Tasks/Output files/Build status/Run Build - replaces echo pause > PAUSE, del tasks.json, type logs.txt, dir output

## Full Pipeline v6 - Guaranteed Start > Finish:

```
IDEA (5. GDD.md READ ONLY, LANGUAGE field, Game Type, Engine)
-> DETECT game type (2D/3D/Text/GUI) + language (Python/C++/C#/Lua/GDScript/Rust/JS) + engine mode (custom/standard)
-> GUI builds per-system asset lists from your Features text (what art/audio/code each system needs) -> system_requirements.json -> studio injects that list into AURA's planning prompt so tasks follow it
-> PLAN missing only (dedup via output/ scan + existing_titles, unique naming with random suffix to avoid overwrite)
-> BUILD each once in parallel where VRAM allows (max 2 models in 16GB VRAM, respects 32GB RAM limit, no crossover)
-> VALIDATE engine respect + language respect + role lane + file size <=500 lines + imports <=5
-> COMPILE to /build/ in detected language (main.py/.cpp/.cs/.lua/.gd/.rs/.js) + run.bat/run.sh + README + DONE
-> TEST (smoke 5s, save to test_results.txt)
-> EXPORT to builds/{Stage}_{timestamp}_{random4}/ before clearing current build (unique folder + manifest, never overwrites)
-> DONE file + IDLE until GDD mtime changes (true finish, not endless FORGE loop)
```

## Fixes for Your Issues:

1. **Unique naming avoids repeat naming/overwrite:**
   {ID}_{role}_{SafeTitle}_{Random4}.{ext} e.g., 07_forge_Save_System_A1B2.py - Random4 = 4-char hex random, guarantees uniqueness even if the same title recurs; global ID counter never reuses. Oversize files (>500 lines / >25KB / >5 imports) are rejected by a real M9 gate and re-queued with a split instruction - AURA can then plan the split as sibling tasks. (The spec's automatic facade-split registry is deliberately NOT built - one file is written per task attempt, so a facade registry would be scaffolding; see 'Review before touching aiteam folder' Parts 7-8.)

2. **Any language, not just Python:**
   GDD LANGUAGE field: C++ + Lua, Python, GDScript etc. detect_language() maps extension and run command, roles respect Language field, build generates correct entry point and launcher, fallback build always in detected language.

3. **Minimal GUI - No direct GDD editing needed:**
   GUI has Project Name, Engine dropdown (Custom from scratch, Unity, Godot, None), Language dropdown (Python, C++, C#, C# + Lua, Lua, GDScript, Rust, JS, TS...), Game Type (2D, 2D Pixel, 3D, 3D Fishing, Text, GUI), Genre, Art Style, Scope, Elevator Pitch, Core Loop, Features - Generate GDD button creates 5. GDD.md focused on pitch/ideas from GUI inputs. New Project button: Generates GDD + AURA makes system asset lists (what each system needs asset-wise) -> system_requirements.json -> follows list to assign tasks. Continue Project button loads existing.

4. **Parallel models:** studio.py dispatches up to 2 tasks simultaneously where VRAM allows (real combos from the VRAM map: gemma3:12b+gemma3:4b=11.1GB, qwen2.5-coder:14b+gemma3:4b=12.1GB, deepseek-r1:14b+gemma3:4b=12.8GB), validated after each batch. Note: FORGE (devstral:24b ~14GB) can never pair within a 15GB budget, so FORGE-first cycles run sequentially - that is physics, not a bug.

5. **Industry standards:**
   File max 500 lines / 25KB, line max 100 chars (80 pref), function 50 lines, class 300 lines, 15% comments, no monoliths ECS/component/single responsibility, unique naming with random suffix, build self-contained.

6. **Build Pipeline MVP > Alpha > Beta + Export + Game Type Alignment:**
   See docs/BUILD_PIPELINE - MVP Alpha Beta - Export System.md - MVP complete core loop + onboarding + 2-3 sessions + analytics + monetization, Alpha Feature Complete, Beta Content Complete 99.5% crash-free, Export unique folder Random4 before clearing.

7. **Anti-infinite loop 41 measures:**
   See docs/SAFEGUARDS - finite core systems list, max 25 tasks then [], dedup, loop breaker after 3 fails, DONE file true finish, IDLE until GDD change, fallback build, GDD safe, GUI replaces manual ops, etc.

## Fresh Start (Via GUI, no manual file ops):

1. Copy this fixed folder to PC, put your fine-tuned 5. GDD.md back if needed - system NEVER modifies it
2. Double-click 4. GUI - Minimal Control Panel.bat
3. Fill Engine, Language, Game Type, Genre, Pitch, Loop, Features -> Click Generate GDD from GUI Inputs -> Click New Project (AURA makes system asset lists -> system_requirements.json) -> Click Start Team
4. Watch Live Log panel - should see diverse roles: FORGE, SPARK, LORE, PIXEL, GLITCH, AUDIO with parallel batches (max 2 models)
5. After 20-25 tasks, Build Status shows DONE exists, main.<ext> exists, IDLE - true finish
6. Click Run Build button

No manual del, echo, mkdir, type needed - all via GUI.
