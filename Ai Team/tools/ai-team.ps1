# ai-team.ps1 - Your Game Dev Team Switcher - 100% PowerShell/CMD
# Usage from CMD: powershell -File ai-team.ps1 -Role aura -Prompt "Design fishing loop"
# Usage from PowerShell: .\ai-team.ps1 -Role forge -Prompt "Write player controller"

param(
    [Parameter(Mandatory=$true)][ValidateSet("aura","forge","spark","lore","pixel","glitch","integrator","audio","director","programmer","gameplay","writer","artist","qa","builder","sfx")][string]$Role,
    [Parameter(Mandatory=$true)][string]$Prompt
)

# Role -> Model Map (Optimized for 32GB RAM + RTX 5060 Ti 16GB)
$TeamMap = @{
    "aura"       = @{ model="qwen3:14b";          name="AURA (Game Director)";       file="roles/aura.txt" }
    "director"   = @{ model="qwen3:14b";          name="AURA (Game Director)";       file="roles/aura.txt" }
    "forge"      = @{ model="devstral:24b";       name="FORGE (Lead Programmer)";    file="roles/forge.txt" }
    "programmer" = @{ model="devstral:24b";       name="FORGE (Lead Programmer)";    file="roles/forge.txt" }
    "spark"      = @{ model="qwen2.5-coder:14b";  name="SPARK (Gameplay Scripter)";  file="roles/spark.txt" }
    "gameplay"   = @{ model="qwen2.5-coder:14b";  name="SPARK (Gameplay Scripter)";  file="roles/spark.txt" }
    "lore"       = @{ model="gemma3:12b";         name="LORE (Writer)";              file="roles/lore.txt" }
    "writer"     = @{ model="gemma3:12b";         name="LORE (Writer)";              file="roles/lore.txt" }
    "pixel"      = @{ model="gemma3:12b";         name="PIXEL (Tech Artist)";        file="roles/pixel.txt" }
    "artist"     = @{ model="gemma3:12b";         name="PIXEL (Tech Artist)";        file="roles/pixel.txt" }
    "glitch"     = @{ model="deepseek-r1:14b";    name="GLITCH (QA)";                file="roles/glitch.txt" }
    "qa"         = @{ model="deepseek-r1:14b";    name="GLITCH (QA)";                file="roles/glitch.txt" }
    # Audit11 R-B: these two roles were defined in TEAM/spec but missing here (L9)
    "integrator" = @{ model="qwen3:14b";          name="INTEGRATOR (Final Builder)"; file="roles/integrator.txt" }
    "builder"    = @{ model="qwen3:14b";          name="INTEGRATOR (Final Builder)"; file="roles/integrator.txt" }
    "audio"      = @{ model="gemma3:4b";          name="AUDIO (Audio Designer)";     file="roles/audio.txt" }
    "sfx"        = @{ model="gemma3:4b";          name="AUDIO (Audio Designer)";     file="roles/audio.txt" }
}

$selected = $TeamMap[$Role.ToLower()]
if (-not $selected) { Write-Error "Unknown role"; exit 1 }

$model = $selected.model
$systemFile = $selected.file
$displayName = $selected.name

# Load system prompt if exists, otherwise use default
$systemPrompt = ""
if (Test-Path $systemFile) {
    $systemPrompt = Get-Content $systemFile -Raw
} else {
    # Fallback defaults if role files not found
    $defaults = @{
        "aura" = "You are AURA Game Director. Respect the Engine field in the GDD completely - if it says no engine/from scratch/custom, you NEVER plan Unity/Unreal/Godot. You output strict JSON tasks. GDD is read-only, never modify it."
        "forge" = "You are FORGE Lead Engine Programmer. Respect the Engine field above all else - if the GDD says custom engine/from scratch, build in the detected language with SDL/pygame/Raylib/OpenGL, NOT Unity C#/Unreal. GDD is read-only."
        "spark" = "You are SPARK Gameplay Scripter. Respect the Engine field - for custom engine you write gameplay for that engine in the detected language, NOT Unity C#. 50-150 lines, fast prototype, fun. GDD is read-only."
        "lore" = "You are LORE Narrative Designer. You write story, dialogue JSON, quests. ONLY narrative, not code. GDD is read-only, never modify it."
        "pixel" = "You are PIXEL Technical Artist. Respect the Engine field - for custom engine write shaders for custom engine (GLSL, python), not Unity Shader Graph unless the GDD says Unity. GDD is read-only."
        "glitch" = "You are GLITCH QA Lead. Respect the Engine field. Think step-by-step, check edge cases. Output bug report with fixed code. GDD is read-only, never modify it."
        "integrator" = "You are INTEGRATOR final build engineer. Respect the Engine field completely. You merge fragments into one runnable game in /build/ in the detected language. If the GDD says custom/from scratch, build the entry point with custom loop, window, input. GDD is read-only."
        "audio" = "You are AUDIO Audio Designer. Respect Engine and Language fields. You design SFX, music triggers, and audio system code stubs in the detected language. GDD is read-only."
    }
    # Map aliases to their canonical role key for the fallback table
    $aliasToRole = @{ "director"="aura"; "programmer"="forge"; "gameplay"="spark"; "writer"="lore"; "artist"="pixel"; "qa"="glitch"; "builder"="integrator"; "sfx"="audio" }
    $roleKey = $Role.ToLower()
    if ($aliasToRole.ContainsKey($roleKey)) { $roleKey = $aliasToRole[$roleKey] }
    $systemPrompt = $defaults[$roleKey]
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host " Loading $displayName" -ForegroundColor Cyan
Write-Host " Model: $model" -ForegroundColor DarkCyan
Write-Host "========================================" -ForegroundColor Cyan

# Build payload for Ollama API (http://localhost:11434)
$payload = @{
    model = $model
    messages = @(
        @{ role = "system"; content = $systemPrompt }
        @{ role = "user"; content = $Prompt }
    )
    stream = $false
} | ConvertTo-Json -Depth 6

try {
    $response = Invoke-RestMethod -Uri "http://localhost:11434/api/chat" -Method Post -Body $payload -ContentType "application/json" -TimeoutSec 300
    Write-Host ""
    Write-Host $response.message.content
    Write-Host ""
    Write-Host "--- VRAM Status ---" -ForegroundColor DarkGray
    ollama ps
} catch {
    Write-Host "API failed, trying direct ollama run..." -ForegroundColor Yellow
    # Fallback to direct run
    $fullPrompt = "$systemPrompt`n`nUSER TASK: $Prompt"
    ollama run $model $fullPrompt
}
