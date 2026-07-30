#!/usr/bin/env python3
"""
Minimal GUI v2 - Ai Team Control Panel - No Manual File Nonsense, No Direct GDD Editing Required
- All mandatory inputs via GUI: Engine, Language, Game Type, Genre, Pitch, etc. -> GDD auto-generated focused on pitch/ideas
- New Project / Continue Project buttons - AURA makes system asset lists at new project start
- Parallel model execution status
- Offline, Tkinter, no deps
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, simpledialog
import json
import subprocess
import threading
import time
from pathlib import Path
import os
import sys
import shutil
import random
from datetime import datetime

BASE = Path(__file__).resolve().parent  # resolve() so every path is absolute regardless of launch CWD
GDD_CANDIDATES = [BASE / "5. GDD.md", BASE / "4. GDD.md", BASE / "GDD.md"]
TASKS_FILE = BASE / "tasks.json"
MEMORY_FILE = BASE / "MEMORY.md"
SYSTEM_REQS_FILE = BASE / "system_requirements.json"
LOG_FILE = BASE / "logs.txt"
LIVE_STATUS = BASE / "live_status.txt"
PAUSE_FILE = BASE / "PAUSE"
BUILD_DIR = BASE / "build"
OUTPUT_DIR = BASE / "output"
BUILDS_ARCHIVE = BASE / "builds"

def get_gdd_path():
    for c in GDD_CANDIDATES:
        if c.exists():
            return c
    return BASE / "5. GDD.md"

def detect_from_gdd():
    # FIX M4/M5: Import detection from studio.py instead of reimplementing divergent logic
    # This ensures GUI and orchestrator agree on Engine/Language/Game Type
    p = get_gdd_path()
    txt = ""
    if p.exists():
        try:
            txt = p.read_text(encoding="utf-8")
        except:
            txt = ""
    try:
        # Import from studio.py for single source of truth
        import sys
        sys.path.insert(0, str(BASE))
        from studio import detect_language, detect_game_type, detect_engine_mode
        full_lang, primary, ext, run_cmd = detect_language(txt)
        gtype = detect_game_type(txt)
        engine_mode, _ = detect_engine_mode(txt)
        # Map engine_mode to display
        engine = "Custom from scratch" if engine_mode == "custom" else "Standard"
        # Try to get more specific from GDD ENGINE field
        for line in txt.splitlines():
            if "engine:" in line.lower():
                eng_line = line.split(":",1)[1].strip()[:40]
                if eng_line:
                    engine = eng_line
                break
        return engine, full_lang, gtype, txt
    except Exception:
        # Fallback to old logic if import fails
        lower = txt.lower()
        engine = "Custom from scratch"
        if "unity" in lower and "avoid unity" not in lower and "no unity" not in lower:
            engine = "Unity"
        elif "godot" in lower and "avoid godot" not in lower:
            engine = "Godot"
        lang = "Python"
        if "language:" in lower:
            for line in txt.splitlines():
                if "language:" in line.lower():
                    lang = line.split(":",1)[1].strip()[:40]
                    break
        gtype = "2D"
        if any(k in lower for k in ["3d", "tether", "ragdoll"]):
            gtype = "3D"
        return engine, lang, gtype, txt

class AiTeamGUIv2:
    def __init__(self, root):
        self.root = root
        root.title("Ai Team v6 - Full Studio Control - No GDD Direct Editing Needed")
        root.geometry("1250x800")

        # Top bar
        top = ttk.Frame(root, padding=5)
        top.pack(fill=tk.X)
        self.gdd_label = ttk.Label(top, text="Loading GDD...", font=("Segoe UI", 9, "bold"))
        self.gdd_label.pack(side=tk.LEFT)
        ttk.Button(top, text="Refresh All", command=self.refresh_all).pack(side=tk.RIGHT, padx=2)
        ttk.Button(top, text="Open Builds Archive", command=self.open_builds_archive).pack(side=tk.RIGHT, padx=2)

        # Main notebook for New Project vs Continue
        notebook = ttk.Notebook(root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Tab 1 - New Project Setup (All mandatory inputs via GUI, so GDD can focus on pitch)
        self.tab_new = ttk.Frame(notebook, padding=10)
        notebook.add(self.tab_new, text="New Project Setup (No Direct GDD Editing Needed)")

        # Form for mandatory stuff
        form = ttk.Frame(self.tab_new)
        form.pack(fill=tk.X, pady=5)

        # Row 1: Project Name, Engine, Language, Game Type
        r1 = ttk.Frame(form)
        r1.pack(fill=tk.X, pady=2)
        ttk.Label(r1, text="Project Name:").pack(side=tk.LEFT)
        self.entry_project = ttk.Entry(r1, width=20)
        self.entry_project.pack(side=tk.LEFT, padx=5)
        self.entry_project.insert(0, "TideLoop")

        ttk.Label(r1, text="Engine:").pack(side=tk.LEFT, padx=(10,0))
        self.combo_engine = ttk.Combobox(r1, values=["Custom from scratch", "Unity", "Godot", "None", "Unreal (if you must)"], width=20, state="readonly")
        self.combo_engine.set("Custom from scratch")
        self.combo_engine.pack(side=tk.LEFT, padx=5)

        ttk.Label(r1, text="Language:").pack(side=tk.LEFT, padx=(10,0))
        self.combo_lang = ttk.Combobox(r1, values=["Python", "C++", "C#", "C# + Lua", "Lua", "GDScript", "Rust", "JavaScript", "TypeScript", "Python + C++", "C++ + Lua"], width=15, state="readonly")
        self.combo_lang.set("Python")
        self.combo_lang.pack(side=tk.LEFT, padx=5)

        ttk.Label(r1, text="Game Type:").pack(side=tk.LEFT, padx=(10,0))
        self.combo_type = ttk.Combobox(r1, values=["2D", "2D Pixel", "3D", "3D Fishing", "Text", "GUI", "GUI Puzzle"], width=12, state="readonly")
        self.combo_type.set("3D")
        self.combo_type.pack(side=tk.LEFT, padx=5)

        # Row 2: Genre, Scope
        r2 = ttk.Frame(form)
        r2.pack(fill=tk.X, pady=2)
        ttk.Label(r2, text="Genre:").pack(side=tk.LEFT)
        self.entry_genre = ttk.Entry(r2, width=20)
        self.entry_genre.pack(side=tk.LEFT, padx=5)
        self.entry_genre.insert(0, "Roguelite Fishing + Time Loop")

        ttk.Label(r2, text="Scope:").pack(side=tk.LEFT, padx=(10,0))
        self.combo_scope = ttk.Combobox(r2, values=["Small (10 tasks)", "Medium (25 tasks) - Recommended", "Large (50 tasks)"], width=30, state="readonly")
        self.combo_scope.set("Medium (25 tasks) - Recommended")
        self.combo_scope.pack(side=tk.LEFT, padx=5)

        ttk.Label(r2, text="Art Style:").pack(side=tk.LEFT, padx=(10,0))
        self.entry_art = ttk.Entry(r2, width=20)
        self.entry_art.pack(side=tk.LEFT, padx=5)
        self.entry_art.insert(0, "Cozy dark, low-poly")

        # Pitch
        ttk.Label(form, text="Elevator Pitch (1 sentence, GDD focused on ideas):").pack(anchor=tk.W, pady=(10,0))
        self.text_pitch = scrolledtext.ScrolledText(form, height=3, wrap=tk.WORD, font=("Segoe UI", 9))
        self.text_pitch.pack(fill=tk.X, pady=2)
        self.text_pitch.insert(tk.END, "You are a fisherman cursed to repeat 3 days. Ocean changes each loop. Catch 7 impossible fish to break curse.")

        # Core Loop
        ttk.Label(form, text="Core Loop (e.g., Wake -> Fish -> Sell -> Explore -> Sleep -> Loop):").pack(anchor=tk.W)
        self.text_loop = scrolledtext.ScrolledText(form, height=3, wrap=tk.WORD, font=("Segoe UI", 9))
        self.text_loop.pack(fill=tk.X, pady=2)
        self.text_loop.insert(tk.END, "1. Wake (Day 1/2/3) -> 2. Fish (timing mini-game) -> 3. Sell/Craft Bait -> 4. Explore islands/dialogue -> 5. Sleep (loop resets but you keep knowledge)")

        # Features
        ttk.Label(form, text="Key Features (5-15, one per line, will become tasks + system asset lists):").pack(anchor=tk.W)
        self.text_features = scrolledtext.ScrolledText(form, height=6, wrap=tk.WORD, font=("Segoe UI", 9))
        self.text_features.pack(fill=tk.X, pady=2)
        self.text_features.insert(tk.END, "Tether System: Bodyguards tethered to VIP, tension builds with distance\nStress Meter: VIP stress from tether tension, hazards, panic dialogue\nContract Progression Lock: Unlock contracts by prerequisites\nSave System: Cloud sync + daily contracts (local JSON)\nLeaderboard: Local + Steam stub\nVIP Personality: Diva, Panicker, etc. with dialogue variations\nFishing Mini-game: Timing QTE\nSteam API: Achievements, leaderboards, cloud saves\nServer: Dedicated server stub for multiplayer tether sync")

        # Buttons for New Project flow
        btn_frame = ttk.Frame(form)
        btn_frame.pack(fill=tk.X, pady=10)
        ttk.Button(btn_frame, text="1. Generate GDD from GUI Inputs (No Direct GDD Editing Needed)", command=self.generate_gdd_from_gui, width=60).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="2. New Project - AURA Makes System Asset Lists + Starts Team", command=self.new_project, width=50).pack(side=tk.LEFT, padx=5)

        ttk.Label(form, text="This will: Generate 5. GDD.md focused on pitch/ideas (Engine/Language/Type from GUI, not manual), then AURA will make lists for each system (what art/audio/code needed per system), save to system_requirements.json, then follow that list to assign tasks. True start>finish.", wraplength=1000, font=("Segoe UI", 8)).pack(anchor=tk.W, pady=5)

        # Tab 2 - Continue Project + Control Panel
        self.tab_continue = ttk.Frame(notebook, padding=5)
        notebook.add(self.tab_continue, text="Continue Project + Control Panel + Live Log")

        # Paned for this tab
        paned = ttk.PanedWindow(self.tab_continue, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True)

        # Left controls
        left = ttk.Frame(paned, padding=5)
        paned.add(left, weight=1)

        ttk.Label(left, text="Controls (No manual file ops)", font=("Segoe UI", 10, "bold")).pack(anchor=tk.W, pady=2)
        
        btns = [
            ("Continue Project (Load tasks.json + output/ + build/)", self.continue_project),
            ("Start Team (Live Log in new window + GUI panel)", self.start_team),
            ("Pause Team", self.pause_team),
            ("Resume Team", self.resume_team),
            ("Fresh Start (Backup output, clear tasks, keep GDD)", self.fresh_start),
            ("Force Rebuild (Delete build/DONE+main, keep output)", self.force_rebuild),
            ("Restore Output Backup (undo Fresh Start)", self.restore_backup),
            ("Edit GDD (Pitch only, Engine/Lang via GUI)", self.edit_gdd),
            ("Open Build Folder", self.open_build),
            ("Open Output Folder", self.open_output),
            ("Run Build (build/run.bat)", self.run_build),
            ("Install Check (ollama list)", self.install_check),
            ("Export MVP Build", lambda: self.export_build("MVP")),
            ("Export Alpha Build", lambda: self.export_build("Alpha")),
            ("Export Beta Build", lambda: self.export_build("Beta")),
        ]
        for txt, cmd in btns:
            ttk.Button(left, text=txt, command=cmd, width=45).pack(fill=tk.X, pady=1)

        ttk.Label(left, text="Send Directive to Director (INBOX, GDD untouched):").pack(anchor=tk.W, pady=(10,2))
        self.directive_entry = ttk.Entry(left, width=40)
        self.directive_entry.pack(fill=tk.X, pady=2)
        self.directive_entry.bind("<Return>", lambda e: self.send_directive())
        ttk.Button(left, text="Send Directive", command=self.send_directive).pack(fill=tk.X, pady=2)

        # Build status
        ttk.Separator(left, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        self.build_status = ttk.Label(left, text="Checking build...", wraplength=300, font=("Segoe UI", 9))
        self.build_status.pack(anchor=tk.W, pady=2)
        self.stats_label = ttk.Label(left, text="Stats loading...", wraplength=300, font=("Segoe UI", 8))
        self.stats_label.pack(anchor=tk.W, pady=2)

        # Parallel status
        ttk.Label(left, text="Parallel Execution Status:", font=("Segoe UI", 9, "bold")).pack(anchor=tk.W, pady=(10,0))
        self.parallel_label = ttk.Label(left, text="Parallel: Idle - Max 2 models in 16GB VRAM", wraplength=300, font=("Consolas", 8))
        self.parallel_label.pack(anchor=tk.W, pady=2)

        # Center live log
        center = ttk.Frame(paned, padding=5)
        paned.add(center, weight=3)
        ttk.Label(center, text="Live Log - Real-time (replaces type logs.txt)", font=("Segoe UI", 10, "bold")).pack(anchor=tk.W)
        self.log_text = scrolledtext.ScrolledText(center, wrap=tk.WORD, height=30, font=("Consolas", 9))
        self.log_text.pack(fill=tk.BOTH, expand=True)

        # Right tasks and system requirements
        right = ttk.Frame(paned, padding=5)
        paned.add(right, weight=2)

        ttk.Label(right, text="System Asset Lists (AURA makes at New Project start)", font=("Segoe UI", 9, "bold")).pack(anchor=tk.W)
        self.system_reqs_text = scrolledtext.ScrolledText(right, wrap=tk.WORD, height=12, font=("Consolas", 8))
        self.system_reqs_text.pack(fill=tk.BOTH, expand=True, pady=2)

        ttk.Label(right, text="Tasks (tasks.json)", font=("Segoe UI", 10, "bold")).pack(anchor=tk.W, pady=(5,0))
        self.tasks_text = scrolledtext.ScrolledText(right, wrap=tk.WORD, height=10, font=("Consolas", 8))
        self.tasks_text.pack(fill=tk.BOTH, expand=True, pady=2)

        ttk.Label(right, text="Output Files (output/)", font=("Segoe UI", 10, "bold")).pack(anchor=tk.W)
        self.output_list = tk.Listbox(right, height=10, font=("Consolas", 8))
        self.output_list.pack(fill=tk.BOTH, expand=True, pady=2)

        # Bottom status
        bottom = ttk.Frame(self.tab_continue, padding=2)
        bottom.pack(fill=tk.X, side=tk.BOTTOM)
        self.status_bar = ttk.Label(bottom, text="Idle - Ready - GDD Safe - v6 Parallel - No manual file ops", relief=tk.SUNKEN)
        self.status_bar.pack(fill=tk.X)

        # Auto refresh
        self.running = True
        self.refresh_thread = threading.Thread(target=self.auto_refresh_loop, daemon=True)
        self.refresh_thread.start()
        self.refresh_all()

    def get_gdd_path(self):
        for c in [BASE / "5. GDD.md", BASE / "4. GDD.md", BASE / "GDD.md"]:
            if c.exists():
                return c
        return BASE / "5. GDD.md"

    def refresh_all(self):
        try:
            # GDD label
            gdd_path = self.get_gdd_path()
            txt = ""
            if gdd_path.exists():
                txt = gdd_path.read_text(encoding="utf-8")
            lower = txt.lower()
            # Detect
            engine = self.combo_engine.get() if hasattr(self, 'combo_engine') else "Custom"
            lang = self.combo_lang.get() if hasattr(self, 'combo_lang') else "Python"
            gtype = self.combo_type.get() if hasattr(self, 'combo_type') else "3D"
            # From GDD if exists
            if "language:" in lower:
                for line in txt.splitlines():
                    if "language:" in line.lower():
                        lang = line.split(":",1)[1].strip()[:30]
                        break

            self.gdd_label.config(text=f"{gdd_path.name} | Engine: {engine} | Lang: {lang} | Type: {gtype} | {len(txt)} chars | Tasks: {self.count_tasks()}")

            # Build status
            main_exists = any((BASE / "build" / f"main{e}").exists() for e in [".py",".cpp",".cs",".lua",".gd",".rs",".js",".ts"])
            done_exists = (BASE / "build" / "DONE").exists()
            output_count = len(list((BASE / "output").rglob("*.*"))) if (BASE / "output").exists() else 0
            build_size = sum(f.stat().st_size for f in (BASE / "build").rglob("*") if f.is_file()) / 1024 / 1024 if (BASE / "build").exists() else 0
            self.build_status.config(text=f"Build main exists: {main_exists}\nDONE: {done_exists}\nBuild size: {build_size:.1f} MB\nOutput files: {output_count}")

            # Stats
            tasks = []
            if (BASE / "tasks.json").exists():
                try:
                    tasks = json.loads((BASE / "tasks.json").read_text(encoding="utf-8"))
                except:
                    tasks = []
            pending = len([t for t in tasks if t.get("status") in ["pending","failed","in_progress"]])
            done = len([t for t in tasks if t.get("status")=="done"])
            # Parallel estimation
            parallel_max = 2  # For 16GB VRAM, max 2 small models
            self.stats_label.config(text=f"Tasks: {len(tasks)} total\nPending: {pending}\nDone: {done}\nPAUSE: { (BASE / 'PAUSE').exists() }\nParallel Max: {parallel_max} models in 16GB VRAM")

            self.parallel_label.config(text=f"Parallel: {'Running' if pending>1 else 'Idle'} - Up to {parallel_max} models can run simultaneously within 16GB VRAM\nVRAM est: qwen3:14b=9GB, devstral:24b=14GB, gemma3:12b=7.8GB\nSafe combos: gemma3:12b+gemma3:4b=11.1GB, qwen3:8b+gemma3:12b=12.8GB")

            # System reqs
            if (BASE / "system_requirements.json").exists():
                try:
                    reqs = (BASE / "system_requirements.json").read_text(encoding="utf-8")[:2000]
                    self.system_reqs_text.delete(1.0, tk.END)
                    self.system_reqs_text.insert(tk.END, reqs)
                except: pass

            # Tasks
            if (BASE / "tasks.json").exists():
                content = (BASE / "tasks.json").read_text(encoding="utf-8")[:3000]
                self.tasks_text.delete(1.0, tk.END)
                self.tasks_text.insert(tk.END, content)

            # Output list
            self.output_list.delete(0, tk.END)
            if (BASE / "output").exists():
                for f in sorted((BASE / "output").rglob("*.*"))[:150]:
                    if f.is_file():
                        self.output_list.insert(tk.END, str(f.relative_to(BASE)))

            # Logs
            if (BASE / "logs.txt").exists():
                lines = (BASE / "logs.txt").read_text(encoding="utf-8").splitlines()[-80:]
                self.log_text.delete(1.0, tk.END)
                self.log_text.insert(tk.END, "\n".join(lines))
                self.log_text.see(tk.END)

            if (BASE / "live_status.txt").exists():
                self.status_bar.config(text=(BASE / "live_status.txt").read_text(encoding="utf-8")[:150])

        except Exception as e:
            self.status_bar.config(text=f"Refresh error: {e}")

    def auto_refresh_loop(self):
        while self.running:
            time.sleep(3)
            try:
                self.root.after(0, self.refresh_all)
            except:
                break

    def generate_gdd_from_gui(self):
        # Generate 5. GDD.md from GUI inputs so GDD can focus on pitch/ideas but mandatory fields from GUI
        try:
            project = self.entry_project.get().strip() or "My Game"
            engine = self.combo_engine.get()
            lang = self.combo_lang.get()
            gtype = self.combo_type.get()
            genre = self.entry_genre.get().strip()
            pitch = self.text_pitch.get(1.0, tk.END).strip()
            loop = self.text_loop.get(1.0, tk.END).strip()
            features = self.text_features.get(1.0, tk.END).strip()
            art = self.entry_art.get().strip()
            scope = self.combo_scope.get()

            # Map scope to task count
            scope_tasks = "25"
            if "10" in scope:
                scope_tasks = "10"
            elif "50" in scope:
                scope_tasks = "50"

            gdd_content = f"""# GAME DESIGN DOCUMENT - Generated from GUI - Focused on Pitch/Ideas
# Mandatory fields (Engine, Language, Type) came from GUI, so GDD can focus on pitch

PROJECT: {project}
GENRE: {genre} - {gtype}
ENGINE: {engine}
LANGUAGE: {lang}
ART STYLE: {art}
SCOPE: {scope} - Max {scope_tasks} tasks then DONE

ELEVATOR PITCH:
{pitch}

CORE LOOP:
{loop}

FEATURES:
{features}

---
## SYSTEM REQUIREMENTS - Will be auto-generated by AURA at New Project start
# AURA will make lists for each system: what art/audio/code needed per system, then follow that list

TECH:
Engine: {engine} (from GUI, respected)
Language: {lang} (from GUI, any language supported: Python, C++, C#, Lua, etc.)
Art Style: {art}
Game Type: {gtype} (2D/3D/Text/GUI auto-detected)
Scope: {scope}

## NOTES:
- This GDD was generated from GUI so you don't need to edit GDD directly for mandatory stuff
- Edit pitch/ideas here or via GUI, Engine/Language/Type via GUI dropdowns
- System asset lists will be generated by AURA at New Project start into system_requirements.json
- GDD is READ ONLY for system - never modified by system, only read

## ORIGINAL IDEA FOCUS:
{pitch}

CORE SYSTEMS FROM FEATURES:
{features}
"""

            gdd_path = BASE / "5. GDD.md"
            gdd_path.write_text(gdd_content, encoding="utf-8")
            messagebox.showinfo("GDD Generated", f"Generated {gdd_path.name} from GUI inputs\nEngine: {engine}\nLanguage: {lang}\nType: {gtype}\n\nGDD now focused on pitch/ideas, mandatory fields from GUI.")
            self.refresh_all()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def new_project(self):
        # New Project: Generate GDD from GUI if not exists, then make system asset lists via AURA, then start
        if not messagebox.askyesno("New Project", "This will:\n1. Generate GDD from GUI inputs (if you clicked Generate GDD, it uses that, else uses current 5. GDD.md)\n2. Ask AURA to make system asset lists for each system (what art/audio/code needed per system) -> system_requirements.json\n3. Clear tasks.json, MEMORY.md, build/DONE for fresh start>finish\n4. Follow that list to assign tasks\n\nYour old output/ will be backed up to output_backup_*\n\nContinue?"):
            return
        try:
            # Step 1: Ensure GDD exists from GUI
            gdd_path = self.get_gdd_path()
            if not gdd_path.exists() or gdd_path.stat().st_size < 100:
                self.generate_gdd_from_gui()

            # Step 2: Backup output/
            import datetime, random
            backup_name = f"output_backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}_{random.randint(0,0xFFFF):04x}"
            if (BASE / "output").exists():
                shutil.copytree(BASE / "output", BASE / backup_name, dirs_exist_ok=True)

            # Step 3: Clear for fresh start
            (BASE / "tasks.json").write_text("[]", encoding="utf-8")
            (BASE / "MEMORY.md").write_text(f"# Fresh Start New Project {datetime.datetime.now()}\n", encoding="utf-8")
            for f in (BASE / "build").glob("DONE"):
                f.unlink(missing_ok=True)
            for f in (BASE / "build").glob("main.*"):
                # Keep build folder but remove main to trigger rebuild
                pass  # We will let integrator rebuild, not delete now

            # Step 4: Call AURA to make system asset lists
            # This is done by calling ollama via studio.py logic, but here we simulate by creating a placeholder and letting studio.py do it on next run
            # For now, create a placeholder system_requirements.json that AURA will overwrite at start
            gdd_text = gdd_path.read_text(encoding="utf-8") if gdd_path.exists() else ""
            # Detect language etc for display
            full_lang = "Python"
            for line in gdd_text.splitlines():
                if "language:" in line.lower():
                    full_lang = line.split(":",1)[1].strip()
                    break

            # Create initial system_requirements.json that AURA will refine
            initial_reqs = {
                "project": self.entry_project.get(),
                "engine": self.combo_engine.get(),
                "language": full_lang,
                "game_type": self.combo_type.get(),
                "generated_at": str(datetime.datetime.now()),
                "systems": [],
                "note": "AURA will refine this at New Project start - listing what each system needs asset-wise"
            }
            # Parse features into systems
            features_text = self.text_features.get(1.0, tk.END).strip()
            for i, line in enumerate(features_text.splitlines()[:15]):
                if line.strip():
                    # Extract system name before colon
                    sys_name = line.split(":")[0].strip() if ":" in line else line[:30]
                    initial_reqs["systems"].append({
                        "id": i+1,
                        "name": sys_name,
                        "description": line.strip(),
                        "needs": {
                            "code": [f"{sys_name.lower().replace(' ','_')}_system.{ {'python':'py','c++':'cpp','c#':'cs','lua':'lua','gdscript':'gd','rust':'rs','javascript':'js','typescript':'ts'}.get(full_lang.split('+')[0].strip().lower(), 'py') }"],
                            "art": [f"{sys_name.lower().replace(' ','_')}_visual"],
                            "audio": [f"{sys_name.lower().replace(' ','_')}_sfx"],
                            "lore": [f"{sys_name.lower().replace(' ','_')}_dialogue"]
                        },
                        "role": "forge" if any(k in line.lower() for k in ["server","network","save","physics","steam"]) else "spark" if "gameplay" in line.lower() or "movement" in line.lower() else "lore" if "dialogue" in line.lower() else "pixel" if "visual" in line.lower() or "shader" in line.lower() else "forge"
                    })

            (BASE / "system_requirements.json").write_text(json.dumps(initial_reqs, indent=2), encoding="utf-8")

            messagebox.showinfo("New Project", f"New project initialized!\n\nGDD: {gdd_path.name}\nSystem asset lists: system_requirements.json with {len(initial_reqs['systems'])} systems\n\nAURA will now refine asset lists and follow that list to assign tasks when you click Start Team.\n\nNext: Click Start Team or Continue Project")
            self.refresh_all()

        except Exception as e:
            messagebox.showerror("Error", str(e))
            import traceback
            traceback.print_exc()

    def continue_project(self):
        try:
            # Just refresh and show status - tasks.json, output/, build/ kept
            self.refresh_all()
            messagebox.showinfo("Continue Project", "Loaded existing tasks.json, MEMORY.md, output/, build/\n\nReady to continue where left off. Click Start Team to resume.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def start_team(self):
        try:
            subprocess.Popen(["cmd", "/c", "start", "cmd", "/k", "2. Start Team.bat"], shell=True)
            messagebox.showinfo("Started", "Team started in new CMD window + GUI Live Log will update. Parallel execution enabled (max 2 models in 16GB VRAM).")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def pause_team(self):
        try:
            (BASE / "PAUSE").write_text("paused by GUI", encoding="utf-8")
            messagebox.showinfo("Paused", "PAUSE file created - team pauses after current parallel batch")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def resume_team(self):
        try:
            if (BASE / "PAUSE").exists():
                (BASE / "PAUSE").unlink()
            messagebox.showinfo("Resumed", "PAUSE deleted - team resumes")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def fresh_start(self):
        if not messagebox.askyesno("Fresh Start", "Backup output/ + clear tasks.json + MEMORY.md + build/DONE\n\nGDD (5. GDD.md) will NOT be touched (GDD safe).\n\nContinue?"):
            return
        try:
            import datetime, random
            backup_name = f"output_backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}_{random.randint(0,0xFFFF):04x}"
            if (BASE / "output").exists():
                shutil.copytree(BASE / "output", BASE / backup_name, dirs_exist_ok=True)
            (BASE / "tasks.json").write_text("[]", encoding="utf-8")
            (BASE / "MEMORY.md").write_text(f"# Fresh Start {datetime.datetime.now()}\n", encoding="utf-8")
            for f in (BASE / "build").glob("DONE"):
                f.unlink(missing_ok=True)
            for sub in ["code","lore","art","qa","audio"]:
                (BASE / "output" / sub).mkdir(parents=True, exist_ok=True)
            messagebox.showinfo("Fresh Start", f"Backup: {backup_name}\nReady for fresh start>finish")
            self.refresh_all()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def restore_backup(self):
        # Fresh Start / New Project back up output/ but nothing could restore it.
        # Pick a backup -> its contents are copied back over output/.
        try:
            backups = sorted([d for d in BASE.glob("output_backup_*") if d.is_dir()],
                             key=lambda d: d.stat().st_mtime, reverse=True)
            if not backups:
                messagebox.showinfo("Restore", "No output_backup_* folders found")
                return
            names = "\n".join(f"{i+1}. {b.name}" for i, b in enumerate(backups[:10]))
            pick = simpledialog.askstring("Restore Output Backup",
                f"Enter number to restore (latest first):\n\n{names}\n\nExisting output/ will be moved aside first.")
            if not pick or not pick.strip().isdigit():
                return
            idx = int(pick.strip()) - 1
            if idx < 0 or idx >= len(backups[:10]):
                messagebox.showerror("Restore", "Invalid number")
                return
            chosen = backups[idx]
            # move current output aside rather than overwriting (never lose work)
            if (BASE / "output").exists() and any((BASE / "output").rglob("*.*")):
                aside = BASE / f"output_prerestore_{datetime.now().strftime('%Y%m%d_%H%M')}_{random.randint(0,0xFFFF):04x}"
                shutil.copytree(BASE / "output", aside, dirs_exist_ok=True)
            shutil.copytree(chosen, BASE / "output", dirs_exist_ok=True)
            messagebox.showinfo("Restore", f"Restored {chosen.name} -> output/\n(Prior output/ copied aside, nothing deleted)")
            self.refresh_all()
        except Exception as e:
            messagebox.showerror("Restore failed", str(e))

    def force_rebuild(self):
        try:
            for f in (BASE / "build").glob("DONE"):
                f.unlink(missing_ok=True)
            for f in (BASE / "build").glob("main.*"):
                f.unlink(missing_ok=True)
            messagebox.showinfo("Force Rebuild", "Deleted build/DONE and build/main.* - next cycle will trigger FINAL COMPILATION from output/ fragments")
            self.refresh_all()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def edit_gdd(self):
        try:
            gdd = self.get_gdd_path()
            if gdd.exists():
                os.startfile(str(gdd))
            else:
                messagebox.showerror("Error", "No GDD found")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def open_build(self):
        try:
            os.startfile(str(BASE / "build"))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def open_output(self):
        try:
            os.startfile(str(BASE / "output"))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def open_builds_archive(self):
        try:
            (BASE / "builds").mkdir(exist_ok=True)
            os.startfile(str(BASE / "builds"))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def send_directive(self):
        txt = self.directive_entry.get().strip()
        if not txt:
            return
        try:
            with open(BASE / "inbox_history.txt", "a", encoding="utf-8") as f:
                f.write(f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] {txt}\n")
            (BASE / "INBOX.txt").write_text(txt, encoding="utf-8")
            self.directive_entry.delete(0, tk.END)
            messagebox.showinfo("Sent", f"Directive: {txt}\nGDD untouched")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def run_build(self):
        try:
            run_bat = BASE / "build" / "run.bat"
            if run_bat.exists():
                subprocess.Popen(["cmd", "/c", "start", "cmd", "/k", str(run_bat)], shell=True)
            else:
                # Try any main
                for ext in [".py",".cpp",".cs",".lua",".gd",".rs",".js"]:
                    p = BASE / "build" / f"main{ext}"
                    if p.exists():
                        if ext == ".py":
                            subprocess.Popen(["cmd", "/c", "start", "cmd", "/k", f"cd /d {BASE / 'build'} && python main.py"], shell=True)
                        else:
                            os.startfile(str(BASE / "build"))
                        return
                messagebox.showerror("No Build", "No build/run.bat or main.* found")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def install_check(self):
        try:
            out = subprocess.check_output(["ollama", "list"], shell=True, text=True, timeout=5)
            messagebox.showinfo("Ollama Models", out[:1500])
        except Exception as e:
            messagebox.showerror("Failed", str(e))

    def export_build(self, stage):
        try:
            # Call export_build logic from studio.py via python
            code = f"""
import sys
sys.path.insert(0, r'{BASE}')
from studio import export_build
p = export_build('{stage}')
print(f'Exported to {{p}}')
"""
            out = subprocess.check_output([sys.executable, "-c", code], text=True, timeout=20)
            messagebox.showinfo(f"Export {stage}", out)
            self.refresh_all()
        except Exception as e:
            messagebox.showerror("Export Failed", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = AiTeamGUIv2(root)
    root.mainloop()
