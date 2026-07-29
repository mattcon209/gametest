

Here is a step-by-step explanation of the identified bugs and their fixes:

**1. Stress Meter Doesn't Reset Properly on Max Stress:**
- **Issue:** The stress value exceeds maxStress without resetting, causing overflow or crashes.
- **Fix:** Implement a check in `UpdateStress` to reset stress to 0 once it surpasses maxStress.

```csharp
public void UpdateStress(float delta)
{
    stress += delta;
    if (stress > maxStress)
    {
        OnMaxStressReached();
        ResetStress(); // Calls ResetStress method
    }
}

private void ResetStress()
{
    stress = 0f;
}
```

**2. Negative Stress Values:**
- **Issue:** Stress drops below zero, causing invalid states.
- **Fix:** Clamp the stress value to ensure it doesn't go below 0.

```csharp
public void UpdateStress(float delta)
{
    stress += delta;
    if (stress > maxStress)
    {
        OnMaxStressReached();
        ResetStress();
    }
    else if (stress < 0)
    {
        stress = 0f; // Ensures minimum of 0
    }
}
```

**3. Infinite Loop in Animation System:**
- **Issue:** Rapid stress changes cause animations to loop infinitely.
- **Fix:** Introduce a flag to prevent overlapping animations.

```csharp
public class StressMeterManager : MonoBehaviour
{
    private bool isAnimating = false;

    public void PlayStressEffect()
    {
        if (!isAnimating)
        {
            StartCoroutine(AnimateStress());
        }
    }

    private IEnumerator AnimateStress()
    {
        isAnimating = true;
        // Animation logic here
        yield return new WaitForSeconds(animationDuration);
        isAnimating = false;
    }
}
```

**4. Incorrect Display of Current Stress Percentage:**
- **Issue:** UI doesn't update correctly due to miscalculations or delayed updates.
- **Fix:** Ensure the UI updates at each stress change and uses correct percentage calculations.

```csharp
public class UIManager : MonoBehaviour
{
    public Text stressText;

    private void Update()
    {
        if (stressMeterManager.stressUpdated)
        {
            stressText.text = $"{(int)(stressMeterManager.currentStress * 100)}%";
            stressMeterManager.stressUpdated = false;
        }
    }
}
```

These fixes address the identified issues by resetting stress properly, clamping values, preventing animation loops, and ensuring correct UI updates.