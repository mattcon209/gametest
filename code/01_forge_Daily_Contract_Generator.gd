```csharp
using System.Collections.Generic;
using UnityEngine;

public class DailyContractGenerator : MonoBehaviour
{
    public TextAsset contractsConfig; // JSON configuration file with contract data

    private List<DailyContract> dailyContracts = new List<DailyContract>();

    void Start()
    {
        GenerateDailyContracts();
    }

    void GenerateDailyContracts()
    {
        if (contractsConfig != null)
        {
            DailyContractData contractData = JsonUtility.FromJson<DailyContractData>(contractsConfig.text);

            for (int i = 0; i < 10; i++)
            {
                DailyContract newContract = new DailyContract
                {
                    Id = i,
                    Objectives = GetRandomObjectives(contractData.objectives),
                    Hazards = GetRandomHazards(contractData.hazards),
                    Rewards = GetRandomRewards(contractData.rewards)
                };

                dailyContracts.Add(newContract);
            }
        }
    }

    List<string> GetRandomObjectives(List<string> objectivesList)
    {
        List<string> selectedObjectives = new List<string>();
        int maxObjectiveCount = Random.Range(1, 3); // Example: 1-2 objectives per contract

        for (int i = 0; i < maxObjectiveCount; i++)
        {
            string objective = objectivesList[Random.Range(0, objectivesList.Count)];
            selectedObjectives.Add(objective);
        }

        return selectedObjectives;
    }

    List<string> GetRandomHazards(List<string> hazardsList)
    {
        List<string> selectedHazards = new List<string>();
        int maxHazardCount = Random.Range(1, 4); // Example: 1-3 hazards per contract

        for (int i = 0; i < maxHazardCount; i++)
        {
            string hazard = hazardsList[Random.Range(0, hazardsList.Count)];
            selectedHazards.Add(hazard);
        }

        return selectedHazards;
    }

    List<string> GetRandomRewards(List<string> rewardsList)
    {
        List<string> selectedRewards = new List<string>();
        int maxRewardCount = Random.Range(1, 3); // Example: 1-2 rewards per contract

        for (int i = 0; i < maxRewardCount; i++)
        {
            string reward = rewardsList[Random.Range(0, rewardsList.Count)];
            selectedRewards.Add(reward);
        }

        return selectedRewards;
    }

    public DailyContract GetDailyContract(int index)
    {
        if (index >= 0 && index < dailyContracts.Count)
        {
            return dailyContracts[index];
        }
        else
        {
            Debug.LogError("Invalid contract index");
            return null;
        }
    }
}

[System.Serializable]
public class DailyContractData
{
    public List<string> objectives;
    public List<string> hazards;
    public List<string> rewards;
}

public struct DailyContract
{
    public int Id;
    public List<string> Objectives;
    public List<string> Hazards;
    public List<string> Rewards;
}
```