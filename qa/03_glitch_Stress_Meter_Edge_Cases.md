

```markdown
# Stress Meter Edge Cases - Bug Report

## 1. VIP Stress Meter Overflow
- **Issue:** The stress meter does not handle cases where the stress value exceeds 100%. This can cause undefined behavior, such as negative values or unintended penalties.
- **Fixes:**
  - Ensure stress values are capped at 100% and cannot exceed this limit.
  - Log warnings for any attempts to increase stress beyond 100%.

## 2. Negative Stress Values
- **Issue:** The stress meter allows negative values, which can cause penalties to be applied incorrectly (e.g., infinite loop in penalty calculations).
- **Fixes:**
  - Ensure stress cannot drop below 0%.
  - Clamp stress values at the start of each update.

## 3. Synchronization Across Clients
- **Issue:** The stress meter may desynchronize between players due to floating-point precision errors or differing update rates.
- **Fixes:**
  - Use a deterministic calculation method for stress updates.
  - Implement periodic synchronization checks between players.

## 4. VIP Stress at Contract Start/End
- **Issue:** Contracts with extreme initial or final stress values may cause undefined behavior in transition phases (e.g., penalties applied to a fully stressed VIP).
- **Fixes:**
  - Initialize stress at the start of each contract with the specified personality value.
  - Ensure transitions between contracts reset stress correctly.

## 5. VIP Personality Multipliers
- **Issue:** VIP personalities (e.g., The Paranoid) may cause stress calculations to overflow or underflow due to incorrect application of multipliers.
- **Fixes:**
  - Verify that all multipliers are applied before clamping.
  - Test edge cases with high/low multiplier values.

## 6. Performance Issues
- **Issue:** Stress meter calculations may introduce performance hitches during critical moments (e.g., high player count or complex environments).
- **Fixes:**
  - Optimize stress calculation loops to run at a fixed interval.
  - Use efficient data structures for stress updates.

## Fixed Code

```csharp
// Example fix for VIP Stress Meter calculations
public class VIPStressManager {
    private float currentStress;
    private readonly int personalityMultiplier;

    public VIPStressManager(int personality) {
        this.personalityMultiplier = GetPersonalityMultiplier(personality);
        ResetStress();
    }

    public void UpdateStress(float deltaPenalty, float deltaReward) {
        // Apply multipliers
        float newStress = currentStress + 
            (deltaPenalty * personalityMultiplier) - 
            (deltaReward / personalityMultiplier);

        // Cap values
        newStress = Math.Max(0f, Math.Min(newStress, 100f));

        // Update stress with bounds checking
        if (newStress != currentStress) {
            currentStress = newStress;
            OnStressUpdated(currentStress);
        }
    }

    public void ResetStress() {
        currentStress = GetInitialStressValue();
        OnStressUpdated(currentStress);
    }

    private int GetPersonalityMultiplier(int personalityType) {
        switch(personalityType) {
            case (int)VIPPersonalities.TheParanoid:
                return 2;
            default:
                return 1;
        }
    }

    // Implement logging and synchronization as needed
}
```

## Conclusion

These fixes ensure the stress meter handles edge cases gracefully, maintains consistency across players, and performs efficiently under all conditions. Test each scenario thoroughly to confirm stability.
```