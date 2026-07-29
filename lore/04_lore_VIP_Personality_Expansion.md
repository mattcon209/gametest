```json
{
  "VIP_Personalities": [
    {
      "name": "The Pacifist",
      "description": "Absolutely despises violence of any kind. Even witnessing it causes significant stress.",
      "scoring_rules": {
        "positive": {
          "gentle_redirects": 0.5,  // Rewarded for smooth redirections, no sudden movements
          "hazard_avoidance_distance": 1.0, // Extra points for keeping a safe distance from danger
          "npc_de-escalation": 2.0 // Significant bonus if NPCs are pacified non-violently (e.g., distracting them)
        },
        "negative": {
          "vip_damage": -5.0,  // Massive penalty for any VIP damage
          "violent_npc_encounters": -3.0, //Penalty for NPC attacks or player retaliation against NPCs 
          "player_aggression": -2.0 // Penalizes players who attack anything
        }
      },
      "visual_cue": "Carries a small plush toy."
    },
    {
      "name": "The Collector",
      "description": "Obsessed with collecting shiny objects and souvenirs along the route. Will actively try to reach them, regardless of danger.",
      "scoring_rules": {
        "positive": {
          "item_collection": 3.0,  // Major bonus for successfully grabbing collectibles
          "successful_detours": 1.5 // Rewarded for taking roundabout routes to get items.
        },
        "negative": {
          "vip_damage": -2.0,  // Penalty for VIP damage (but less severe than usual)
          "hazard_proximity": -1.0, //Penalty if they are too close to a hazard while collecting
          "missed_collectibles": -0.5 //Penalty for failing to grab an item
        }
      },
      "visual_cue": "Constantly glancing around and trying to reach out to objects."
    },
    {
      "name": "The Historian",
      "description": "Fascinated by local landmarks and historical details. Will pause frequently to observe, hindering progress.",
      "scoring_rules": {
        "positive": {
          "landmark_interaction": 2.0, //Reward for stopping at/examining Landmarks; must remain still for a brief time
          "correct_history_question": 3.0  //If prompted with trivia from landmark - correct answer is heavily rewarded. Incorrect answers are punishing
        },
        "negative": {
          "time_overrun": -4.0, //Severe penalty for exceeding the contract's time limit.
          "vip_damage": -1.5, //Penalty for VIP damage, slightly less severe.
          "missed_landmark": -1.0 // Penalty if a landmark is skipped
        }
      },
      "visual_cue": "Carries a notebook and pen, occasionally stopping to make notes."
    },
     {
      "name": "The Fashionista",
      "description": "Extremely concerned about their appearance and the current trends. Disapproves of anything that ruins an outfit.",
      "scoring_rules": {
        "positive": {
          "stylish_choices": 1.0, //Bonus for navigating paths with aesthetically pleasing scenery (determined by unseen game criteria)
          "coordinated_ensemble": 2.5  //Large bonus if VIP's outfit matches a 'daily theme' visible in the contract briefing.
        },
        "negative": {
          "dirt_penalty": -3.0, //Major penalty for getting dirty or scuffed; dirt/grime is prioritized over damage
          "fashion_faux_pas":-2.0, //Penalty for being near unsavory objects
           "vip_damage": -1.0  // Penalty for VIP Damage
        }
      },
      "visual_cue": "Constantly adjusting their clothes and accessories."
    }
  ]
}
```