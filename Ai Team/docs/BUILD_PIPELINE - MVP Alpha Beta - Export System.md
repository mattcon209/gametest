# BUILD PIPELINE - Industry Standard MVP > Alpha > Beta > RC > Gold - Export System

**Date:** July 29, 2026
**Source:** Industry standard from AAA, indie, mobile pipelines (Concept > Prototype > Vertical Slice > MVP > Alpha > Beta > RC > Gold) [1](https://videogamedevelopmentauthority.com/game-development-production-pipeline) [2](https://game-ace.com/blog/game-development-stages/)
**Purpose:** Define build requirements for each stage, export system that saves build to unique folder before clearing, and game-type alignment (3D fishing vs 2D pixel)

---

### 1. INDUSTRY STANDARD PIPELINE - MVP > ALPHA > BETA etc.

From industry references, standard pipeline is [1][2]:

```
Concept / Ideation (1-4 weeks) -> 
Pre-Production: Prototype + Vertical Slice (2-6 months) -> 
Production: MVP (6-14 weeks) [1] -> 
Alpha = Feature Complete (all features in, rough) [2][3] -> 
Beta = Content Complete (all assets final, bug fixing) [4][5] ->
Release Candidate (RC) = All bugs fixed or acceptable, 99.5% crash-free [6] ->
Gold Master = Final build for manufacturing/store submission ->
Post-Launch Live Ops
```

**Definitions per industry:**

- **Prototype:** Internal tool to answer "can we build this?" Rough, incomplete, team-only [1]
- **Vertical Slice:** One slice of game at target quality bar - represents all key pieces but one level [2]
- **MVP (Minimum Viable Product):** Functional, playable product for limited external audience to answer "does this work as a game?" Must include complete core loop with beginning/middle/resolution, onboarding that works without explanation, enough content for 2-3 return sessions, basic analytics, at least one monetization intent moment [1][2]
- **Alpha:** Feature Complete - all intended features exist in some form, even if buggy. All levels blocked out, audio placeholder, first-party SDK integration complete, automated test suite operational. Playable from start to finish, unpolished [3][4][5]
- **Beta:** Content Complete - all assets, levels, systems final, art/audio final, localization locked, bug-fixing primary work, crash-free 99.5% target [4][5][6]
- **RC (Release Candidate):** All bugs fixed or considered acceptable, heavily tested, submitted for certification (Sony/Microsoft/Nintendo/App Store) [5][6]
- **Gold Master:** Final approved build for manufacturing/distribution

---

### 2. BUILD REQUIREMENTS PER STAGE - What Must Be Included

#### Stage 0: Concept (Not a playable build - folder: builds/Concept_*)
- **Required:** High-concept doc (1 page), GDD v0.1, platform/genre target, team size estimate
- **Code:** None
- **Art:** Concept art 1-2 images
- **Max File Size:** GDD 2KB, art 2MB
- **Exit Criteria:** Core experience statement documented

#### Stage 1: Prototype (Internal, answers "can we build this?")
- **Required:**
  - One main mechanic working (e.g., tether distance, fishing cast)
  - Basic controls, no win/lose needed, placeholder art (colored boxes)
  - No save, no audio, no menu
- **Max Lines:** 1 file, 200 lines max, 10KB
- **Build:** `build/main.<ext>` + `run.bat` that launches prototype - no assets folder needed
- **Game Type Alignment:**
  - 3D fishing: One fishing rod cast + tension line, no fish, no water shader
  - 2D pixel: One sprite moving, no sprite sheet yet, colored rectangle OK
  - Text: Parser that understands `go north`, `look`
  - GUI: One window with one button that does something
- **Exit Criteria:** Mechanic feels possible, team says yes/no

#### Stage 2: Vertical Slice (Target Quality Bar)
- **Required:**
  - One complete level/slice at final quality bar for art + code
  - Core loop beginning/middle/end for that slice (e.g., cast -> bite -> catch -> sell for one fish)
  - One art style finalized (e.g., pixel art 16x16 or low-poly 3D)
  - One sound effect, one music loop
  - Basic UI for that slice (score, tension meter)
- **Max:** 3-5 files, each <500 lines / 25KB, total build <50MB
- **Build:** `build/` with `engine/`, `systems/tether.py`, `assets/slice/`, `main.<ext>`
- **Game Type Alignment:**
  - 3D fishing: One 3D fish model (low-poly <5K tris) + water plane + tether line visual + one fish type
  - 2D pixel: One sprite sheet (4 frames walk, 2 frames idle) + tilemap 10x10 + stress meter UI overlay shader
  - Text: One room with 10 objects, save/load for that room
  - GUI: Main menu + one puzzle screen + win condition
- **Exit Criteria:** Looks like final game but only one slice, approved by director

#### Stage 3: MVP - Minimum Viable Product (Answers "does this work as a game?")
Industry min for MVP [1][2]:
- Complete playable core loop with beginning/middle/resolution
- Functional onboarding that works without explanation (tutorial)
- Enough content for 2-3 return sessions
- Basic analytics (session length, retention)
- At least one monetization intent moment (if applicable)
- One win/lose/completion state
- Stable build

**MVP Build Requirements:**
- Code: Core loop 100% working, 5-10 systems, each file <500 lines, total <200KB code
  - Required systems: Save System (local JSON), Core Mechanic (Tether OR Fishing Cast), Contract/Quest System (1-2 contracts), Stress/Progress Meter, Input, Main Loop
  - Optional: Cloud save, leaderboard, multiplayer (NO for MVP)
- Art: 
  - 3D fishing: 1-2 fish models (each <10K tris, <2MB), 1 water shader (50KB max), 1 boat, 1 character, 1 biome - total art <20MB
  - 2D pixel: 1 sprite sheet per character (4 walk + 2 idle + 1 action, 128x128 each, <500KB total), 1 tileset 256x256, 1 UI sheet
  - Text: 3 rooms, 20 objects, 30 dialogue lines, save system
  - GUI: 3 screens (menu, game, win), 10 UI elements
- Audio: 2 SFX (action + feedback), 1 music loop <5MB, 44.1kHz
- Lore: 5-10 dialogue lines, 1 contract narrative
- Performance: 60 FPS target on RTX 5060 Ti, 30 FPS min on 8GB, <2s load time, crash-free 95%
- Build: `build/` self-contained, `main.<ext>`, `engine/`, `systems/`, `assets/`, `run.bat`, `README.md`, `test_results.txt`
- Max Build Size: <100MB
- Exit Criteria: External playtesters can play 2-3 sessions without dev help, D1 retention >20% (industry)

#### Stage 4: Alpha - Feature Complete (All features in, rough) [3][4][5]
Industry: All features implemented in any state, all levels blocked out, audio placeholder, SDK integration complete, automated test suite operational [3]

**Alpha Build Requirements:**
- Code: ALL features from GDD implemented, even if buggy. 15-30 files, each <500 lines, total <500KB
  - Must include: Save (local + cloud sync stub), All core mechanics (Tether Slack & Tension, VIP Stress & Panic, Personality, Hazard Interaction, Diving, Contract Progression, Leaderboard), Networking & Server Authoritative stub, Steam API stub (achievements, cloud), Input, Main Loop, Audio engine
  - No new features after Alpha - feature freeze
- Art: All levels blocked out with graybox or placeholder art, art style guide locked
  - 3D fishing: All fish types blocked as capsules or low-poly placeholders (5-10 types), 3 biomes grayboxed, water shader placeholder, boat + character placeholder, stress meter UI graybox
  - 2D pixel: All sprite sheets blocked - colored boxes OK for missing, but all animations listed, all tilesets grayboxed
  - Text: All rooms blocked (10-20 rooms), all objects listed, parser handles all verbs
  - GUI: All screens blocked, wireframes OK
- Audio: All SFX placeholder (at least silent files with correct names), 1 music per biome placeholder
- Lore: All contracts/narrative blocked, dialogue placeholder OK
- Performance: 60 FPS target, <5s load, crash-free 90%, memory <1GB
- Build: `build/` + `build/DONE` NOT yet (Alpha not true finish), `test_results.txt` with functional tests
- Max Build Size: <300MB
- Exit Criteria: Playable from start to finish, even if rough, all features present

#### Stage 5: Beta - Content Complete (All assets final, bug fixing) [4][5][6]
Industry: Content-complete, all assets final, art/audio final, localization locked, bug-fixing primary, crash-free 99.5% [6]

**Beta Build Requirements:**
- Code: No new features, only bug fixes. All files <500 lines, total <600KB, 15% comments min
  - All systems polished: Tether Slack Physics Optimization, VIP Pathfinding AI, Hazard-Contract Synergy, Server Sync, Steam Cloud Save Failover, etc.
  - No `TODO`, `FIXME`, `PLACEHOLDER` in code
- Art: FINAL art, no placeholders
  - 3D fishing: All fish models final (each <10K tris, <2MB, LODs), water shader final (50KB), all biomes final, PBR materials, 4K textures compressed to 2K max, total art <200MB
  - 2D pixel: All sprite sheets final (16x16 or 32x32, all frames), all tilesets final, all UI final with animations, total art <50MB
  - Text: All rooms final, all dialogue final, save system final
  - GUI: All screens final, animations, transitions
- Audio: FINAL SFX + music, 44.1kHz, <5MB each, total audio <50MB, Wwise/FMOD integration if needed
- Lore: All dialogue final, personality database final, contract narrative final
- Performance: 60 FPS locked on RTX 5060 Ti, 60 FPS on 8GB variant, load <2s, memory <2GB, crash-free 99.5%
- Build: `build/` with `main.<ext>`, `engine/`, `systems/`, `assets/final/`, `content/final/`, `run.bat`, `README.md`, `DONE` written after test, `test_results.txt` 99.5% pass
- Max Build Size: <500MB (2D) / <1GB (3D)
- Exit Criteria: External beta testers (100s-1000s) can play full game, no blocking bugs, ready for certification

#### Stage 6: Release Candidate (RC)
- No new content, no new features, only critical bug fixes
- All assets locked, audio lock, art lock, animation lock (no changes except major bugs)
- Performance: 99.9% crash-free, passes platform certification (Sony/Microsoft/Nintendo/App Store)
- Build: `builds/RC_YYYY-MM-DD_HHMM/` exported, versioned, includes symbols for debugging

#### Stage 7: Gold Master
- Final approved build for manufacturing/store submission
- No changes except certification-required fixes
- Build: `builds/Gold_YYYY-MM-DD/` + `GoldMaster.zip` self-contained

---

### 3. EXPORT SYSTEM - Unique Folder Before Clearing Build

**Requirement:** Before clearing current `build/` for next stage, export current build to unique versioned folder.

**Implementation (automated, no manual file ops - via GUI button or studio.py):**

```python
def export_build(stage_name):
    # stage_name = MVP, Alpha, Beta, RC, Gold, etc.
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    # Unique folder: builds/MVP_2026-07-29_1030_a1b2/
    random_suffix = hex(random.randint(0, 0xFFFF))[2:].zfill(4)
    export_path = BASE / "builds" / f"{stage_name}_{timestamp}_{random_suffix}"
    export_path.mkdir(parents=True, exist_ok=True)
    
    # Copy entire build/ (excluding __pycache__ and save files)
    shutil.copytree(BUILD_DIR, export_path / "build", dirs_exist_ok=True, ignore=shutil.ignore_patterns('__pycache__', '*.pyc', 'save_file.json'))
    
    # Copy metadata: GDD, tasks.json, MEMORY.md, logs.txt, test_results
    shutil.copy(GDD_FILE, export_path / f"GDD_{stage_name}.md")
    shutil.copy(TASKS_FILE, export_path / f"tasks_{stage_name}.json")
    shutil.copy(MEMORY_FILE, export_path / f"MEMORY_{stage_name}.md")
    shutil.copy(LOG_FILE, export_path / f"logs_{stage_name}.txt")
    
    # Write export manifest with build requirements checklist
    manifest = {
        "stage": stage_name,
        "timestamp": timestamp,
        "engine": detect_engine_mode(read_file(GDD_FILE))[0],
        "language": detect_language(read_file(GDD_FILE)),
        "game_type": detect_game_type(read_file(GDD_FILE)),
        "build_requirements_met": checklist_for_stage(stage_name),
        "file_count": len(list(export_path.rglob("*"))),
        "build_size_mb": sum(f.stat().st_size for f in export_path.rglob("*") if f.is_file()) / 1024 / 1024,
        "performance": {"crash_free": "99.5% for Beta", "fps_target": "60"},
        "gdd_safe": True
    }
    (export_path / f"EXPORT_MANIFEST_{stage_name}.json").write_text(json.dumps(manifest, indent=2))
    
    # Now safe to clear build/ for next stage (via GUI Fresh Start or auto on next stage trigger)
    # build/ will be rebuilt by integrator for next stage
    return export_path
```

**GUI Buttons:**
- `Export MVP Build` -> Calls export_build("MVP") -> creates `builds/MVP_2026-07-29_1030_a1b2/build/` + manifest, then clears `build/` for Alpha work
- `Export Alpha`, `Export Beta`, `Export RC`, `Export Gold` similarly
- `Open Builds Folder` button

**Unique Folder Naming:**
- `{Stage}_{YYYY-MM-DD_HHMM}_{Random4}` e.g., `MVP_2026-07-29_1030_a1b2`, `Alpha_2026-07-30_0200_c3d4`, `Beta_2026-07-31_1800_e5f6`
- Random4 hex ensures uniqueness even if two exports same minute (fixes overwrite bug you found)
- No file ever overwritten - new export always new folder

**Before Clearing Current Build:**
- Export system copies build/ first, then and only then clears build/ for next stage
- Old builds preserved in `builds/` forever, never deleted
- User never manually `rmdir /S /Q build` - GUI does it after export

---

### 4. GAME TYPE ALIGNMENT - Build Requirements Per Game Type

**System must detect game type from GDD and adjust build requirements:**

**Detection:**
- `detect_game_type(gdd_text)`:
  - If contains `3D, Node3D, physics, tether, ragdoll, diving, global_transform.origin.distance_to, apply_central_impulse, mesh, model, 3D fishing` -> 3D
  - If `2D, pixel, sprite, sprite sheet, platformer, tilemap, 2D fishing` -> 2D
  - If `text based, text adventure, parser, dialogue, room, inventory text` -> Text
  - If `GUI only, puzzle, clicker, editor, window, button` -> GUI
  - If `fishing` alone -> check 2D vs 3D keywords to decide

**Build Requirements Aligned:**

| Game Type | MVP Focus | Alpha Focus | Beta Focus | Max Build Size |
|-----------|-----------|-------------|------------|----------------|
| **3D Fishing** | 1 fish model low-poly <10K tris, 1 water plane shader 50KB, tether line visual, cast mechanic | All fish types grayboxed capsules, 3 biomes grayboxed, boat/character placeholder, water shader placeholder, stress UI graybox | All fish final <10K tris each + LODs, PBR materials, 4K->2K compressed, water final, total art <200MB, 60 FPS | <1GB |
| **2D Pixel** | 1 sprite sheet 4 walk +2 idle 128x128 <500KB, tilemap 10x10, stress UI overlay shader | All sprite sheets blocked (colored boxes OK), all tilesets grayboxed, all UI wireframes | All sprite sheets final 16x16/32x32, all frames, all tilesets final, UI final with animations, total art <50MB, 60 FPS | <500MB |
| **Text Adventure** | 3 rooms, 20 objects, parser `go north`, save/load 1 room, 1 win/lose | All rooms blocked 10-20 rooms, all objects listed, parser all verbs | All rooms final, all dialogue final (30-100 lines), save final, total <5MB | <10MB |
| **GUI Puzzle** | 3 screens (menu, game, win), 10 UI elements, one puzzle mechanic | All screens blocked wireframes, all puzzles listed | All screens final with animations, transitions, total <50MB | <100MB |

**Example:** If GDD says `Make a 3D fishing game`, system knows it needs 3D models (fish, boat, water) vs 2D pixel where focus is sprite sheets. It will NOT request sprite sheets for 3D fishing, and will NOT request 3D models for 2D pixel. This is enforced in AURA planning prompt: `Game Type: 3D Fishing -> Required Art: fish model <10K tris, water shader, NOT sprite sheet`

---

### 5. INDUSTRY STANDARD PRACTICES - Integrated

- **File Size & Line Limits:** As Section 4 in FULL_SYSTEM_SPEC v6 - 500 lines/25KB max, 100 chars line, function 50 lines, class 300 lines, 15% comments
- **No Monoliths:** ECS/component, single responsibility, dependency engine->systems only, interface segregation
- **Unique Splitting:** ID_role_Title_Part_Random4.ext with random hex suffix, never overwrites (fixes your issue)
- **Language Support:** Any language via LANGUAGE field, extension mapping, launcher auto-generation (fixes Python-only)
- **Minimal GUI:** Tkinter gui.py with buttons for Pause, Resume, Fresh Start, Force Rebuild, Edit GDD, Open Build/Output, Send Directive, Live Log panel - no manual `echo pause > PAUSE` etc.
- **GDD Safe:** Never writes to 4. GDD.md, only reads, inbox goes to inbox_history.txt
- **Dedup + Loop Breaker + DONE file:** Prevents endless FORGE loop and infinite new files
- **Fallback Build:** `ensure_build_runnable()` guarantees build/main.<ext> always exists even if LLM fails
- **Test Step:** After each build, runs smoke test 5s, saves to test_results.txt, checks crash-free target per stage (95% MVP, 90% Alpha, 99.5% Beta)
- **Export System:** Unique folder per stage before clearing build, with manifest, never overwrites

---

### 6. EXPORT SYSTEM DOCUMENT - Requirements to Build at Each Stage

**This file is that document - defines requirements per stage and how export works.**

**Before Clearing Build:**
1. GUI button `Export [Stage]` or studio.py auto-exports when stage complete
2. `export_build(stage_name)` creates `builds/{Stage}_{timestamp}_{random4}/`
3. Copies `build/` + GDD + tasks.json + MEMORY.md + logs.txt
4. Writes `EXPORT_MANIFEST_{Stage}.json` with checklist of requirements met for that stage (see Section 2)
5. Then and only then clears `build/` for next stage (GUI does `shutil.rmtree(build/)` + `mkdir build` via code, not manual del)
6. Old exports preserved forever in `builds/`

**Manifest Example for 3D Fishing MVP:**
```json
{
  "stage": "MVP",
  "timestamp": "2026-07-29_1030",
  "engine": "custom",
  "language": "Python",
  "game_type": "3D Fishing",
  "build_requirements_met": {
    "core_loop": true,
    "onboarding": true,
    "content_2_3_sessions": true,
    "analytics": false,
    "monetization_intent": true,
    "win_lose": true,
    "stable": true,
    "fish_model_low_poly_10k": true,
    "water_shader_50KB": true,
    "tether_line_visual": true,
    "max_build_size_100MB": true,
    "fps_60_target": true
  },
  "build_size_mb": 85.3,
  "file_count": 42,
  "gdd_safe": true
}
```

---

**END OF BUILD PIPELINE SPEC - Ready to Implement in v6**
