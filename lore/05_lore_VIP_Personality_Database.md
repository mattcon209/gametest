```json
{
  "VIP_Personalities": [
    {
      "name": "The Diva",
      "description": "Obsessed with appearances and luxury. Physical harm is a minor inconvenience compared to a smudge on their impeccable attire.",
      "scoring_priority": {
        "physical_damage": 0.2,
        "dirtiness": 0.8,
        "embarrassment": 0.1
      },
      "stress_meter_behavior": "Stress increases rapidly with any form of dirt or visible damage to clothing.",
      "unique_mechanics": {
        "dirt_penalty_multiplier": 2.0,
        "clothing_damage_effect": "Causes a temporary decrease in movement speed and increased stress.",
        "cleanup_bonus": "+5 points per successful cleaning station interaction."
      }
    },
    {
      "name": "The Glass Cannon",
      "description": "Incredibly fragile but remarkably unconcerned with their well-being. A bit of a masochist, really.",
      "scoring_priority": {
        "physical_damage": 0.9,
        "dirtiness": 0.1,
        "embarrassment": 0.2
      },
      "stress_meter_behavior": "Stress is largely unaffected by physical harm; increased by embarrassment or failure to prevent damage.",
      "unique_mechanics": {
        "health_multiplier": 0.5,
        "damage_reduction_bonus": "+10% Damage Resistance when taking damage",
        "embarrassment_penalty_multiplier": 1.5
      }
    },
    {
      "name": "The Paranoid",
      "description": "Constantly on edge and convinced of imminent danger, even when none exists.",
      "scoring_priority": {
        "physical_damage": 0.3,
        "dirtiness": 0.2,
        "embarrassment": 0.5
      },
      "stress_meter_behavior": "Stress meter fills at double the normal rate and is easily triggered by loud noises, sudden movements, or perceived threats.",
      "unique_mechanics": {
        "stress_fill_rate_multiplier": 2.0,
        "threat_perception_range": "Increased",
        "calming_interaction_bonus": "+15 points per successful calming interaction (e.g., offering reassurance)"
      }
    },
    {
      "name": "The Melancholy",
      "description": "A deeply introspective and contemplative VIP, easily overwhelmed by their own thoughts and feelings.",
      "scoring_priority": {
        "physical_damage": 0.4,
        "dirtiness": 0.3,
        "embarrassment": 0.3
      },
      "stress_meter_behavior": "Stress builds slowly but persistently; exacerbated by isolation and negative environmental stimuli.",
      "unique_mechanics": {
        "isolation_penalty_multiplier": 1.75,
        "positive_interaction_bonus": "+20 points per successful supportive interaction from bodyguards (e.g., offering a comforting presence)",
        "mood_modifiers": {
          "environmental_factors": [
            { "type": "lighting", "modifier": -0.1 },
            { "type": "sound", "modifier": -0.05 },
            { "type": "crowd_density", "modifier": -0.2 }
          ],
          "damage_taken": 0.3,
          "embarrassment": 0.15
        }
      }
    },
     {
      "name": "The Energetic",
      "description": "A hyperactive VIP who thrives on stimulation and excitement, but can be easily overwhelmed by monotony.",
      "scoring_priority": {
        "physical_damage": 0.3,
        "dirtiness": 0.2,
        "embarrassment": 0.5
      },
      "stress_meter_behavior": "Stress meter decreases with exposure to stimulating environments and activities, but rapidly increases if left bored.",
      "unique_mechanics": {
        "boredom_fill_rate_multiplier": 1.5,
        "stimulation_requirement": "High",
        "interactive_element_bonus": "+10 points per successful interaction with stimulating elements (e.g., arcade games, vibrant displays)"
      }
    }

  ]
}
```