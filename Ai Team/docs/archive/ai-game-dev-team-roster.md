# 🎮 Offline AI Game Dev Team - Built for 32GB RAM + RTX 5060 Ti 16GB

> Reusing the LLMs from your list, optimized to actually *run together* on your hardware. 
> Strategy: 4 unique weights, 6 team members via different system prompts / instances. Only 1-2 models are loaded in VRAM at a time - Ollama auto-swaps in ~2 seconds.

---

### 🖥️ Your Hardware Budget
RTX 5060 Ti 16GB (if you have the 8GB variant, use the Q3 versions noted below)

| Model (Quantized) | File Size | VRAM Used | Fits? |
|---|---|---|---|
| **Devstral 24B Q4_K_M** | 14.2 GB | 13.5 GB VRAM + 2GB RAM | ✅ Your heavy hitter, loads alone |
| **Qwen3 14B Q4_K_M** | 9.1 GB | 9 GB VRAM | ✅ |
| **Qwen2.5-Coder 14B Q4** | 8.8 GB | 8.5 GB VRAM | ✅ Can run 2x 14B at once with offload |
| **Gemma 3 12B Q4_K_M** | 7.8 GB | 7.5 GB VRAM | ✅ |
| **DeepSeek-R1 Distill 14B Q4** | 9.5 GB | 9 GB VRAM | ✅ |

You CANNOT load all 6 at once in 16GB VRAM (that would need 48GB). But you don't need to - they work in turns like a real team. Ollama / LM Studio will automatically unload the idle one.

---

### THE TEAM

#### 1. "AURA" - Game Director / Systems Designer
**Model:** `Qwen3 14B Q4_K_M` [Best Overall from your list]
**Reuse for:** Level Designer
**Install:** `ollama run qwen3:14b`
**Role:** Brain of the operation. Keeps the Game Design Doc in memory (128K context), balances mechanics, makes final calls.
**System Prompt Snippet:**
> You are AURA, Game Director. You specialize in systems design, player loops, and scope control. You are ruthlessly practical about what fits in a solo/small team indie game. Output tasks for other team members.

**Why Qwen3?** Ranked #1 overall for local use because it balances reasoning, tool-use, and planning with Apache 2.0 license. Its agent/explicit tool-calling design is perfect for a director assigning work [Best overall from previous list].

#### 2. "FORGE" - Lead Engine / Architecture Programmer
**Model:** `Devstral Small 24B Q4_K_M` [Best Local Coding Agent from your list]
**Install:** `ollama run devstral:24b` or `ollama run devstral-small:24b`
**Role:** Builds core systems - save system, player controller, inventory, build pipeline. Works in repo, not just snippets.
**System Prompt:**
> You are FORGE, Senior Engine Programmer. You write clean, modular C# (Godot/Unity) or GDScript. You use tools, read files, plan refactors. Never write throwaway code.

**Why Devstral?** Built specifically for agentic software engineering - it was trained to use bash, edit files, plan multi-step tasks, not just chat. Perfect for Continue.dev / Cline integration.

**Hardware Note:** This is your biggest model. Run it solo when it's coding. If you have the 8GB 5060 Ti, use `devstral:24b-q3_K_M` (~9GB).

#### 3. "SPARK" - Gameplay Scripter / Rapid Prototyper (2nd instance of Qwen family)
**Model:** `Qwen2.5-Coder 14B Q4` [Coding Specialist from your list]
**Install:** `ollama run qwen2.5-coder:14b`
**Role:** Implements Aura's tickets FAST. Enemy AI, power-ups, UI interactions. Fill-in-the-middle specialist.
**System Prompt:**
> You are SPARK, Gameplay Scripter. You take a 2-sentence feature request and output working, commented code with edge cases handled. Optimize for fun > perfection.

**Why?** 92% HumanEval, excellent FIM (fill in the middle) - like offline Copilot but better for game logic. Smaller and faster than Forge, so you can keep it loaded while Forge rests.

#### 4. "LORE & PIXEL" - Two Roles, One Brain (Gemma 3 Vision)
**Model:** `Gemma 3 12B Q4_K_M` [Best Laptop-Friendly / Multimodal from your list] - Used TWICE
**Install:** `ollama run gemma3:12b`
**Role A - LORE (Narrative Designer):** Dialogue, world bible, quests, item descriptions. Remembers entire story with 128K context.
**Role B - PIXEL (Technical Artist):** Reads concept art screenshots, writes shaders, generates material prompts, creates asset lists.

**System Prompts:**
> LORE: You are a cozy/dark game writer. You maintain consistent tone, write branching dialogue in JSON, never break lore.
> PIXEL: You are a Tech Artist. You can SEE images (Gemma is multimodal). Analyze screenshots for art direction, write Unity Shader Graph / Godot shaders, suggest color palettes.

**Why Gemma?** It's the best single-GPU multimodal model - it can actually SEE images and talk about them, unlike pure coders. Also rated best for creative writing / instruction-following on your list. Using one weight for two jobs saves 7.5GB VRAM.

#### 5. "GLITCH" - QA / Bug Hunter / Optimizer
**Model:** `DeepSeek-R1-Distill-Qwen-14B Q4` [Reasoning King from your list]
**Install:** `ollama run deepseek-r1:14b`
**Role:** The annoying but essential QA. Finds logic holes, race conditions, performance bottlenecks. Thinks step-by-step for 30 seconds before answering.
**System Prompt:**
> You are GLITCH, QA Lead. You think in chain-of-thought. Find 3 bugs, 2 exploits, and 1 performance issue in the provided code. Be brutal. Provide fix suggestions.

**Why DeepSeek-R1?** 79.8% AIME math, 71.5% GPQA - it was built to *reason* slowly and deeply. Perfect for debugging and edge-case hunting where other models get lazy.

---

### How They Work Together - A Typical Workflow (Local, Offline)

**You use:** Open WebUI + Pipelines, or just 3 terminal tabs + Continue.dev in VS Code

1.  **You → AURA (Qwen3 14B):** "We want a 2D roguelite fishing game with time-loop"
    → AURA outputs GDD.md and creates tasks.

2.  **AURA → FORGE (Devstral 24B) in VS Code:** "Build player controller + time loop manager"
    → Forge builds the core C# files via Continue.dev agent.

3.  **AURA → SPARK (Qwen2.5-Coder):** "Prototype: fish bite mini-game in 80 lines"
    → Spark outputs quick playable snippet.

4.  **You screenshot the game → PIXEL (Gemma 3 12B):** "What does this scene need visually?"
    → Pixel: "Add chromatic aberration shader, here's the code... palette is too saturated"

5.  **SPARK's code → GLITCH (DeepSeek-R1 14B):** "Review this mini-game for exploits"
    → Glitch: "Found infinite fish bug if player spams click - fix with cooldown"

6.  **Close with LORE (Gemma 3 12B second instance):** "Write 5 NPC barks for the harbor keeper who remembers loops"

**VRAM tip:** Only Forge OR Glitch + one other should be loaded. Let Ollama handle it: `ollama run devstral` will auto-unload gemma3.

### Final Roster for YOUR PC (Copy/Paste)

```bash
# On your 32GB + RTX 5060 Ti 16GB - these 4 weights = your entire studio
ollama run qwen3:14b                 # AURA - Director (9GB)
ollama run devstral:24b              # FORGE - Lead Programmer (14.2GB) - run alone
ollama run qwen2.5-coder:14b         # SPARK - Gameplay (8.8GB)
ollama run gemma3:12b                # LORE+PIXEL - Writer/Artist (7.8GB) x2 roles
ollama run deepseek-r1:14b           # GLITCH - QA (9.5GB)

# If you have the 8GB 5060 Ti variant, use these instead:
ollama run qwen3:8b
ollama run devstral:24b-q3_K_M
ollama run gemma3:4b
```

Total disk space: ~50GB once. After that, full airplane mode game studio.

Want me to generate the actual system prompt files + CrewAI config to launch all 6 roles with one click?
