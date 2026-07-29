```json
{
  "VIPPanicDialogue": {
    "global_defaults": {
      "trigger_threshold": 0.75,
      "intensity_scaling": "linear",
      "volume_increase": 0.15,
      "pitch_shift": -0.05,
      "reverb_increase": 0.1
    },

    "VIPProfiles": {
      "TheDiva": {
        "name": "Genevieve Dubois",
        "panic_lines": [
          {
            "intensity": 0.2,
            "dialogue": "Oh dear! Is that… mud? Absolutely dreadful!"
          },
          {
            "intensity": 0.4,
            "dialogue": "My shoes! Be careful where you're going!"
          },
          {
            "intensity": 0.6,
            "dialogue": "I can feel a stain coming on! Please protect me!"
          },
          {
            "intensity": 0.8,
            "dialogue": "My reputation! Don’t let me get dirty!"
          },
          {
            "intensity": 1.0,
            "dialogue": "This is a DISASTER! My image! Someone do something!"
          }
        ],
        "specific_hazard_reactions": {
            "mud": {
              "priority": 1,
              "dialogue": "Noooo! The MUD!"
            },
            "splash_water":{
              "priority": 2,
              "dialogue": "Water?! On my ensemble?!"
            }
          }
      },
      "TheGlassCannon": {
        "name": "Professor Quentin Finch",
        "panic_lines": [
          {
            "intensity": 0.2,
            "dialogue": "A slight jostle! Quite unsettling."
          },
          {
            "intensity": 0.4,
            "dialogue": "Careful now, a little bump and I might… topple."
          },
          {
            "intensity": 0.6,
            "dialogue": "I feel...precarious! Please maintain balance!"
          },
          {
            "intensity": 0.8,
            "dialogue": "A minor inconvenience is all it takes, I’m afraid."
          },
          {
            "intensity": 1.0,
            "dialogue": "Oh dear! I think I felt a fracture...!"
          }
        ],
         "specific_hazard_reactions": {
            "collision": {
              "priority": 1,
              "dialogue": "Oof! That was rather abrupt."
            },
            "impact":{
              "priority": 2,
              "dialogue": "My structural integrity!"
            }
          }

      },
      "TheParanoid": {
        "name": "Esmeralda Blackwood",
        "panic_lines": [
          {
            "intensity": 0.2,
            "dialogue": "Did you hear that? I think someone's watching..."
          },
          {
            "intensity": 0.4,
            "dialogue": "Are you sure this is safe? It doesn’t *feel* safe."
          },
          {
            "intensity": 0.6,
            "dialogue": "I have a very bad feeling about this! Something terrible's going to happen!"
          },
          {
            "intensity": 0.8,
            "dialogue": "We’re being targeted! I just *know* it!"
          },
          {
            "intensity": 1.0,
            "dialogue": "Run! Run for your lives! It's coming!!!"
          }
        ],
         "specific_hazard_reactions": {
            "shadow": {
              "priority": 1,
              "dialogue": "What was that?! Something’s behind us!"
            },
            "sudden_noise":{
              "priority": 2,
              "dialogue": "Eeeek! What *was* that noise?!"
            }
          }
      }
    }
  }
}
```