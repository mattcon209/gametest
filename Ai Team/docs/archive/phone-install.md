# 📱 PHONE REMOTE INSTALL - COPY/PASTE THIS

You have RTX 5060 Ti + 32GB RAM = Windows 11. Do this from your phone's remote CMD.

### PASTE 1: Install Ollama (the switcher + runner)
```
winget install Ollama.Ollama --silent --accept-package-agreements --accept-source-agreements
```

Wait 30 sec, close CMD, open new CMD, then paste:

```
ollama --version
```

If that fails (winget missing), paste this ONE line instead:
```
powershell -Command "Invoke-WebRequest -Uri https://ollama.com/download/OllamaSetup.exe -OutFile $env:TEMP\OllamaSetup.exe; Start-Process -Wait -FilePath $env:TEMP\OllamaSetup.exe -ArgumentList '/S'"
```

### PASTE 2: Pull Your Team (50GB, needs internet once)
Paste one at a time. Each takes 5-20 mins:
```
ollama pull qwen3:14b
ollama pull devstral:24b
ollama pull qwen2.5-coder:14b
ollama pull gemma3:12b
ollama pull deepseek-r1:14b
```

Light version for 8GB VRAM 5060 Ti:
```
ollama pull qwen3:8b
ollama pull devstral:24b-q3_K_M
ollama pull qwen2.5-coder:7b
ollama pull gemma3:4b
ollama pull deepseek-r1:7b
```

### PASTE 3: USE YOUR TEAM - No extra program needed
Ollama IS the switcher. Just call a different model name and it auto-unloads the old one from VRAM to fit your 16GB.

From CMD on your phone:
```
ollama run qwen3:14b "You are AURA Game Director. Design core loop for roguelite fishing game"
ollama run devstral:24b "You are FORGE Lead Programmer. Write Unity C# player controller"
ollama run qwen2.5-coder:14b "You are SPARK. Write fishing mini-game GDScript"
ollama run gemma3:12b "You are LORE Writer. Write 5 NPC dialogues for harbor keeper"
ollama run deepseek-r1:14b "You are GLITCH QA. Find bugs in: [paste code]"
```

Check what's loaded:
```
ollama ps
nvidia-smi
```

Free VRAM manually:
```
ollama stop devstral:24b
```

### PASTE 4: Advanced Switcher Script (optional but better)
If you downloaded my files (setup-team.bat + ai-team.ps1 + roles folder) to C:\ai-team\ , then from that folder:

```
powershell -File ai-team.ps1 -Role aura -Prompt "Design a fishing game"

powershell -File ai-team.ps1 -Role forge -Prompt "Build save system in C#"

powershell -File ai-team.ps1 -Role spark -Prompt "Prototype fishing bite mechanic"

powershell -File ai-team.ps1 -Role lore -Prompt "Write quest: The Last Catch"

powershell -File ai-team.ps1 -Role pixel -Prompt "Write water shader for Godot"

powershell -File ai-team.ps1 -Role glitch -Prompt "Review this code for bugs: [code]"
```

Roles: aura/director, forge/programmer, spark/gameplay, lore/writer, pixel/artist, glitch/qa

**That's it. 100% CMD. No clicks.**

After download, you can disconnect internet - all offline.
