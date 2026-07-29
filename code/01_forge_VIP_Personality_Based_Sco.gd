```csharp
using UnityEngine;

public enum VIPPersonality
{
    Diva,
    GlassCannon,
    Paranoid,
}

public class VIPScoringSystem : MonoBehaviour
{
    public VIPPersonality vipPersonality;
    public int grimeScore;
    public int physicalHarmScore;
    public int stressScore;

    private void Start()
    {
        InitializeScores();
    }

    private void InitializeScores()
    {
        switch (vipPersonality)
        {
            case VIPPersonality.Diva:
                physicalHarmScore = 10; // Diva cares less about physical harm
                grimeScore = 50; // Diva is extremely sensitive to getting dirty
                stressScore = 20;
                break;

            case VIPPersonality.GlassCannon:
                physicalHarmScore = 80; // Glass Cannon is very fragile, high impact of physical harm
                grimeScore = 10; // Glass Cannon doesn't mind getting scuffed up or dirty
                stressScore = 30;
                break;

            case VIPPersonality.Paranoid:
                physicalHarmScore = 20;
                grimeScore = 40;
                stressScore = 50; // Paranoid has a high sensitivity to stress
                break;
        }
    }

    public void AddGrime(int amount)
    {
        if (vipPersonality == VIPPersonality.Diva)
        {
            amount *= 2; // Diva is more sensitive to grime
        }
        UpdateScore(ref grimeScore, amount);
    }

    public void ApplyPhysicalHarm(int amount)
    {
        if (vipPersonality == VIPPersonality.GlassCannon)
        {
            amount *= 1.5f; // Glass Cannon takes higher damage from physical harm
        }
        UpdateScore(ref physicalHarmScore, amount);
    }

    public void IncreaseStress(int amount)
    {
        if (vipPersonality == VIPPersonality.Paranoid)
        {
            amount *= 2; // Paranoid is more sensitive to stress
        }
        UpdateScore(ref stressScore, amount);
    }

    private void UpdateScore(ref int score, int amount)
    {
        score += amount;
        if (score < 0) score = 0;

        // Assuming there's a method in the contract progression system to update scores.
        ContractProgressionSystem.UpdateVIPScores(grimeScore, physicalHarmScore, stressScore);
    }
}
```

This code implements the VIP Personality-Based Scoring System. It initializes scores based on VIP personality and updates them dynamically during gameplay by considering the specific traits of each personality type (e.g., Diva's grime sensitivity, Paranoid's stress multipliers). The system is integrated with an assumed `ContractProgressionSystem` to update scores accordingly.