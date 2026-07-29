```csharp
using System;
using System.Collections.Generic;
using UnityEngine;

public class ContractProgressionTracker : MonoBehaviour
{
    public static ContractProgressionTracker Instance { get; private set; }

    [Serializable]
    public struct VIPPersonalityStats
    {
        public string personalityName;
        public int successfulProtections;
        public float averageStressLevel;
        public bool achievementUnlocked;
    }

    public List<VIPPersonalityStats> vipPersonalityStats = new List<VIPPersonalityStats>();

    private void Awake()
    {
        if (Instance == null)
        {
            Instance = this;
            DontDestroyOnLoad(gameObject);
        }
        else
        {
            Destroy(gameObject);
        }

        LoadData();
    }

    public void UpdateVIPStats(string personalityName, int successfulProtections, float averageStressLevel, bool achievementUnlocked)
    {
        VIPPersonalityStats stats = vipPersonalityStats.Find(x => x.personalityName == personalityName);

        if (stats != null)
        {
            stats.successfulProtections += successfulProtections;
            stats.averageStressLevel = (stats.averageStressLevel + averageStressLevel) / 2; // Simple averaging for simplicity
            stats.achievementUnlocked |= achievementUnlocked;

            int index = vipPersonalityStats.FindIndex(x => x.personalityName == personalityName);
            vipPersonalityStats[index] = stats;
        }
        else
        {
            vipPersonalityStats.Add(new VIPPersonalityStats { personalityName = personalityName, successfulProtections = successfulProtections, averageStressLevel = averageStressLevel, achievementUnlocked = achievementUnlocked });
        }

        SaveData();
    }

    private void LoadData()
    {
        // Implement data loading from persistent storage
    }

    private void SaveData()
    {
        // Implement data saving to persistent storage
    }
}
```