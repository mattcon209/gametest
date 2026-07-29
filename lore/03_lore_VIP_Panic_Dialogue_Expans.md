```json
{
  "vip_panic_dialogue": {
    "base_lines": [
      "Oh dear! This is rather unsettling.",
      "Goodness, what was that?",
      "I do hope nothing breaks!",
      "A little… alarming, isn’t it?",
      "Please be careful!"
    ],
    "personality_modifiers": {
      "The Diva": {
        "priority": 1,
        "lines": [
          "My hair! I hope that didn't damage my hair!",
          "Is this… dirt? On *my* shoes?",
          "Someone get me a towel! Immediately!",
          "This is simply dreadful for my complexion.",
          "I expected better protection, frankly."
        ],
        "stress_threshold": 0.7,
        "voice_tone": "high-pitched, dramatic"
      },
      "The Glass Cannon": {
        "priority": 2,
        "lines":[
          "Oof! That was close!",
          "Did… did I break something?",
          "I think I felt a draft.",
          "Just try to be gentle, please.",
          "Am I... okay?"
        ],
        "stress_threshold": 0.5,
        "voice_tone": "nervous, trembling"
      },
      "The Paranoid": {
        "priority": 3,
        "lines":[
            "They're coming! I know they are!",
            "We’re not safe here! Move us!",
            "I heard something behind me!",
            "Protect me! Please protect me!",
            "This is all a trap!"
        ],
        "stress_threshold": 0.3,
        "voice_tone": "anxious, breathy"
      },
      "The Stoic": {
          "priority":4,
          "lines":[
              "Acknowledged.",
              "Minor inconvenience.",
              "Proceeding with caution.",
              "Maintain composure.",
              "Assess the situation."
          ],
          "stress_threshold": 0.9,
          "voice_tone": "monotone, even"

      },
       "The Enthusiast": {
           "priority":5,
           "lines":[
               "Whee! Exciting!",
               "This is a bit of an adventure, isn't it?",
               "Oh my goodness, what will happen next?!",
               "Let's see if we can dodge that one!",
               "Faster, faster!"
           ],
           "stress_threshold":0.4,
           "voice_tone":"upbeat, excited"

       }

    },
    "fallbacks":[
      "Please! I don't like this!",
      "What’s happening?",
      "I'm feeling a little… uneasy."
    ],
     "randomization": "Prioritize personality-specific lines based on 'priority' value. If no personality matches, use base lines. Randomly select from available lines within each category (base, personality, fallback)."
  }
}
```