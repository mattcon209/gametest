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

import time, json, urllib.request, urllib.error, re, shutil, random, subprocess
import sys, difflib, concurrent.futures
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).resolve().parent  # FIX N2: resolve() hardens all paths, fixes smoke test build/build/main.py bug

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

# Per-role temperature: deterministic for code/QA/build, creative for narrative/art/audio
# (looked up by model so every call path gets it with no signature changes)
TEMP_BY_MODEL = {
    "qwen3:14b": 0.3,          # aura + integrator - planning/merging must be precise
    "devstral:24b": 0.3,       # forge - engine code
    "qwen2.5-coder:14b": 0.4,  # spark - gameplay code
    "deepseek-r1:14b": 0.2,    # glitch - QA reasoning must be strict
    "gemma3:12b": 0.8,         # lore + pixel - creative writing/art direction
    "gemma3:4b": 0.7,          # audio
}

def preflight_models():
    """Check /api/tags at startup so a missing model surfaces as a clear
    'ollama pull X' instruction once, instead of a generic 'Call failed'
    that silently burns task attempts (Audit5 H2-ollama)."""
    try:
        with urllib.request.urlopen("http://localhost:11434/api/tags", timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        pulled = {m.get("name", "").lower() for m in data.get("models", []) if m.get("name")}
        missing = []
        for role, model in TEAM.items():
            base = model.lower()
            # REGRESSION FIX (Audit6): match the TAG EXACTLY. The previous
            # startswith(base.split(":")[0] + ":") test meant any gemma3:* satisfied
            # a requirement for gemma3:4b - so a machine with only gemma3:12b pulled
            # was reported "all 8 role models present" while AUDIO's model was absent
            # (different model entirely: 3.3GB vs 7.8GB VRAM). Verified by test.
            # Only fall back to prefix logic when the requirement itself is untagged.
            if ":" in base:
                ok = base in pulled or f"{base}:latest" in pulled
            else:
                ok = any(p == base or p.startswith(base + ":") for p in pulled)
            if not ok:
                missing.append((role, model))
        if missing:
            log(f"PREFLIGHT: {len(missing)} model(s) NOT pulled:", "PREFLIGHT")
            for role, model in missing:
                log(f"  MISSING [{role}] -> run: ollama pull {model}", "PREFLIGHT")
        else:
            log(f"PREFLIGHT: all {len(TEAM)} role models present in Ollama", "PREFLIGHT")
        return missing
    except Exception as e:
        log(f"PREFLIGHT: could not reach Ollama (/api/tags): {e} - is 'ollama serve' running?", "PREFLIGHT")
        return None

def call_ollama(model, system_prompt, user_prompt, timeout=400):
    url = "http://localhost:11434/api/chat"
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "stream": False,
        "options": {
            "num_ctx": 8192,
            "temperature": TEMP_BY_MODEL.get(model, 0.6)
        },
        "keep_alive": "5m"
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

# === v6.1 FIXED: Language Detection - Explicit field first, engine-hint fallback ===
def _lang_from_string(s):
    """Map a language/engine string to (primary, ext, run_cmd) using plain
    substring matching. This only ever runs against the LANGUAGE field or
    engine/tech hint lines - text that IS about languages - so word-boundary
    regexes are unnecessary, and the old ones were actively broken:
    r'\\bc\\+\\+\\b' can NEVER match because '+' is a non-word character, so a
    word boundary cannot follow it (same for 'c#'). LANGUAGE: C++ silently
    fell through to Python."""
    t = s.lower()
    if "c++" in t or "cpp" in t:
        return "cpp", ".cpp", "g++ main.cpp -o game && game.exe"
    if "c#" in t or "csharp" in t:
        return "csharp", ".cs", "dotnet run"
    if "gdscript" in t or "godot" in t:
        return "gdscript", ".gd", "godot --path . main.tscn"
    if "lua" in t or "love2d" in t:
        return "lua", ".lua", "lua main.lua"
    if "rust" in t:
        return "rust", ".rs", "cargo run"
    if "typescript" in t:
        return "typescript", ".ts", "npx ts-node main.ts"
    if "javascript" in t or re.search(r"\bjs\b", t):
        return "javascript", ".js", "node main.js"
    if "python" in t or "pygame" in t:
        return "python", ".py", "python main.py"
    if "unreal" in t:
        return "cpp", ".cpp", "g++ main.cpp -o game && game.exe"
    if "unity" in t:
        return "csharp", ".cs", "dotnet run"
    return None, None, None

def detect_language(gdd_text):
    # First, look for explicit LANGUAGE field
    lang = ""
    for line in gdd_text.splitlines():
        if re.match(r"^\s*LANGUAGE\s*:", line, re.IGNORECASE):
            parts = line.split(":", 1)
            if len(parts) > 1 and parts[1].strip():
                lang = parts[1].strip()[:50]
                break

    if lang:
        # FIX M3: First listed language is primary - split by + and take first token
        # e.g., "Python + C++" -> primary = Python, not C++ (old checked C++ first)
        first_lang = lang.split("+")[0].strip()
        primary, ext, run_cmd = _lang_from_string(first_lang)
        if not primary:
            primary, ext, run_cmd = _lang_from_string(lang)
        if primary:
            return lang, primary, ext, run_cmd

    # No usable LANGUAGE field - infer from ENGINE/TECH hints before defaulting.
    # Shipped GDDs often specify an engine (e.g. "Godot 4.2 GDScript preferred")
    # but omit the LANGUAGE line entirely; silent-Python was the Python-only bug.
    for line in gdd_text.splitlines():
        if re.match(r"^\s*(ENGINE|TECH)\s*:", line, re.IGNORECASE) or "engine:" in line.lower():
            try:
                hint_part = line.split(":", 1)[1]
            except IndexError:
                hint_part = line
            # Respect listing order within the line: check segments first->last
            # so "Godot GDScript (preferred) or Unity C#" infers gdscript,
            # not the second-listed unity/csharp (M3 ordering rule)
            segments = re.split(r"\bor\b|,|/|\||-", hint_part.lower())
            for seg in segments:
                primary, ext, run_cmd = _lang_from_string(seg.strip())
                if primary:
                    log(f"No LANGUAGE field - inferred {primary} from engine/tech line: {line.strip()[:60]}", "DETECT")
                    return f"Inferred {primary} (add LANGUAGE: field to GDD to pin)", primary, ext, run_cmd

    log("No LANGUAGE field and no engine hint - defaulting to Python (add LANGUAGE: field to pin)", "DETECT")
    return "Python", "python", ".py", "python main.py"

# === v6.1 FIXED: Game Type Detection - Explicit field first, word boundaries ===
def detect_game_type(gdd_text):
    # First check explicit GAME TYPE field if present
    for line in gdd_text.splitlines():
        if re.match(r"^\s*GENRE\s*:", line, re.IGNORECASE) or re.match(r"^\s*GAME TYPE\s*:", line, re.IGNORECASE):
            lower_line = line.lower()
            # Explicit 2D/3D mentions in genre line
            if re.search(r"\b3d\b", lower_line):
                return "3D"
            if re.search(r"\b2d\b", lower_line):
                # Check for pixel qualifier
                if "pixel" in lower_line:
                    return "2D Pixel"
                return "2D"
            if "text" in lower_line:
                return "Text"
            if "gui" in lower_line:
                return "GUI"

    lower = gdd_text.lower()
    # Use word boundaries to avoid false positives on "model" substring (M1 fix)
    # Old code: "model" matched any occurrence like "all models read this"
    # New: check for explicit game type keywords with \b and prioritize genre line above
    if re.search(r"\b3d\b", lower) or re.search(r"\bnode3d\b", lower) or re.search(r"\btether\b", lower) or re.search(r"\bragdoll\b", lower):
        # But exclude if it's in a comment about models plural that is not game type - we already checked GENRE field first
        # Require additional 3D indicator, not just "model" alone
        if re.search(r"\b3d\b", lower) or "tether" in lower or "ragdoll" in lower or "diving" in lower:
            return "3D"
    if re.search(r"\b2d\b", lower) and "pixel" in lower:
        return "2D Pixel"
    if re.search(r"\b2d\b", lower):
        return "2D"
    if re.search(r"\btext\s*based\b|\btext\s*adventure\b|\bparser\b", lower):
        return "Text"
    if re.search(r"\bgui\s*only\b|\bgui\s*puzzle\b|\bclicker\b.*\bgui\b", lower):
        return "GUI"

    return "2D"  # default safe fallback

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
    """Scans output/ to prevent duplicate work - any language - FIXED M6: Only strip _XXXX random suffix from f.stem BEFORE _->space, not legit words like cafe"""
    existing = []
    existing_titles = set()
    if not OUTPUT_DIR.exists():
        return existing, existing_titles
    valid_exts = {".py",".cpp",".h",".hpp",".cs",".lua",".gd",".rs",".js",".ts",".go",".java",".shader",".md",".txt",".json"}
    for f in OUTPUT_DIR.rglob("*.*"):
        if f.is_file() and f.suffix.lower() in valid_exts:
            if f.stat().st_size < 10:
                continue
            stem = f.stem
            # FIX M6 (for real this time): strip the _XXXX random suffix from the
            # stem BEFORE the _->space conversion, and WITHOUT IGNORECASE.
            # random_suffix() only ever generates lowercase hex; matching
            # case-insensitively eats legitimate Title-case trailing words
            # (Cafe/Fade/Face/Deed/Bead are all in [a-f]).
            stem = re.sub(r"_(core|utils|api|part\d+)_?[a-f0-9]{4}$", "", stem)
            stem = re.sub(r"_[a-f0-9]{4}$", "", stem)
            name = stem.lower().replace("_"," ").replace("-"," ")
            name = re.sub(r"^\d+\s+","", name)
            name = re.sub(r"^(forge|spark|lore|pixel|glitch|aura|integrator|audio)\s+","", name)
            existing.append(str(f.relative_to(BASE)))
            existing_titles.add(name.strip())
    return existing, existing_titles

def save_memory(text):
    try:
        # FIX M11: Trim MEMORY.md on disk to prevent unbounded growth, keep last 3000 chars
        # Previously only read was truncated, disk file grew forever
        trimmed = text[-3000:] if len(text) > 3000 else text
        MEMORY_FILE.write_text(f"# STUDIO MEMORY v6 - {datetime.now()}\n\n{trimmed}\n", encoding="utf-8")
        # Also enforce max file size 10KB
        if MEMORY_FILE.stat().st_size > 10240:
            # Keep last 10KB
            content = MEMORY_FILE.read_text(encoding="utf-8")
            MEMORY_FILE.write_text(content[-10240:], encoding="utf-8")
    except: pass

def extract_code_from_response(result, primary="python"):
    """FIX C5: Strip markdown, code fences, <think> blocks, prose - worker path"""
    if not result:
        return result
    # Remove <think>...</think> blocks (deepseek-r1 reasoning)
    result = re.sub(r"<think>.*?</think>", "", result, flags=re.DOTALL | re.IGNORECASE)
    # Remove <thinking> blocks
    result = re.sub(r"<thinking>.*?</thinking>", "", result, flags=re.DOTALL | re.IGNORECASE)

    # Try to extract fenced code block for primary language
    # Look for ```python ... ``` or ```<primary> ... ```
    # Case insensitive search for primary
    lower_res = result.lower()
    # Try primary-specific fence
    for lang_tag in [primary.lower(), "python", "cpp", "c++", "c#", "csharp", "lua", "gdscript", "rust", "javascript", "js", "typescript", "ts"]:
        fence = f"```{lang_tag}"
        if fence in lower_res:
            # Find in original case-insensitive but extract from original
            idx = lower_res.find(fence)
            if idx != -1:
                after = result[idx+len(fence):]
                # Skip possible newline after language tag
                # Extract until closing ```
                end_idx = after.find("```")
                if end_idx != -1:
                    code = after[:end_idx]
                    # Strip first line if it's just language identifier left
                    code = code.strip()
                    # Remove leading/trailing extra markdown
                    if len(code) > 10:  # FIX C5 Audit4: lowered from 50 to 10 - short helper classes valid
                        return code.strip()

    # Fallback: extract first generic code block ``` ... ```
    if "```" in result:
        parts = result.split("```")
        # parts[1], parts[3], etc. are code blocks
        for i in range(1, len(parts), 2):
            code_candidate = parts[i]
            # Remove first line if it's a language identifier
            lines = code_candidate.splitlines()
            if lines and lines[0].strip().lower() in ["python","cpp","c++","c#","csharp","lua","gdscript","rust","javascript","js","typescript","ts","gd","csharp"]:
                code_candidate = "\n".join(lines[1:])
            code_candidate = code_candidate.strip()
            if len(code_candidate) > 10:  # FIX C5: lowered from 50 to 10 code length
                return code_candidate

    # If no fences, return cleaned result (FIX C5: was returning original.strip() discarding <think> stripping)
    return result.strip()

def _norm_title(s):
    """Normalize a title for comparison: alnum-only tokens, lowercase."""
    return re.sub(r"[^a-z0-9 ]", " ", s.lower()).split()

def titles_similar(a, b):
    """Real similarity metric (replaces pure containment - Audit M7).
    A new task title is a duplicate of an existing one when:
      - normalized strings are identical, OR
      - token Jaccard >= 0.8, OR
      - SequenceMatcher ratio >= 0.85
    Verified against M7's over-blocking cases: with 'save system' present,
    'Save System Cloud Sync' (0.67), 'Autosave System' (0.33) and 'System'
    (0.5) must NOT match, while true repeats and trivial renames must."""
    if not a or not b:
        return False
    na, nb = a.strip().lower(), b.strip().lower()
    if na == nb:
        return True
    ta, tb = set(_norm_title(a)), set(_norm_title(b))
    if not ta or not tb:
        return False
    if ta == tb:  # same words, different order/spacing e.g. "Save-System" vs "save system"
        return True
    jacc = len(ta & tb) / len(ta | tb)
    if jacc >= 0.8 and min(len(ta), len(tb)) >= 2:
        return True
    if difflib.SequenceMatcher(None, "".join(sorted(ta)), "".join(sorted(tb))).ratio() >= 0.9:
        return True
    return False

def strip_thinking(text):
    """Remove <think>/<thinking> blocks without touching anything else.
    Used as the safe .md fallback so GLITCH (deepseek-r1) never lands raw
    reasoning blocks in output/qa/*.md (C5 regression in the md branch)."""
    if not text:
        return text
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<thinking>.*?</thinking>", "", text, flags=re.DOTALL | re.IGNORECASE)
    return text.strip()


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

def snapshot_gdd(reason="change"):
    """Archive every GDD state that triggers a (re)build so each rebuild is
    attributable to the edit that caused it. GDD itself stays read-only -
    we only copy FROM it."""
    try:
        hist = BASE / "gdd_history"
        hist.mkdir(exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        dest = hist / f"GDD_{stamp}_{random_suffix()}.md"
        shutil.copy(GDD_FILE, dest)
        log(f"GDD snapshot saved ({reason}): {dest.name}", "GDD-HISTORY")
        return dest
    except Exception as e:
        log(f"GDD snapshot failed ({reason}): {e}", "GDD-HISTORY")
        return None

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

    if main_path.exists() and main_path.stat().st_size > 10:  # FIX N1: Lowered from 100 to 10, 44-char games valid
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
print("Your fragments are in output/ - check output/ folder")
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
    log(f"Fallback build created: {main_path} - no valid LLM main existed, placeholder written instead", "BUILD")

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
    preflight_models()

    tasks = []
    if TASKS_FILE.exists():
        try:
            tasks = json.loads(read_file(TASKS_FILE))
            # FIX C4: Reset any in_progress tasks left from crash/Ctrl-C to pending to avoid deadlock
            reset_count = 0
            for t in tasks:
                if t.get("status") == "in_progress":
                    t["status"] = "pending"
                    reset_count += 1
            if reset_count > 0:
                log(f"Reset {reset_count} in_progress tasks to pending (crash recovery) - fixes deadlock", "RECOVERY")
                TASKS_FILE.write_text(json.dumps(tasks, indent=2), encoding="utf-8")
            log(f"Loaded {len(tasks)} tasks", "MEMORY")
        except Exception as e:
            log(f"Failed to load tasks.json: {e}, resetting", "ERROR")
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
                snapshot_gdd("gdd_changed")
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
            # FIX H2: Read system_requirements.json if exists (produced by GUI New Project)
            sys_reqs_text = ""
            sys_reqs_path = BASE / "system_requirements.json"
            if sys_reqs_path.exists():
                try:
                    sys_reqs_data = json.loads(sys_reqs_path.read_text(encoding="utf-8"))
                    # Build summary for AURA
                    sys_lines = []
                    for s in sys_reqs_data.get("systems", [])[:12]:
                        needs = s.get("needs", {})
                        sys_lines.append(f"- {s.get('name')}: code={needs.get('code',[])}, art={needs.get('art',[])}, audio={needs.get('audio',[])}")
                    sys_reqs_text = "\nSystem Asset Lists (from GUI New Project, AURA must follow):\n" + "\n".join(sys_lines)
                    log(f"Loaded system_requirements.json with {len(sys_reqs_data.get('systems',[]))} systems", "SYSREQ")
                except Exception as e:
                    log(f"Failed to read system_requirements.json: {e}", "SYSREQ")

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
                        # Use the CANONICAL extractor (same as worker path) instead of a
                        # third divergent implementation that drifted out of sync twice
                        main_path = BUILD_DIR / f"main{ext}"
                        code = extract_code_from_response(result, primary)
                        if code and len(code.strip()) > 10:
                            main_path.write_text(code, encoding="utf-8")
                            log(f"Build {main_path.name} extracted from LLM ({len(code)} chars)", "BUILD")
                        else:
                            log("Integrator output had no usable code block - fallback will handle", "BUILD")
                    
                    ensure_build_runnable(ext, run_cmd, engine_mode, gdd_text)

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
                    # Post-build self-check (the two-line check from audits 3/4, made permanent)
                    try:
                        sc = subprocess.run([sys.executable, str(BASE / "tools" / "smoke_check.py")], timeout=30, capture_output=True, text=True, cwd=str(BASE))
                        for line in (sc.stdout or "").strip().splitlines()[:12]:
                            log(f"SMOKE: {line}", "SMOKE")
                    except Exception as sc_err:
                        log(f"Smoke check could not run: {sc_err}", "SMOKE")
                    inbox_directive_global = ""
                    time.sleep(10)
                    continue

                except Exception as e:
                    log(f"Build failed: {e}", "ERROR")
                    ensure_build_runnable(ext, run_cmd, engine_mode, gdd_text)
                    time.sleep(5)
                    continue

            # Planning - only missing
            aura_system = SYSTEM.get("aura","") + f"\n\n{engine_instruction}\nLanguage: {full_lang} primary {primary} ext {ext}\nGame Type: {game_type}\n\nCRITICAL: Existing: {titles_list}\nDo NOT re-plan existing unless GDD says IMPROVE/REDO/REBUILD\nEngine={engine_mode} Language={full_lang} Type={game_type} must be respected\nNeed diversity: at least 1 FORGE, 1 SPARK, 1 LORE, 1 PIXEL, 1 GLITCH, 1 AUDIO if missing in output"

            inbox_part = f"\nHUMAN DIRECTIVE (GDD untouched): {inbox_directive_global}\n" if inbox_directive_global else ""

            aura_prompt = f"""
You are AURA supervisor. GDD READ ONLY.

MEMORY:
{memory_summary[-2500:]}

GDD (READ ONLY):
{gdd_text[:4500]}
{inbox_part}

{sys_reqs_text}

OUTPUT INDEX - Already have (DO NOT RE-PLAN unless IMPROVE/REDO):
{output_index}
Titles: {titles_list}

COMPLETED:
{completed_str}

ENGINE: {engine_mode} - {engine_instruction}
LANGUAGE: {full_lang} primary {primary} ext {ext} - Build files must use {ext}
GAME TYPE: {game_type}

TASK: Plan ONLY missing features not in output index, following system asset lists if present. 3-5 small isolated tasks max, must include diverse roles (at least 1 FORGE, 1 SPARK, 1 LORE, 1 PIXEL, 1 GLITCH if missing).
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
                # FIX M10: Include output filenames IDs to avoid collision after Fresh Start
                existing_ids = []
                for f in OUTPUT_DIR.rglob("*.*"):
                    # Extract leading digits like 01_ from filename
                    m = re.match(r"^(\d+)_", f.name)
                    if m:
                        try:
                            existing_ids.append(int(m.group(1)))
                        except:
                            pass
                all_ids = [t.get("id",0) for t in tasks] + existing_ids
                next_id = max(all_ids, default=0) + 1

                improve_mode = any(k in gdd_text.lower() for k in ["improve","redo","rebuild"])
                for nt in new_tasks:
                    if "id" not in nt:
                        nt["id"] = next_id
                        next_id += 1
                    is_dup = False
                    # FIX M7: real similarity (titles_similar) instead of raw
                    # containment that over-blocked legit follow-up work
                    for ex in existing_titles:
                        if titles_similar(nt.get("title",""), ex):
                            if not improve_mode:
                                is_dup = True
                                log(f"Dedup skip: {nt['title']} similar to existing {ex}", "DEDUP")
                                break
                    if not is_dup:
                        nt["status"] = "pending"
                        nt["attempts"] = 0
                        nt["created_at"] = str(datetime.now())
                        nt["prompt"] = nt["prompt"] + f"\n\nENGINE RULE: {engine_instruction}\nLANGUAGE RULE: Build in {full_lang} primary {primary} ext {ext}\nSTRICT: {nt['role']} ONLY."
                        filtered.append(nt)

                # FIX H4: Role diversity - force at least 1 of each missing role if output missing those roles
                # Count existing roles in output/
                existing_roles = set()
                for f in existing_files:
                    # Extract role from filename like 01_forge_...
                    parts = f.split("_")
                    if len(parts) >= 2:
                        existing_roles.add(parts[1].lower())
                
                missing_roles = []
                for required_role in ["forge","spark","lore","pixel","glitch","audio"]:
                    # Check if role folder has files
                    role_folder = BASE / "output" / {"forge":"code","spark":"code","lore":"lore","pixel":"art","glitch":"qa","audio":"audio"}.get(required_role,"code")
                    has_files = False
                    if role_folder.exists():
                        has_files = any(role_folder.glob("*.*"))
                    if not has_files and required_role not in [t.get("role") for t in filtered]:
                        missing_roles.append(required_role)
                
                if missing_roles and len(filtered) < 5:
                    log(f"Role diversity fix: Missing roles {missing_roles} not in plan and not in output - forcing add", "DIVERSITY")
                    for mr in missing_roles[:2]:  # Add up to 2 missing roles
                        if mr not in [t.get("role") for t in filtered]:
                            filtered.append({
                                "id": next_id,
                                "role": mr,
                                "title": f"Missing {mr} system for {game_type} {full_lang}",
                                "prompt": f"Create {mr} system for {game_type} game in {full_lang}. This role was missing in output/ and is required for full team diversity.",
                                "status": "pending",
                                "attempts": 0,
                                "created_at": str(datetime.now())
                            })
                            next_id += 1

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

        # FIX N4/C-cap: Cap check must be above IDLE check to be reachable - was dead code before
        # Parse scope from MEMORY or GDD
        MAX_TASKS = 25
        try:
            mem_text = open(MEMORY_FILE, encoding="utf-8").read().lower() + " " + open(GDD_FILE, encoding="utf-8").read().lower()
            if "large (50" in mem_text or "50 tasks" in mem_text:
                MAX_TASKS = 50
            elif "small (10" in mem_text:
                MAX_TASKS = 10
        except Exception:
            pass
        done_count = len([t for t in tasks if t.get("status")=="done"])
        pending_count = len([t for t in tasks if t.get("status") in ["pending","failed","in_progress"]])
        if done_count >= MAX_TASKS:
            # FIX N3: Idempotency - only export if DONE doesn't exist
            if (BUILD_DIR / "DONE").exists():
                log(f"Max tasks cap {done_count} >= {MAX_TASKS} reached and DONE exists - IDLE (prevents disk-filler)", "CAP")
                time.sleep(15)
                continue
            if pending_count == 0:
                log(f"Max tasks cap {done_count} >= {MAX_TASKS} reached - true finish - will export build if exists and go IDLE", "CAP")
                if (BUILD_DIR / "main.py").exists() or any((BUILD_DIR / f"main{e}").exists() for e in [".cpp",".cs",".lua",".gd",".rs",".js",".ts"]):
                    export_build(f"CAP_{MAX_TASKS}")
                    if not (BUILD_DIR / "DONE").exists():
                        (BUILD_DIR / "DONE").write_text(f"DONE cap {MAX_TASKS} reached at {datetime.now()} - {done_count} tasks done", encoding="utf-8")
                else:
                    log("Cap reached but no build/main.* exists - NOT writing DONE, will trigger build next cycle", "CAP")
                time.sleep(15)
                continue

        if not pending:
            if not (BUILD_DIR / "DONE").exists() and len(existing_files) >= 1:
                time.sleep(2)
                continue
            log("No pending tasks. IDLE waiting for GDD change - TRUE FINISH, not looping", "IDLE")
            time.sleep(15)
            continue

        # === FIX H1: Parallel execution - select batch that fits VRAM ===
        # VRAM estimates from audit
        VRAM_MAP = {
            "qwen3:14b": 9.0,
            "devstral:24b": 14.0,
            "qwen2.5-coder:14b": 8.8,
            "gemma3:12b": 7.8,
            "deepseek-r1:14b": 9.5,
            "gemma3:4b": 3.3,
            "qwen3:8b": 5.0
        }
        MAX_VRAM = 15.0  # For 16GB VRAM, leave 1GB headroom
        MAX_PARALLEL = 2  # As per GUI label
        
        # Select parallel batch
        parallel_batch = []
        used_models = set()
        vram_used = 0.0
        for t in pending[:5]:  # Look at first 5 pending
            role = t.get("role","forge")
            model = TEAM.get(role, "qwen3:14b")
            # If model already in batch, VRAM already counted
            vram_needed = 0 if model in used_models else VRAM_MAP.get(model, 9.0)
            if vram_used + vram_needed <= MAX_VRAM and len(parallel_batch) < MAX_PARALLEL:
                parallel_batch.append(t)
                used_models.add(model)
                vram_used += vram_needed
        
        if len(parallel_batch) > 1:
            log(f"Parallel batch selected: {len(parallel_batch)} tasks, VRAM {vram_used:.1f}GB / {MAX_VRAM}GB - {', '.join([t['title'][:20] for t in parallel_batch])}", "PARALLEL")
        else:
            parallel_batch = [pending[0]]

        # FIX H1: True parallel execution via ThreadPoolExecutor - max 2 models in 16GB VRAM
        # If parallel batch >1, process in parallel, else process single
        if len(parallel_batch) > 1:
            log(f"Executing parallel batch of {len(parallel_batch)} tasks in parallel (ThreadPoolExecutor)", "PARALLEL")

            def process_one_task(t_item):
                # FIX H1a Audit5: Move breaker + in_progress marking BEFORE call_ollama to stop 3 duplicate files
                # Previously attempts incremented after success, so failing task would write file 3 times before breaker
                if t_item.get("attempts",0) >= 3:
                    return (t_item, None, "skipped_breaker")
                t_item["status"] = "in_progress"
                t_item["attempts"] = t_item.get("attempts",0) + 1
                # Isolated processing for one task - no shared state except file writes which are unique due to random suffix
                role = t_item.get("role","forge")
                model = TEAM.get(role, "qwen3:14b")
                gdd_snip = read_file(GDD_FILE)[:3500]
                full_l, prim, ext_, run_c = detect_language(gdd_snip)
                eng_mode, eng_instr = detect_engine_mode(gdd_snip)
                base_sys = SYSTEM.get(role,"")
                if eng_mode == "custom":
                    base_sys = base_sys.replace("Unity","custom engine").replace("Unreal","custom engine").replace("Godot","custom")
                    base_sys += f"\n\n{eng_instr}\nSTRICTLY NO Unity/Unreal.\nLANGUAGE: {full_l} primary {prim} ext {ext_} - Must respect."
                worker_prompt = f"""
GDD (READ ONLY):
{gdd_snip}

TASK ({role} ONLY) in {full_l} primary {prim} ext {ext_}:
Title: {t_item['title']}
Details: {t_item['prompt']}

ENGINE MODE: {eng_mode}
{eng_instr}
LANGUAGE: {full_l} primary {prim} ext {ext_} -> File must be *{ext_}
GAME TYPE: {detect_game_type(gdd_snip)}

RULES: Stay lane, respect engine+language+type, output file-ready result in {full_l}. Max 500 lines, 25KB, 100 chars line. GDD read-only.
"""
                result = call_ollama(model, base_sys, worker_prompt, 350)
                if not result:
                    return (t_item, None, "failed")
                # Unique naming + extract
                ext_to_use = ext_for_role(role, ext_)
                folder_to_use = folder_for_role(role)
                safe_file_title = "".join(c if c.isalnum() else "_" for c in t_item['title'])[:30]
                rand_suf = random_suffix()
                fname = f"{t_item.get('id',99):02d}_{role}_{safe_file_title}_{rand_suf}{ext_to_use}"
                fpath = OUTPUT_DIR / folder_to_use / fname
                fpath.parent.mkdir(parents=True, exist_ok=True)
                cleaned = extract_code_from_response(result, prim)
                if ext_to_use == ".md" and len(cleaned) < 50:
                    cleaned = strip_thinking(result)  # think-stripped, never raw reasoning blocks
                fpath.write_text(cleaned, encoding="utf-8")
                return (t_item, (fpath, cleaned, result), "done")

            # Execute parallel
            results = []
            with concurrent.futures.ThreadPoolExecutor(max_workers=len(parallel_batch)) as executor:
                future_to_task = {executor.submit(process_one_task, t): t for t in parallel_batch}
                for future in concurrent.futures.as_completed(future_to_task):
                    try:
                        task_item, res, status = future.result()
                        results.append((task_item, res, status))
                        log(f"Parallel task done: {task_item['title']} -> {status}", "PARALLEL")
                    except Exception as e:
                        t = future_to_task[future]
                        log(f"Parallel task {t['title']} failed: {e}", "ERROR")
                        results.append((t, None, "failed"))

            # Save all results to tasks.json and validate each sequentially (AURA validation sequential to avoid VRAM spike)
            for task_item, res, status in results:
                # Find task in main tasks list
                for tt in tasks:
                    if tt.get("id") == task_item.get("id"):
                        if status == "skipped_breaker":
                            # FIX: old code fell into the res-is-None branch and marked the
                            # task "failed" - and "failed" tasks are re-selected as pending
                            # every cycle, so a breaker-skipped task was re-dispatched in a
                            # 2-second tight loop forever. Mark done like the sequential path.
                            tt["status"] = "done"
                            tt["note"] = "Skipped by loop breaker (parallel)"
                            log(f"LOOP BREAKER: Skip {tt['title']} after {tt.get('attempts',0)} attempts (parallel)", "BREAKER")
                        elif status == "failed" or res is None:
                            tt["status"] = "failed"
                        else:
                            tt["status"] = "done"
                            tt["output_file"] = str(res[0])
                            # attempts already incremented BEFORE the call in
                            # process_one_task - do NOT increment again (was double-count)
                        break
            TASKS_FILE.write_text(json.dumps(tasks, indent=2), encoding="utf-8")

            # Validate each result sequentially
            for task_item, res, status in results:
                if status == "failed" or res is None:
                    continue
                fpath, cleaned, raw_result = res
                gdd_snip = read_file(GDD_FILE)[:2000]
                full_l, prim, ext_, run_c = detect_language(gdd_snip)
                eng_mode, eng_instr = detect_engine_mode(gdd_snip)
                validate_prompt = f"""GDD: {gdd_snip[:2000]}\nTask: {task_item['title']} Role: {task_item.get('role')} Expected: {task_item['prompt']}\nOutput: {raw_result[:3000]}\nCheck 1) role lane 2) engine 3) language\nOutput JSON ONLY: {{"verdict":"PASS/FAIL","reason":"...","fix":"..."}}"""
                validation = call_ollama(TEAM["aura"], SYSTEM.get("aura",""), validate_prompt, 200)
                try:
                    if validation:
                        import json as _json
                        raw_v = validation
                        s = raw_v.find("{")
                        e = raw_v.rfind("}")+1
                        if s != -1:
                            raw_v = raw_v[s:e]
                        v = _json.loads(raw_v)
                        verdict = v.get("verdict","PASS").upper()
                        if "FAIL" in verdict:
                            for tt in tasks:
                                if tt.get("id") == task_item.get("id") and tt.get("attempts",0) < 3:
                                    tt["status"] = "pending"
                                    tt["prompt"] = tt["prompt"] + f"\nCORRECTION: {v.get('fix')}"
                        TASKS_FILE.write_text(json.dumps(tasks, indent=2), encoding="utf-8")
                except Exception as e:
                    log(f"Validation parse fail parallel: {e}", "VALIDATE")
            time.sleep(2)
            continue
        else:
            # Sequential fallback - only one task in batch
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

        # Unique naming with random suffix to avoid overwrite - v6 fix for repeat naming - FIXED C1: pass ext not primary
        # FIXED C5: Extract code from LLM prose before writing
        ext_to_use = ext_for_role(role, ext)
        folder_to_use = folder_for_role(role)
        safe_file_title = "".join(c if c.isalnum() else "_" for c in task['title'])[:30]
        rand_suf = random_suffix()
        fname = f"{task.get('id',99):02d}_{role}_{safe_file_title}_{rand_suf}{ext_to_use}"
        fpath = OUTPUT_DIR / folder_to_use / fname
        # FIX C5 + H7: Ensure parent dir exists and strip prose
        fpath.parent.mkdir(parents=True, exist_ok=True)
        cleaned_result = extract_code_from_response(result, primary)
        # For lore/glitch/qa roles (.md), keep original if cleaning would remove too much? But still strip <think>
        if ext_to_use == ".md" and len(cleaned_result) < 50:
            cleaned_result = strip_thinking(result)  # safe raw fallback: think-stripped (old comment lied - raw result still carried <think> blocks)
        fpath.write_text(cleaned_result, encoding="utf-8")
        log(f"{role.upper()} DONE -> {fpath} ({len(cleaned_result)} chars, raw {len(result)} chars) [{full_lang}]", "DONE")

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
        verdict = "PASS"  # FIX H8: Ensure verdict defined even if validation fails
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
                # Cap in-process growth - disk file is trimmed by save_memory,
                # but this string lived for the whole process run before
                if len(memory_summary) > 4000:
                    memory_summary = memory_summary[-3000:]
                save_memory(memory_summary)
            else:
                # No validation response at all - treat as failed, retry if attempts left, not silent PASS
                log("Validation response empty - will retry if attempts remain", "VALIDATE")
                if task["attempts"] < 3:
                    task["status"] = "pending"
                else:
                    task["status"] = "done"
                    task["note"] = "Validation empty, forced done after 3 attempts"
                task["output_file"] = str(fpath)
                TASKS_FILE.write_text(json.dumps(tasks, indent=2), encoding="utf-8")
        except Exception as e:
            # FIX H8: Don't silently PASS on first parse fail - retry if attempts remain
            log(f"Validation parse fail: {e} - will retry if attempts remain", "VALIDATE")
            if task.get("attempts",0) < 3:
                task["status"] = "pending"
                task["prompt"] = task["prompt"] + "\nVALIDATION PARSE FAILED, retry validating strictly."
            else:
                log("Validation parse failed 3 times, forcing PASS to prevent deadlock (was silent PASS after 1st before)", "VALIDATE")
                task["status"] = "done"
                verdict = "PASS"
            task["output_file"] = str(fpath)
            TASKS_FILE.write_text(json.dumps(tasks, indent=2), encoding="utf-8")

        time.sleep(2)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log("Stopped - Memory saved, GDD untouched. Resume via 2. Start Team.bat or GUI", "STOP")
