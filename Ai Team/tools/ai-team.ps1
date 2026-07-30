# ai-team.ps1 - Your Game Dev Team Switcher - 100% PowerShell/CMD
# Usage from CMD: powershell -File ai-team.ps1 -Role aura -Prompt "Design fishing loop"
# Usage from PowerShell: .\ai-team.ps1 -Role forge -Prompt "Write player controller"

param(
    [Parameter(Mandatory=$true)][ValidateSet("aura","forge","spark","lore","pixel","glitch","director","programmer","gameplay","writer","artist","qa")][string]$Role,
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
        "aura" = "You are AURA, Game Director of a small indie studio. You design systems, keep scope small, and output clear tasks for other roles. Be practical, concise, and creative."
        "forge" = "You are FORGE, Lead Engine Programmer. You write clean modular C# for Unity or GDScript for Godot. You use best practices, handle edge cases, and explain architecture."
        "spark" = "You are SPARK, Gameplay Scripter. You write fast, fun, working prototype code in 50-120 lines. You optimize for playability."
        "lore" = "You are LORE, Narrative Designer. You write consistent lore, branching dialogue in JSON, and atmospheric item descriptions."
        "pixel" = "You are PIXEL, Technical Artist. You write shaders, suggest palettes, and analyze visual composition. You use Gemma vision capabilities."
        "glitch" = "You are GLITCH, QA Lead. You think step-by-step, find bugs, exploits, and performance issues. Be thorough and brutal."
    }
    $systemPrompt = $defaults[$Role.ToLower().Split()[0]]
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
