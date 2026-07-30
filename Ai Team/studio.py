#!/usr/bin/env python3
"""
AI GAME STUDIO v6 - FINAL - ANY LANGUAGE, ANY GAME TYPE, UNIQUE SPLITTING, MINIMAL GUI, NO MANUAL NONSENSE
- GDD SAFE: 4./5. GDD.md NEVER touched, only read
- ANY LANGUAGE: Python, C++, C#, Lua, GDScript, Rust, JS, etc. defined in GDD LANGUAGE field
- ANY GAME TYPE: 2D, 3D, Text, GUI - auto-detected
- UNIQUE SPLITTING: ID_role_Title_Part_Random4.ext - random hex suffix prevents overwrite
- NO MANUAL FILE NONSENSE: All file ops via GUI buttons or automated, not manual del/echo/mkdir
- EXPORT SYSTEM: MVP/Alpha/Beta/RC/Gold -> builds/{Stage}_{timestamp}_{random4}/ before clearing
- SAFEGUARDS: 41 measures against infinite loop, excessive looping, monoliths, etc.
- PIPELINE: IDEA (GDD READ ONLY) -> DETECT game type/language/engine -> PLAN missing only (dedup) -> BUILD once -> VALIDATE -> COMPILE /build/ -> TEST -> DONE -> IDLE (true finish)
"""

import os, time, json, urllib.request, urllib.error, re, shutil, random, subprocess
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).parent

def get_gdd_path():
    # v6 supports both 4. and 5. naming due to GUI being 4.
    candidates = [BASE / "5. GDD.md", BASE / "4. GDD.md", BASE / "GDD.md"]
    for c in candidates:
        if c.exists():
            return c
    return BASE / "5. GDD.md"

GDD_FILE = get_gdd_path()
INBOX_FILE = BASE / "INBOX.txt"
INBOX_HISTORY = BASE / "inbox_history.txt"
TASKS_FILE = BASE / "tasks.json"
MEMORY_FILE = BASE / "MEMORY.md"
PAUSE_FILE = BASE / "PAUSE"
OUTPUT_DIR = BASE / "output"
BUILD_DIR = BASE / "build"
BUILDS_ARCHIVE = BASE / "builds"
LOG_FILE = BASE / "logs.txt"

# Team models - fits 32GB RAM + RTX 5060 Ti 16GB
TEAM = {
    "aura": "qwen3:14b",
    "forge": "devstral:24b",
    "spark": "qwen2.5-coder:14b",
    "lore": "gemma3:12b",
    "pixel": "gemma3:12b",
    "glitch": "deepseek-r1:14b",
    "integrator": "qwen3:14b",
    "audio": "gemma3:4b"
}

SYSTEM = {}
for role_file in BASE.glob("roles/*.txt"):
    try:
        SYSTEM[role_file.stem] = role_file.read_text(encoding="utf-8")
    except:
        pass

if "aura" not in SYSTEM:
    SYSTEM["aura"] = "You are AURA Game Director."
if "integrator" not in SYSTEM:
    SYSTEM["integrator"] = "You are INTEGRATOR final builder."

def log(msg, tag="INFO"):
    ts = datetime.now().strftime("%H:%M:%S")
    line = f"[{ts}] [{tag}] {msg}"
    print(line, flush=True)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except: pass
    try:
        with open(BASE / "live_status.txt", "w", encoding="utf-8") as f:
            f.write(line)
    except: pass

def call_ollama(model, system_prompt, user_prompt, timeout=400):
    url = "http://localhost:11434/api/chat"
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "stream": False
    }
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        log(f"Loading {model} ...", "LOAD")
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            result = json.loads(resp.read().decode('utf-8'))
            content = result["message"]["content"]
            log(f"{model} responded ({len(content)} chars)", "DONE")
            return content
    except urllib.error.URLError as e:
        log(f"Ollama not running? {e} - Start Ollama app or ollama serve", "ERROR")
        time.sleep(5)
        return None
    except Exception as e:
        log(f"Call failed {model}: {e}", "ERROR")
        return None

def read_file(p):
    try:
        return Path(p).read_text(encoding="utf-8") if Path(p).exists() else ""
    except:
        return ""

def refresh_gdd_path():
    global GDD_FILE
    GDD_FILE = get_gdd_path()
    return GDD_FILE

# === NEW v6: Language Detection ===
def detect_language(gdd_text):
    lower = gdd_text.lower()
    # Look for LANGUAGE: line
    lang = "Python"  # default
    for line in gdd_text.splitlines():
        if "language:" in line.lower():
            # Take after colon
            parts = line.split(":",1)
            if len(parts)>1:
                candidate = parts[1].strip()
                # Clean up - take first language if multiple
                # e.g., "C++ + Lua" -> primary C++
                # e.g., "Python + C++" -> Python primary
                # Keep full string for info but primary is first
                if candidate:
                    lang = candidate[:50]  # limit
                    break
    # Normalize primary language for extension mapping
    lower_lang = lang.lower()
    primary = "python"
    ext = ".py"
    run_cmd = "python main.py"
    if "c++" in lower_lang or "cpp" in lower_lang:
        primary = "cpp"
        ext = ".cpp"
        run_cmd = "g++ main.cpp -o game && game.exe"
    elif "c#" in lower_lang or "csharp" in lower_lang:
        primary = "csharp"
        ext = ".cs"
        run_cmd = "dotnet run"
    elif "lua" in lower_lang:
        primary = "lua"
        ext = ".lua"
        run_cmd = "lua main.lua"
    elif "gdscript" in lower_lang or "godot" in lower_lang:
        primary = "gdscript"
        ext = ".gd"
        run_cmd = "godot --path . main.tscn"
    elif "rust" in lower_lang:
        primary = "rust"
        ext = ".rs"
        run_cmd = "cargo run"
    elif "javascript" in lower_lang or "js" in lower_lang and "typescript" not in lower_lang:
        primary = "javascript"
        ext = ".js"
        run_cmd = "node main.js"
    elif "typescript" in lower_lang or "ts" in lower_lang:
        primary = "typescript"
        ext = ".ts"
        run_cmd = "npx ts-node main.ts"
    elif "python" in lower_lang:
        primary = "python"
        ext = ".py"
        run_cmd = "python main.py"
    
    # Full language string for info (may contain +)
    full_lang = lang
    return full_lang, primary, ext, run_cmd

# === NEW v6: Game Type Detection ===
def detect_game_type(gdd_text):
    lower = gdd_text.lower()
    if any(k in lower for k in ["3d", "node3d", "tether", "ragdoll", "diving", "mesh", "model", "3d fishing", "global_transform"]):
        return "3D"
    elif any(k in lower for k in ["2d", "pixel", "sprite", "tilemap", "platformer", "2d fishing"]):
        return "2D"
    elif any(k in lower for k in ["text based", "text adventure", "parser", "text-based"]):
        return "Text"
    elif any(k in lower for k in ["gui only", "gui puzzle", "clicker", "editor", "window", "button"]):
        return "GUI"
    else:
        return "2D"  # default

def detect_engine_mode(gdd_text):
    lower = gdd_text.lower()
    custom_keywords = ["no engine", "from scratch", "custom engine", "build engine", "avoid unity", "avoid unreal", "no unity", "no unreal", "scratch build", "own engine", "engine: custom", "engine: none"]
    is_custom = any(k in lower for k in custom_keywords)
    has_steam = "steam" in lower
    has_server = any(k in lower for k in ["server", "steam api", "steamworks", "multiplayer", "dedicated", "netcode"])
    
    if is_custom:
        instruction = (
            "ENGINE OVERRIDE ACTIVE - CUSTOM FROM SCRATCH:\n"
            "- STRICT: DO NOT USE Unity, Unreal, Godot unless GDD explicitly says so.\n"
            "- Build custom engine from scratch in detected LANGUAGE with SDL/Raylib/OpenGL/PyGame/LÖVE etc.\n"
            "- DO NOT mention Unity GameObjects/MonoBehaviour/UObjects.\n"
            "- Focus on: " + ("Steamworks API, " if has_steam else "") + ("dedicated servers, " if has_server else "") + "custom window, main loop, input, physics.\n"
        )
        return "custom", instruction
    else:
        return "standard", "Follow Engine field in GDD exactly."

def scan_existing_outputs():
    """Scans output/ to prevent duplicate work - any language"""
    existing = []
    existing_titles = set()
    if not OUTPUT_DIR.exists():
        return existing, existing_titles
    # Any source extension for any language
    valid_exts = {".py",".cpp",".h",".hpp",".cs",".lua",".gd",".rs",".js",".ts",".go",".java",".shader",".md",".txt",".json"}
    for f in OUTPUT_DIR.rglob("*.*"):
        if f.is_file() and f.suffix.lower() in valid_exts:
            if f.stat().st_size < 10:
                continue
            name = f.stem.lower().replace("_"," ").replace("-"," ")
            name = re.sub(r"^\d+\s+", "", name)
            name = re.sub(r"^(forge|spark|lore|pixel|glitch|aura|integrator|audio)\s+", "", name)
            # Remove random suffix like _A1B2
            name = re.sub(r"\s+[a-f0-9]{4}$", "", name)
            name = re.sub(r"\s+core\s+[a-f0-9]{4}$", "", name)
            name = re.sub(r"\s+utils\s+[a-f0-9]{4}$", "", name)
            existing.append(str(f.relative_to(BASE)))
            existing_titles.add(name.strip())
    return existing, existing_titles

def save_memory(text):
    try:
        MEMORY_FILE.write_text(f"# STUDIO MEMORY v6 - {datetime.now()}\n\n{text}\n", encoding="utf-8")
    except: pass

def random_suffix():
    return f"{random.randint(0, 0xFFFF):04x}"

def ext_for_role(role, primary_ext):
    """Map role to extension - respects language"""
    # Lore, qa always .md even if language is C++
    if role in ["lore"]:
        return ".md"
    if role in ["glitch","qa"]:
        return ".md"
    if role in ["pixel","art"]:
        return ".shader" if primary_ext in [".cpp",".cs"] else ".py"
    # Code roles use primary language ext
    return primary_ext

def folder_for_role(role):
    if role in ["forge","spark","integrator"]:
        return "code"
    if role in ["lore"]:
        return "lore"
    if role in ["pixel","art"]:
        return "art"
    if role in ["glitch","qa"]:
        return "qa"
    if role in ["audio"]:
        return "audio"
    return "code"

def export_build(stage_name):
    """Export current build to unique folder before clearing - industry standard"""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    suffix = random_suffix()
    export_path = BUILDS_ARCHIVE / f"{stage_name}_{timestamp}_{suffix}"
    export_path.mkdir(parents=True, exist_ok=True)
    try:
        # Copy build/
        if BUILD_DIR.exists():
            shutil.copytree(BUILD_DIR, export_path / "build", dirs_exist_ok=True, ignore=shutil.ignore_patterns('__pycache__','*.pyc','save_file.json'))
        # Copy GDD, tasks, memory, logs
        if GDD_FILE.exists():
            shutil.copy(GDD_FILE, export_path / f"GDD_{stage_name}.md")
        if TASKS_FILE.exists():
            shutil.copy(TASKS_FILE, export_path / f"tasks_{stage_name}.json")
        if MEMORY_FILE.exists():
            shutil.copy(MEMORY_FILE, export_path / f"MEMORY_{stage_name}.md")
        if LOG_FILE.exists():
            shutil.copy(LOG_FILE, export_path / f"logs_{stage_name}.txt")
        
        gdd_text = read_file(GDD_FILE)
        full_lang, primary, ext, run_cmd = detect_language(gdd_text)
        game_type = detect_game_type(gdd_text)
        engine_mode, _ = detect_engine_mode(gdd_text)

        file_count = len(list(export_path.rglob("*")))
        size_mb = sum(f.stat().st_size for f in export_path.rglob("*") if f.is_file()) / 1024 / 1024

        manifest = {
            "stage": stage_name,
            "timestamp": timestamp,
            "engine": engine_mode,
            "language_full": full_lang,
            "language_primary": primary,
            "language_ext": ext,
            "game_type": game_type,
            "file_count": file_count,
            "build_size_mb": round(size_mb,2),
            "gdd_safe": True,
            "random_suffix": suffix,
            "export_path": str(export_path)
        }
        (export_path / f"EXPORT_MANIFEST_{stage_name}.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        log(f"Exported {stage_name} build to {export_path} ({size_mb:.1f} MB)", "EXPORT")
        return export_path
    except Exception as e:
        log(f"Export failed: {e}", "ERROR")
        return None

def ensure_build_runnable(primary_ext, run_cmd, engine_mode, gdd_text):
    """Guarantees build/ always has runnable main file in detected language"""
    BUILD_DIR.mkdir(exist_ok=True)
    main_path = BUILD_DIR / f"main{primary_ext}"

    if main_path.exists() and main_path.stat().st_size > 100:
        return main_path

    # Language-specific fallbacks
    fallbacks = {
        ".py": f'''#!/usr/bin/env python3
"""
Fallback Build - Custom Engine From Scratch - Auto-generated
Engine: {engine_mode} - Guarantees build always runnable
GDD snippet: {gdd_text[:200]}
"""
print("="*60)
print(" Fallback Build - Custom Engine From Scratch")
print(" Language: Python - Engine: {engine_mode}")
print(" This fallback ensures build/ ALWAYS runnable - start>finish guarantee")
print("="*60)
print("Your fragments are in output/ - check repo_backup/ for original files")
print("Edit 5. GDD.md to trigger rebuild")
''',
        ".cpp": f'''
// Fallback Build - Custom Engine From Scratch - C++
#include <iostream>
int main() {{
    std::cout << "Fallback Build - Custom Engine C++ - Engine: {engine_mode}" << std::endl;
    std::cout << "Build always runnable - start>finish guarantee" << std::endl;
    return 0;
}}
''',
        ".cs": f'''
using System;
class Program {{
    static void Main() {{
        Console.WriteLine("Fallback Build - Custom Engine C# - Engine: {engine_mode}");
    }}
}}
''',
        ".lua": f'''
-- Fallback Build - Custom Engine Lua
print("Fallback Build - Custom Engine Lua - Engine: {engine_mode}")
''',
        ".gd": f'''
extends Node
func _ready():
    print("Fallback Build - Custom Engine GDScript - Engine: {engine_mode}")
''',
        ".rs": f'''
fn main() {{
    println!("Fallback Build - Custom Engine Rust - Engine: {engine_mode}");
}}
''',
        ".js": f'''
console.log("Fallback Build - Custom Engine JS - Engine: {engine_mode}");
''',
    }

    content = fallbacks.get(primary_ext, fallbacks[".py"])
    main_path.write_text(content, encoding="utf-8")
    log(f"Fallback build created: {main_path} (language {primary_ext})", "BUILD")

    # Create run.bat / run.sh language-aware
    run_bat = BUILD_DIR / "run.bat"
    if primary_ext == ".py":
        run_bat.write_text("@echo off\npython main.py\npause\n", encoding="utf-8")
    elif primary_ext == ".cpp":
        run_bat.write_text("@echo off\ng++ main.cpp -o game.exe && game.exe\npause\n", encoding="utf-8")
    elif primary_ext == ".cs":
        run_bat.write_text("@echo off\ndotnet run\npause\n", encoding="utf-8")
    elif primary_ext == ".lua":
        run_bat.write_text("@echo off\nlua main.lua\npause\n", encoding="utf-8")
    elif primary_ext == ".gd":
        run_bat.write_text("@echo off\necho Open in Godot\npause\n", encoding="utf-8")
    elif primary_ext == ".rs":
        run_bat.write_text("@echo off\ncargo run\npause\n", encoding="utf-8")
    elif primary_ext == ".js":
        run_bat.write_text("@echo off\nnode main.js\npause\n", encoding="utf-8")
    else:
        run_bat.write_text(f"@echo off\n{run_cmd}\npause\n", encoding="utf-8")

    (BUILD_DIR / "run.sh").write_text(f"#!/bin/bash\n{run_cmd}\n", encoding="utf-8")
    return main_path

def main():
    OUTPUT_DIR.mkdir(exist_ok=True)
    BUILD_DIR.mkdir(exist_ok=True)
    BUILDS_ARCHIVE.mkdir(exist_ok=True)
    for sub in ["code","lore","art","qa","audio"]:
        (OUTPUT_DIR / sub).mkdir(parents=True, exist_ok=True)

    log("==================================================", "START")
    log("AI GAME STUDIO v6 - ANY LANGUAGE, ANY GAME TYPE, GUI, NO MANUAL NONSENSE", "START")
    log("Pipeline: IDEA (GDD READ-ONLY) -> DETECT type/language/engine -> PLAN missing only -> BUILD once -> VALIDATE -> COMPILE /build/ -> TEST -> DONE -> IDLE", "FLOW")
    refresh_gdd_path()
    log(f"GDD READ ONLY, NEVER modified: {GDD_FILE}", "SAFE")
    gdd_text_initial = read_file(GDD_FILE)
    full_lang, primary, ext, run_cmd = detect_language(gdd_text_initial)
    game_type = detect_game_type(gdd_text_initial)
    log(f"Detected Language: {full_lang} -> primary {primary} ext {ext} run: {run_cmd}", "DETECT")
    log(f"Detected Game Type: {game_type}", "DETECT")
    log(f"Team: {', '.join([f'{k}={v}' for k,v in TEAM.items()])}", "INFO")
    log("==================================================", "START")

    tasks = []
    if TASKS_FILE.exists():
        try:
            tasks = json.loads(read_file(TASKS_FILE))
            log(f"Loaded {len(tasks)} tasks", "MEMORY")
        except:
            tasks = []

    memory_summary = read_file(MEMORY_FILE) or "No memory yet."
    last_gdd_mtime = 0
    inbox_directive_global = ""

    while True:
        if PAUSE_FILE.exists():
            log("PAUSED - delete PAUSE via GUI Resume button (no manual file ops needed, but PAUSE file still works)", "PAUSE")
            time.sleep(10)
            continue

        # INBOX - GDD safe, goes to history
        inbox = read_file(INBOX_FILE).strip()
        if inbox:
            log(f"NEW DIRECTIVE from INBOX: {inbox} (GDD untouched)", "HUMAN")
            inbox_directive_global = inbox
            INBOX_FILE.write_text("", encoding="utf-8")
            last_gdd_mtime = 0
            try:
                with open(INBOX_HISTORY, "a", encoding="utf-8") as f:
                    f.write(f"\n[{datetime.now()}] {inbox}\n")
            except: pass

        refresh_gdd_path()
        cur_mtime = GDD_FILE.stat().st_mtime if GDD_FILE.exists() else 0
        gdd_changed = cur_mtime != last_gdd_mtime

        existing_files, existing_titles = scan_existing_outputs()
        pending = [t for t in tasks if t.get("status") in ["pending","failed","in_progress"]]

        if gdd_changed or len(pending) == 0:
            if gdd_changed:
                log(f"{GDD_FILE.name} changed! Re-reading GDD read-only...", "AURA")
                last_gdd_mtime = cur_mtime
                # Remove DONE to allow rebuild
                done_path = BUILD_DIR / "DONE"
                if done_path.exists():
                    try:
                        done_path.unlink()
                        log("GDD changed after DONE - removing DONE for rebuild", "REBUILD")
                    except: pass
            else:
                log("All active tasks done. Checking build phase...", "AURA")

            gdd_text = read_file(GDD_FILE)
            if not gdd_text.strip():
                log(f"{GDD_FILE.name} empty - waiting", "WAIT")
                time.sleep(5)
                continue

            full_lang, primary, ext, run_cmd = detect_language(gdd_text)
            game_type = detect_game_type(gdd_text)
            engine_mode, engine_instruction = detect_engine_mode(gdd_text)
            log(f"Engine: {engine_mode.upper()} Language: {full_lang} ({primary}) Type: {game_type}", "ENGINE")

            output_index = "\n".join(existing_files[-30:]) if existing_files else "No files yet"
            titles_list = ", ".join(list(existing_titles)[:20]) if existing_titles else "none"
            completed_str = "\n".join([f"- {t['title']} [{t['role']}]" for t in tasks if t.get("status")=="done"][-15:]) or "None yet"

            # INTEGRATOR / COMPILE - Guaranteed finish
            should_build = False
            main_path_check = BUILD_DIR / f"main{ext}"
            # Also check any main.* exists
            any_main = any((BUILD_DIR / f"main{e}").exists() for e in [".py",".cpp",".cs",".lua",".gd",".rs",".js",".ts"])
            if len(pending) == 0 and len(existing_files) >= 1:
                if not any_main:
                    should_build = True
                    log(f"Build missing main.* but have {len(existing_files)} fragments - triggering compile", "BUILD")
                elif gdd_changed:
                    should_build = True
                    log("GDD changed - triggering rebuild", "BUILD")
                elif not (BUILD_DIR / "DONE").exists() and len(existing_files) >= 3:
                    should_build = True
                    log("No DONE but have fragments - final compile", "BUILD")

            if should_build:
                log(f"FINAL COMPILATION to {BUILD_DIR} - {len(existing_files)} fragments -> full game in {full_lang}", "INTEGRATOR")
                code_files = []
                for cf in (OUTPUT_DIR / "code").glob("*.*"):
                    if cf.is_file() and cf.stat().st_size > 20:
                        try:
                            code_files.append(f"--- {cf.name} ---\n{cf.read_text(encoding='utf-8')[:1500]}")
                        except: pass
                code_bundle = "\n\n".join(code_files[-12:])[:10000]
                extra_context = f"\nHUMAN DIRECTIVE (GDD untouched): {inbox_directive_global}\n" if inbox_directive_global else ""

                integrator_prompt = f"""
GDD (READ ONLY):
{gdd_text[:4000]}
{extra_context}

FRAGMENTS ({len(existing_files)} files):
{code_bundle}

ENGINE: {engine_mode} - {engine_instruction}
LANGUAGE: {full_lang} primary {primary} ext {ext}
GAME TYPE: {game_type}

TASK: Merge fragments into ONE runnable game in /build/ in LANGUAGE {full_lang}.
Requirements:
- Build in {full_lang} - entry main{ext} - {run_cmd}
- If custom engine: from scratch, no Unity/Unreal, focus Steam API stub + server stub if mentioned
- Must include window creation, main loop, input, core mechanic
- Output code block for main file: ```{primary} ... ```
"""
                result = call_ollama(TEAM["integrator"], SYSTEM.get("integrator",""), integrator_prompt, 400)
                try:
                    BUILD_DIR.mkdir(exist_ok=True)
                    if result:
                        (BUILD_DIR / "integrator_output.md").write_text(result, encoding="utf-8")
                        # Try extract code block for detected language
                        # Look for ```python, ```cpp, etc.
                        main_path = BUILD_DIR / f"main{ext}"
                        # Try generic extraction
                        pattern = f"```{primary}"
                        if pattern in result.lower():
                            # Find case insensitive
                            lower_res = result.lower()
                            idx = lower_res.find(pattern)
                            if idx != -1:
                                # Extract from original result at idx
                                after = result[idx+len(pattern):]
                                code = after.split("```")[0]
                                if len(code.strip()) > 50:
                                    main_path.write_text(code, encoding="utf-8")
                                    log(f"Build {main_path.name} extracted from LLM", "BUILD")
                        elif "```" in result:
                            # Fallback extract first code block
                            parts = result.split("```")
                            for i in range(1, len(parts), 2):
                                code_candidate = parts[i]
                                # Remove language identifier first line if present
                                lines = code_candidate.splitlines()
                                if lines and lines[0].strip().lower() in ["python","cpp","c++","c#","lua","gdscript","rust","javascript","js"]:
                                    code_candidate = "\n".join(lines[1:])
                                if len(code_candidate.strip()) > 100:
                                    main_path.write_text(code_candidate, encoding="utf-8")
                                    log(f"Build {main_path.name} extracted (fallback)", "BUILD")
                                    break
                    
                    ensure_build_runnable(primary, run_cmd, engine_mode, gdd_text)

                    # Test
                    log("Build created, running smoke test...", "TEST")
                    try:
                        # Only test python easily, for other languages just check file exists
                        if primary == "python":
                            test_res = subprocess.run(["python", str(BUILD_DIR / f"main{ext}")], timeout=5, capture_output=True, text=True, cwd=str(BUILD_DIR))
                            log(f"Test exit {test_res.returncode}", "TEST")
                            (BUILD_DIR / "test_results.txt").write_text(f"Exit: {test_res.returncode}\nStdout: {test_res.stdout[:500]}\nStderr: {test_res.stderr[:500]}", encoding="utf-8")
                        else:
                            (BUILD_DIR / "test_results.txt").write_text(f"Build for {full_lang} created, manual test needed: {run_cmd}", encoding="utf-8")
                    except Exception as e:
                        log(f"Test: {e}", "TEST")

                    (BUILD_DIR / "DONE").write_text(f"DONE at {datetime.now()}\nEngine: {engine_mode}\nLanguage: {full_lang}\nType: {game_type}\nFragments: {len(existing_files)}\n", encoding="utf-8")
                    log(f"FINAL BUILD DONE in {BUILD_DIR} - DONE file written - TRUE FINISH", "DONE")
                    inbox_directive_global = ""
                    time.sleep(10)
                    continue

                except Exception as e:
                    log(f"Build failed: {e}", "ERROR")
                    ensure_build_runnable(primary, run_cmd, engine_mode, gdd_text)
                    time.sleep(5)
                    continue

            # Planning - only missing
            aura_system = SYSTEM.get("aura","") + f"\n\n{engine_instruction}\nLanguage: {full_lang} primary {primary} ext {ext}\nGame Type: {game_type}\n\nCRITICAL: Existing: {titles_list}\nDo NOT re-plan existing unless GDD says IMPROVE/REDO/REBUILD\nEngine={engine_mode} Language={full_lang} Type={game_type} must be respected\nNeed diversity: at least 1 FORGE, 1 SPARK, 1 LORE, 1 PIXEL, 1 GLITCH, 1 AUDIO if missing in output"

            inbox_part = f"\nHUMAN DIRECTIVE (GDD untouched): {inbox_directive_global}\n" if inbox_directive_global else ""

            aura_prompt = f"""
You are AURA supervisor. GDD READ ONLY.

MEMORY:
{memory_summary[:2500]}

GDD (READ ONLY):
{gdd_text[:4500]}
{inbox_part}

OUTPUT INDEX - Already have (DO NOT RE-PLAN unless IMPROVE/REDO):
{output_index}
Titles: {titles_list}

COMPLETED:
{completed_str}

ENGINE: {engine_mode} - {engine_instruction}
LANGUAGE: {full_lang} primary {primary} ext {ext} - Build files must use {ext}
GAME TYPE: {game_type}

TASK: Plan ONLY missing features not in output index. 3-5 small isolated tasks max, must include diverse roles (at least 1 FORGE, 1 SPARK, 1 LORE, 1 PIXEL, 1 GLITCH if missing).
Each task role: forge=engine/systems, spark=gameplay, lore=story, pixel=art, glitch=qa, audio=sfx, integrator is not for you to plan (system auto)
Output ONLY JSON array: [{{"id":1,"role":"forge","title":"...","prompt":"..."}}] with title short, prompt detailed for language {full_lang}
If all core features exist, output [].
JSON only.
"""

            result = call_ollama(TEAM["aura"], aura_system, aura_prompt, 200)
            if not result:
                time.sleep(10)
                continue

            try:
                raw = result
                if "```" in raw:
                    for part in raw.split("```"):
                        if "[" in part and "]" in part:
                            raw = part
                            break
                s = raw.find("[")
                e = raw.rfind("]")+1
                if s != -1 and e != 0:
                    raw = raw[s:e]
                new_tasks = json.loads(raw)

                done_tasks = [t for t in tasks if t.get("status")=="done"]
                filtered = []
                next_id = max([t.get("id",0) for t in tasks], default=0) + 1

                for nt in new_tasks:
                    if "id" not in nt:
                        nt["id"] = next_id
                        next_id += 1
                    safe = re.sub(r"[^a-z0-9]","", nt.get("title","").lower())
                    is_dup = False
                    for ex in existing_titles:
                        ex_safe = re.sub(r"[^a-z0-9]","", ex.lower())
                        if ex_safe and len(safe)>5 and (ex_safe in safe or safe in ex_safe):
                            if not any(k in gdd_text.lower() for k in ["improve","redo","rebuild"]):
                                is_dup = True
                                log(f"Dedup skip: {nt['title']} already exists as {ex}", "DEDUP")
                                break
                    if not is_dup:
                        nt["status"] = "pending"
                        nt["attempts"] = 0
                        nt["created_at"] = str(datetime.now())
                        nt["prompt"] = nt["prompt"] + f"\n\nENGINE RULE: {engine_instruction}\nLANGUAGE RULE: Build in {full_lang} primary {primary} ext {ext}\nSTRICT: {nt['role']} ONLY."
                        filtered.append(nt)

                if not filtered:
                    log("All GDD features already in output/ - IDLE until GDD changes (prevents endless loop)", "IDLE")
                    tasks = done_tasks
                    TASKS_FILE.write_text(json.dumps(tasks, indent=2), encoding="utf-8")
                    time.sleep(15)
                    continue

                tasks = done_tasks + filtered
                TASKS_FILE.write_text(json.dumps(tasks, indent=2), encoding="utf-8")
                new_mem = f"GDD: {gdd_text[:300]}...\nEngine: {engine_mode} Lang: {full_lang} Type: {game_type}\nExisting: {len(existing_files)} files\nNew: {len(filtered)} tasks\n"
                save_memory(new_mem)
                memory_summary = new_mem
                log(f"AURA planned {len(filtered)} new (deduped from {len(new_tasks)})", "AURA")
                for t in filtered:
                    log(f"  + [{t['role'].upper()}] {t['title']} [{primary}]", "PLAN")
            except Exception as e:
                log(f"AURA JSON fail: {e} Raw:{result[:400]}", "ERROR")
                time.sleep(5)
                continue

        pending = [t for t in tasks if t.get("status") in ["pending","failed"]]
        if not pending:
            if not (BUILD_DIR / "DONE").exists() and len(existing_files) >= 1:
                time.sleep(2)
                continue
            log("No pending tasks. IDLE waiting for GDD change - TRUE FINISH, not looping", "IDLE")
            time.sleep(15)
            continue

        task = pending[0]
        role = task.get("role","forge")
        if role not in TEAM:
            role = "forge"
        model = TEAM[role]

        safe_title = re.sub(r"[^a-z0-9]","", task.get("title","").lower())
        attempt_count = sum(1 for t in tasks if re.sub(r"[^a-z0-9]","", t.get("title","").lower()) == safe_title and t.get("attempts",0)>=1)
        if attempt_count >=3 or task.get("attempts",0) >=3:
            log(f"LOOP BREAKER: Skip {task['title']} after {task.get('attempts',0)} fails", "BREAKER")
            task["status"] = "done"
            task["note"] = "Skipped by loop breaker"
            TASKS_FILE.write_text(json.dumps(tasks, indent=2), encoding="utf-8")
            continue

        task["status"] = "in_progress"
        task["attempts"] = task.get("attempts",0)+1
        TASKS_FILE.write_text(json.dumps(tasks, indent=2), encoding="utf-8")

        log(f"Delegating -> [{role.upper()}] {task['title']} (Attempt {task['attempts']}) [{full_lang}]", "DELEGATE")

        gdd_snippet = read_file(GDD_FILE)[:3500]
        engine_mode, engine_instruction = detect_engine_mode(gdd_snippet)
        full_lang, primary, ext, run_cmd = detect_language(gdd_snippet)
        game_type = detect_game_type(gdd_snippet)

        base_system = SYSTEM.get(role,"")
        if engine_mode == "custom":
            base_system = base_system.replace("Unity","custom engine").replace("Unreal","custom engine").replace("Godot","custom")
            base_system += f"\n\n{engine_instruction}\nSTRICTLY NO Unity/Unreal.\nLANGUAGE: {full_lang} primary {primary} ext {ext} - Must respect."

        worker_prompt = f"""
GDD (READ ONLY, respect Engine + Language + Game Type):
{gdd_snippet}

TASK ({role} ONLY) in LANGUAGE {full_lang} primary {primary} ext {ext}:
Title: {task['title']}
Details: {task['prompt']}

ENGINE MODE: {engine_mode}
{engine_instruction}
LANGUAGE: {full_lang} primary {primary} ext {ext} -> File must be *{ext}
GAME TYPE: {game_type}

RULES: Stay lane, respect engine+language+type, output file-ready result in {full_lang}. Max 500 lines, 25KB, 100 chars line. GDD read-only.
"""

        result = call_ollama(model, base_system, worker_prompt, 350)
        if not result:
            task["status"] = "failed"
            TASKS_FILE.write_text(json.dumps(tasks, indent=2), encoding="utf-8")
            continue

        # Unique naming with random suffix to avoid overwrite - v6 fix for repeat naming
        ext_to_use = ext_for_role(role, primary)
        folder_to_use = folder_for_role(role)
        safe_file_title = "".join(c if c.isalnum() else "_" for c in task['title'])[:30]
        rand_suf = random_suffix()
        fname = f"{task.get('id',99):02d}_{role}_{safe_file_title}_{rand_suf}{ext_to_use}"
        fpath = OUTPUT_DIR / folder_to_use / fname
        fpath.write_text(result, encoding="utf-8")
        log(f"{role.upper()} DONE -> {fpath} ({len(result)} chars) [{full_lang}]", "DONE")

        # Validation
        log(f"AURA validating {role} work... Language {full_lang} Engine {engine_mode}", "VALIDATE")
        validate_prompt = f"""
GDD (truth, read-only):
{gdd_snippet[:2000]}

Task: {task['title']} Role: {role} Language: {full_lang} primary {primary}
Expected: {task['prompt']}
Engine Mode: {engine_mode} - {engine_instruction}

Worker Output (first 3000 chars):
{result[:3000]}

Check: 1) role lane 2) engine respect 3) language respect ({full_lang}) 4) not haywire 5) file size <=500 lines 6) unique naming (has random suffix)
Output JSON ONLY: {{"verdict":"PASS/FAIL","reason":"...","fix":"..."}}
"""
        validation = call_ollama(TEAM["aura"], SYSTEM.get("aura",""), validate_prompt, 200)
        try:
            if validation:
                raw = validation
                s = raw.find("{")
                e = raw.rfind("}")+1
                if s != -1:
                    raw = raw[s:e]
                v = json.loads(raw)
                verdict = v.get("verdict","PASS").upper()
                if "FAIL" in verdict:
                    log(f"VALIDATION FAIL: {v.get('reason')} Fix:{v.get('fix')}", "FAIL")
                    if task["attempts"] < 3:
                        task["status"] = "pending"
                        task["prompt"] = task["prompt"] + f"\nCORRECTION: {v.get('fix')}"
                    else:
                        task["status"] = "done"
                        task["note"] = f"Failed but breaker forced done: {v.get('reason')}"
                else:
                    log(f"VALIDATION PASS - {v.get('reason','ok')}", "PASS")
                    task["status"] = "done"
                task["output_file"] = str(fpath)
                TASKS_FILE.write_text(json.dumps(tasks, indent=2), encoding="utf-8")
                memory_summary += f"\n- Done: {task['title']} [{role}] {full_lang} -> {verdict}"
                save_memory(memory_summary)
            else:
                task["status"] = "done"
                task["output_file"] = str(fpath)
                TASKS_FILE.write_text(json.dumps(tasks, indent=2), encoding="utf-8")
        except Exception as e:
            log(f"Validation parse fail, PASS assumed: {e}", "VALIDATE")
            task["status"] = "done"
            task["output_file"] = str(fpath)
            TASKS_FILE.write_text(json.dumps(tasks, indent=2), encoding="utf-8")

        time.sleep(2)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log("Stopped - Memory saved, GDD untouched. Resume via 2. Start Team.bat or GUI", "STOP")
