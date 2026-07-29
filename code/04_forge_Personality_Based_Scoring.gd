```csharp
using UnityEngine;

public enum VIPPersonality
{
    Normal,
    Diva,
    GlassCannon,
    Paranoid
}

public class VIP : MonoBehaviour
{
    public VIPPersonality personality = VIPPersonality.Normal;
    public float dirtExposurePenalty = 10f;
    public float stressSpikeMultiplier = 1.0f;

    private int score = 0;

    void Start()
    {
        // Initialize scoring based on VIP personality
        switch (personality)
        {
            case VIPPersonality.Diva:
                dirtExposurePenalty = 20f; // Example value for Diva
                break;
            case VIPPersonality.GlassCannon:
                stressSpikeMultiplier = 1.5f; // Example value for Glass Cannon
                break;
            case VIPPersonality.Paranoid:
                stressSpikeMultiplier = 2.0f; // Example value for Paranoid
                break;
            default:
                dirtExposurePenalty = 10f;
                stressSpikeMultiplier = 1.0f;
                break;
        }
    }

    public void ApplyDirtDamage(int amount)
    {
        if (personality == VIPPersonality.Diva)
        {
            score -= Mathf.RoundToInt(amount * dirtExposurePenalty);
        }
    }

    public void ApplyStressSpike(int amount)
    {
        int adjustedAmount = Mathf.RoundToInt(amount * stressSpikeMultiplier);
        score -= adjustedAmount;
    }

    public void AddScore(int amount)
    {
        score += amount;
    }

    public int GetScore()
    {
        return score;
    }
}
```