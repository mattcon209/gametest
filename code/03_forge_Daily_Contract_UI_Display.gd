```csharp
using UnityEngine;
using UnityEngine.UI;

public class DailyContractUI : MonoBehaviour
{
    public Text VIPPersonalityText;
    public Text ObjectivesText;
    public Text HazardsText;

    private void Start()
    {
        UpdateDailyContractUI();
    }

    public void UpdateDailyContractUI()
    {
        // Fetch current contract details from a game manager or database
        string vipPersonality = GetCurrentVIPPersonality();
        string objectives = GetCurrentObjectives();
        string hazards = GetCurrentHazards();

        VIPPersonalityText.text = "VIP Personality: " + vipPersonality;
        ObjectivesText.text = "Objectives: " + objectives;
        HazardsText.text = "Hazards: " + hazards;
    }

    private string GetCurrentVIPPersonality()
    {
        // Implement fetching logic here
        return "The Diva";
    }

    private string GetCurrentObjectives()
    {
        // Implement fetching logic here
        return "Keep the VIP clean and avoid physical harm.";
    }

    private string GetCurrentHazards()
    {
        // Implement fetching logic here
        return "Slippery surfaces, mud puddles, hostile NPCs.";
    }
}
```

This script assumes you have UI Text elements set up in your scene for displaying the contract details. Attach this script to a GameObject that manages the daily contract UI and ensure you link the appropriate UI text fields to the public variables in the inspector.