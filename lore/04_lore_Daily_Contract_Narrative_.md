## DAILY CONTRACT NARRATIVE EXPANSION - JSON Format

```json
{
  "dailyContracts": [
    {
      "contractId": "diva_001",
      "vipPersonality": "The Diva",
      "vipBackstory": {
        "name": "Seraphina Bellweather",
        "description": "A renowned opera singer with a famously fragile ego and an even more delicate complexion. Seraphina believes her image is paramount, and any blemish – physical or reputational – is a personal affront.",
        "motivations": ["Maintaining perfect appearance", "Receiving adoration from the crowd", "Avoiding criticism"]
      },
      "contractTitle": "The Charity Gala",
      "narrativeIntro": "Seraphina Bellweather, darling of the opera world, is attending a charity gala tonight. The event promises dazzling lights and appreciative audiences, but also a gauntlet of paparazzi flashes, spilled drinks, and potential wardrobe malfunctions.",
      "storyBeats": [
        {
          "beatId": 1,
          "description": "Navigating the Red Carpet: Seraphina is bombarded by photographers. Players must shield her from flash bursts (damage over time – visual distortion). Getting splashed with a stray champagne bottle incurs a 'Stain' penalty.",
          "challengeType": "Environmental Hazard & Crowd Control",
          "scoringModifier": "+5 points per hazard avoided, -10 points per Stain incurred."
        },
        {
          "beatId": 2,
          "description": "The Unforeseen Guest: A rival opera singer, Madame Evangeline Dubois, arrives with a clear intention to upstage Seraphina. Players must subtly redirect Seraphina’s path to avoid direct confrontation while dodging Evangeline's passive-aggressive tactics (distracting NPC actions).",
          "challengeType": "NPC Avoidance & Pathfinding",
          "scoringModifier": "+10 points per successful redirection, -5 points if Evangeline makes eye contact with Seraphina."
        },
        {
          "beatId": 3,
          "description": "The Performance Stage: As Seraphina takes the stage, a mischievous fan attempts to toss a bouquet of roses. Players must intercept without disrupting the performance (timing-based mini-game). A failed catch results in a visible wardrobe malfunction.",
          "challengeType": "Timing & Precision",
          "scoringModifier": "+20 points for successful interception, -15 points for Wardrobe Malfunction."
        }
      ]
    },
    {
      "contractId": "glass_cannon_002",
      "vipPersonality": "The Glass Cannon",
      "vipBackstory": {
        "name": "Professor Alistair Finch",
        "description": "A brilliant but physically frail inventor with a revolutionary new energy source. While his intellect is formidable, his body is… not. He’s surprisingly unfazed by minor injuries.",
        "motivations": ["Protecting his invention", "Sharing knowledge", "Avoiding philosophical debates"]
      },
      "contractTitle": "The Science Symposium",
      "narrativeIntro": "Professor Finch is presenting his groundbreaking energy device at a prestigious science symposium. The event attracts both eager colleagues and unscrupulous rivals looking to steal his research.",
      "storyBeats": [
        {
          "beatId": 1,
          "description": "The Arrival: Navigating the bustling conference center proves difficult for Professor Finch. Overcrowding and clumsy attendees pose constant threats (small collision hazards).",
          "challengeType": "Crowd Navigation & Collision Avoidance",
          "scoringModifier": "+2 points per meter travelled without a collision, -5 points if Finch trips."
        },
        {
          "beatId": 2,
          "description": "The Saboteur: A rival scientist attempts to disrupt the presentation by triggering a minor lab explosion. Players must quickly shield Professor Finch from shrapnel and smoke (short-burst hazard avoidance).",
          "challengeType": "Hazard Reaction & Shielding",
          "scoringModifier": "+15 points per successful shield, -8 points if Finch takes direct hit."
        },
        {
          "beatId": 3,
          "description": "The Q&A: During the question-and-answer session, a heckler throws a rubber chicken. While harmless, it's extremely embarrassing for Professor Finch.",
          "challengeType": "NPC Interaction & Public Relations",
          "scoringModifier": "+5 points if chicken is caught before hitting Finch, -3 points if he reacts visibly."
        }
      ]
    },
    {
      "contractId": "paranoid_003",
      "vipPersonality": "The Paranoid",
      "vipBackstory": {
        "name": "Barnaby Buttersworth",
        "description": "A reclusive clockwork toy inventor convinced the world is plotting against him. Barnaby is easily startled and constantly perceives threats where none exist.",
        "motivations":["Maintaining safety", "Avoiding attention", "Ensuring his toys are protected"]
      },
      "contractTitle": "The Toy Fair Debut",
      "narrativeIntro": "Barnaby Buttersworth is reluctantly debuting his latest clockwork creations at the annual toy fair. Surrounded by unfamiliar faces and blinking lights, Barnaby’s anxiety reaches new heights.",
      "storyBeats":[
        {
          "beatId": 1,
          "description": "The Entrance: The sheer number of people triggers Barnaby's paranoia (stress meter increases rapidly). Players must create a clear path through the crowd while minimizing stimuli. Loud noises are particularly detrimental.",
          "challengeType": "Crowd Control & Stress Management",
          "scoringModifier": "+3 points per meter travelled without triggering stress, -10 points for severe panic attack."
        },
        {
          "beatId": 2,
          "description": "The Curious Child: A young child reaches out to touch one of Barnaby's inventions. Players must gently redirect the child before Barnaby spirals into a full-blown breakdown.",
          "challengeType": "NPC Redirection & Calming",
          "scoringModifier": "+12 points for successful redirection, -7 points if child touches toy."
        },
        {
          "beatId": 3,
          "description":"The Security Guard: A well-meaning but overzealous security guard approaches Barnaby, suspecting foul play. Players must diffuse the situation without escalating it.",
          "challengeType": "Dialogue & De-escalation",
          "scoringModifier": "+20 points for successful calming dialogue, -18 points if Barnaby flees in terror."
        }
      ]
    }
  ]
}
```