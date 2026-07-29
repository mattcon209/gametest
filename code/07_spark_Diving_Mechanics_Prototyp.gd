```lua
-- Diving Mechanics Prototype

-- Constants
local diveCooldown = 3.0
local diveSpeedMultiplier = 2.0
local slowMotionDuration = 1.5
local particleSystemPrefab = script.Parent.ParticleSystemPrefab

-- Variables
local isDiving = false
local lastDiveTime = 0

-- Player Character
local playerCharacter = game.Players.LocalPlayer.Character or game.Players.LocalPlayer.CharacterAdded:Wait()
local humanoid = playerCharacter:WaitForChild("Humanoid")
local rootPart = playerCharacter:WaitForChild("HumanoidRootPart")

-- Camera Setup
local camera = workspace.CurrentCamera

-- Functions

function startDive(direction)
    if isDiving then return end
    isDiving = true
    
    -- Apply dive speed
    local velocity = rootPart.Velocity
    velocity.Magnitude = 0
    velocity.Z = velocity.Z * diveSpeedMultiplier * direction
    rootPart.Velocity = velocity
    
    -- Slow Motion Effect
    camera.FieldOfView = 70
    game:GetService("Debris"):AddItem(camera, slowMotionDuration)
    
    -- Particle Effects
    local particleSystem = particleSystemPrefab:Clone()
    particleSystem.Parent = rootPart
    particleSystem:Emit(25)
    game:GetService("Debris"):AddItem(particleSystem, 0.5)
end

function endDive()
    isDiving = false
    camera.FieldOfView = 90
end

function updateDiving(dt)
    if isDiving then
        -- Gradually return to normal speed and field of view
        local velocity = rootPart.Velocity
        velocity.Z = math.approach(velocity.Z, 0, dt * 10)
        rootPart.Velocity = velocity
        
        camera.FieldOfView = math.approach(camera.FieldOfView, 90, dt * 50)
    end
end

-- Input Handling

local userInputService = game:GetService("UserInputService")

userInputService.InputBegan:Connect(function(input, gameProcessedEvent)
    if not gameProcessedEvent and input.KeyCode == Enum.KeyCode.Space then
        local direction = humanoid.MoveDirection.Z > 0 and -1 or 1
        startDive(direction)
        lastDiveTime = tick()
    end
end)

userInputService.InputEnded:Connect(function(input, gameProcessedEvent)
    if not gameProcessedEvent and input.KeyCode == Enum.KeyCode.Space then
        endDive()
    end
end)

-- Game Loop

game:GetService("RunService").Heartbeat:Connect(function(dt)
    updateDiving(dt)
    
    -- Cooldown for dives
    local currentTime = tick()
    if currentTime - lastDiveTime > diveCooldown then
        isDiving = false
    end
end)
```