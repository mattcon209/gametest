```lua
-- VIP Panic Pathfinding Prototype Script

-- Constants
local STRESS_THRESHOLD = 50
local PANIC_SPEED = 15
local PANIC_DURATION = 2
local COOLDOWN_DURATION = 10

-- Variables
local vipStress = 0
local isPanicModeActive = false
local panicCooldownTimer = 0

-- Functions
function InitializeVIP()
    -- Reset VIP stress and panic mode status
    vipStress = 0
    isPanicModeActive = false
end

function UpdateVIP(dt)
    -- Increment stress over time
    vipStress = math.min(vipStress + dt * 10, 100)

    if vipStress >= STRESS_THRESHOLD and not isPanicModeActive then
        EnterPanicMode()
    end

    if isPanicModeActive then
        panicCooldownTimer = panicCooldownTimer - dt
        if panicCooldownTimer <= 0 then
            ExitPanicMode()
        end
    end
end

function EnterPanicMode()
    -- Activate panic mode
    isPanicModeActive = true
    vipStress = 0
    panicCooldownTimer = COOLDOWN_DURATION

    -- Choose a random direction for the VIP to sprint
    local panicDirection = Vector3.new(math.random(-1, 1), 0, math.random(-1, 1)).Normalized()

    -- Apply panic speed and direction to the VIP
    -- Assuming there's a function to move the VIP
    MoveVIP(panicDirection * PANIC_SPEED, PANIC_DURATION)
end

function ExitPanicMode()
    -- Deactivate panic mode
    isPanicModeActive = false
end

-- Example function to move the VIP (pseudo-code)
function MoveVIP(direction, duration)
    -- This would typically involve applying force or setting a velocity on the VIP
    print("VIP is sprinting in direction: " .. tostring(direction) .. " for " .. duration .. " seconds")
end

-- Main loop (for testing purposes)
InitializeVIP()

while true do
    local dt = 0.1 -- Simulate time delta
    UpdateVIP(dt)
    wait(0.1)
end
```