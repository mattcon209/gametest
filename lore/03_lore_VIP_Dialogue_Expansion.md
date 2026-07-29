```json
{
  "VIP_Dialogue": {
    "TheDiva": {
      "InitialGreeting": "Darling, must you *breathe* so loudly? Let’s make this… expedient.",
      "ConversationTrees": [
        {
          "Topic": "Compliment",
          "Lines": [
            {"Text": "Oh, that is *divine*. Though it clashes terribly with my aura.", "ScoreModifier": 10},
            {"Condition": "Player Reputation < 25", "Text": "Flattery will get you nowhere. Move along.", "ScoreModifier": -5}
          ]
        },
        {
          "Topic": "Dirt/Stain",
          "Lines": [
            {"Text": "Ew! Is that… mud?! I simply *cannot* be seen with this sort of thing on my person!", "ScoreModifier": -20, "EventTrigger": "Apply Stain"},
            {"Condition": "Player Reputation > 75", "Text": "Honestly, you're doing a rather passable job keeping me clean.  A C+ perhaps." , "ScoreModifier": 5}
          ]
        },
         {
          "Topic": "Speed",
          "Lines":[
            {"Text": "Faster! Do I look like I have all day? My stylist is waiting.", "ScoreModifier": -10, "VIPAction": "Slightly Increase Pace"},
            {"Condition": "Player Reputation < 50", "Text": "Don’t rush me.  My posture requires careful consideration.", "ScoreModifier":-2}
          ]
        },
        {
          "Topic": "Photography",
          "Lines":[
             {"Text":"Absolutely not! Unless it's a *perfect* shot, darling. A perfect shot.", "ScoreModifier": -5},
              {"Condition": "Player Reputation > 80", "Text":"Very well. But only three poses. And no flash!", "ScoreModifier":15}
          ]
        },
       {
          "Topic": "Safety Concerns",
            "Lines":[
             {"Text":"Do you think I care about safety? Safety is *so* last season.", "ScoreModifier": -10},
               {"Condition": "Player Reputation > 60","Text":"You’re surprisingly attentive.  Still, don't expect a thank you." , "ScoreModifier":5}
            ]
        }

      ]
    },
    "TheGlassCannon": {
      "InitialGreeting": "Oh dear... please be careful! I bruise easily.",
      "ConversationTrees": [
        {
          "Topic": "Concern",
          "Lines":[
            {"Text":"Really? You worry about *me*? How flattering, but unnecessary. Mostly.", "ScoreModifier":5},
             {"Condition": "Player Reputation < 30", "Text":"Please don't break me... I just had a facial.", "ScoreModifier": -15}

          ]
        },
        {
          "Topic": "Damage",
          "Lines":[
            {"Text":"Oh! That stung. A little. Actually, quite a bit. ", "ScoreModifier":-20,"EventTrigger": "Briefly Stun VIP"},
              {"Condition": "Player Reputation > 70", "Text":"You're remarkably gentle. Almost makes up for the bumps.", "ScoreModifier":10}

          ]
        },
         {
           "Topic":"Compliment",
             "Lines":[
                {"Text":"Oh my! How kind of you to notice!  I try.", "ScoreModifier": 25},
                 {"Condition":"Player Reputation < 40","Text":"Please don't laugh. My self-esteem is fragile enough already." , "ScoreModifier": -10}
             ]
         },

          {
            "Topic": "Pace",
              "Lines":[
               {"Text":"Could we perhaps... slow down a little? Please?", "ScoreModifier": -5,  "VIPAction": "Slightly Decrease Pace"},
                {"Condition": "Player Reputation > 80","Text":"You’re the best bodyguard I could have asked for. Just… gentle.", "ScoreModifier":30}

              ]
          },

           {
             "Topic": "Cleanliness",
              "Lines":[
               {"Text":"Oh! A speck of dust? *Gasp*!", "ScoreModifier": -15,"EventTrigger":"Apply Small Dust Speck"},
                {"Condition":"Player Reputation > 60","Text":"It's charming you pay so much attention to my appearance.", "ScoreModifier":20}

              ]
           }



      ]
    },
      "TheParanoid": {
          "InitialGreeting": "Are you… are you *sure* it’s safe? Because I don't feel safe! No, not one bit!",
          "ConversationTrees":[
             {
                 "Topic":"Safety",
                  "Lines":[
                   {"Text":"We're doomed. Absolutely doomed! Did you see that pigeon?! It was *watching* me.", "ScoreModifier":-15,"EventTrigger": "Increase Stress"},
                     {"Condition": "Player Reputation > 70","Text":"You... you seem competent. Relatively speaking.", "ScoreModifier":20}
                  ]

              },
             {
                "Topic":"Noise",
                "Lines":[
                 {"Text":"Is that a *bang*?! I can't handle loud noises!", "ScoreModifier":-10,"EventTrigger": "Increase Stress"},
                   {"Condition": "Player Reputation < 35","Text":"Stay back! Don't come any closer. You’re creeping me out.", "ScoreModifier":-20}

                ]
             },
              {
                  "Topic":"Compliment",
                    "Lines":[
                      {"Text":"You think so? Really? You must be mistaken!", "ScoreModifier":5},
                       {"Condition": "Player Reputation < 45","Text":"Don’t patronize me! I'm perfectly aware of my flaws.", "ScoreModifier":-10}

                    ]
              },

               {
                 "Topic": "Route",
                   "Lines":[
                      {"Text":"Are you *certain* this is the safest route? It looks awfully… exposed.","ScoreModifier": -5,  "VIPAction": "Suggest Alternate Route"},
                        {"Condition":"Player Reputation > 80","Text":"You are shockingly good at assessing risk.", "ScoreModifier":40}

                   ]
              },


              {
                "Topic": "People",
                 "Lines":[
                      {"Text":"That person is staring! I know they’re plotting something!", "ScoreModifier": -15,"EventTrigger": "Increase Stress"},
                       {"Condition": "Player Reputation > 60","Text":"You're remarkably good at keeping people away.", "ScoreModifier":30}

                 ]
              }

          ]
      }
  }
}
```