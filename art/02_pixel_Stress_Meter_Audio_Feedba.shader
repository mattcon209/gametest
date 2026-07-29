Okay, here’s a plan for the stress meter audio feedback implementation - as shader/palette/VFX – with notes on how this translates to audible cues and music changes. I will provide lists, organized by Stress Meter Stage. This is geared toward integration into an existing audio engine; specific implementation details (mixing, ducking, etc.) are left to Audio Design.

**Overall Philosophy:** The goal is layered feedback: subtle shifts at low stress escalating into full-blown panic as the VIP’s stress climbs. Avoid sudden jarring sounds – prioritize a sense of increasing unease and pressure.

---
## STRESS METER AUDIO FEEDBACK PLAN - "THE DIVA" VIP PERSONALITY (EXAMPLE)

**I. Baseline (0-25% Stress): Calm & Pleasant**

*   **Music:** Ambient, optimistic underscore with gentle instrumentation (e.g., acoustic guitar, soft strings).  Subtle harmonic shifts to slightly alter the perceived mood, without it being readily noticeable.
    *   *Palette Note:* Consider a "brightness" dial on this track - subtly shifting from warm (yellowish) to cooler tones as stress increases throughout the stage. This is visually-linked feedback for players.
*   **Sound FX:**  Very quiet background sounds of pleasant surroundings, such as gentle birdsong or distant traffic – emphasizing an atmosphere of security and comfort.

**II. Moderate Stress (26-50%): Increased Awareness**

*   **Music:**  Introduction of a subtle percussive element (e.g., light hi-hats) on the offbeat, adding a slight sense of urgency. String instrumentation may become slightly more prominent. A very faint pulsing effect on key frequencies - barely perceptible but contributing to a nervous feeling.
    *   *Palette Note:*  Shift background color slightly towards desaturated blues and purples – visually suggesting approaching tension without overt change.
*   **Sound FX:** Introduction of *very* quiet, filtered vocal murmurs/sighs layered under the music. A very subtle click or brief "whoosh" sound whenever something comes close to the VIP (a near-miss hazard) - almost subliminal.

**III. High Stress (51-75%): Noticeable Anxiety**

*   **Music:** Percussion becomes more prominent and complex, introducing faster tempos and slightly discordant rhythms. Strings become more frenetic. Introduction of a repeating musical motif—a short melodic phrase—played with increasing speed and intensity.
    *   *VFX List:* Slight chromatic aberration effect on the VIP's visual model – subtly shifting colors to create a distorted impression.  This is purely visual feedback correlated to audio cues. *Don’t change the underlying textures*.
*   **Sound FX:**  The filtered vocal murmurs become clearer, evolving into brief snippets of anxious whispers ("Oh dear," "Careful!"). Increase intensity and proximity of "near-miss" sound effects - more prominent and frequent. A subtle mechanical whirring sound starts to build – a visual/auditory clue that systems are straining under pressure (correlating to the tether system).

**IV. Critical Stress (76-100%): Panic!**

*   **Music:** The repeating motif becomes increasingly frantic and distorted, almost overwhelming the base music. Introduction of harsher sounds—static, scraping metal—layered underneath.  The overall music volume increases significantly.
    *   *Shader Note:* Very slight screen shake animation triggered by high-stress events - correlated with audio peaks to avoid sensory overload. This uses a vertex shader offset and is minimal in intensity.
*   **Sound FX:** Full panic vocalizations ("I'm frightened!", "Help me!").  Loud, distorted “near-miss” sounds. The mechanical whirring becomes intense and layered with grinding noises. A distinct, repeating alarm sound begins to blare intermittently (short bursts).
    *   *Palette Note:* Screen flash of intense reds/oranges – very brief and infrequent as a last resort warning.

---
## GENERAL NOTES ON IMPLEMENTATION

*   **Dynamic Mixing:** The volume levels for the various audio cues should be dynamically adjusted based on the VIP's personality profile (e.g., “The Paranoid” would start at higher stress levels).
*   **Spatial Audio:**  Utilize spatial audio to position sound effects accurately in 3D space, enhancing immersion and providing directional clues to players. "Near-miss" sounds should originate from the direction of the threat.
*   **Rhythm & Sync:**  Careful synchronization between visual feedback (palette shifts, VFX) and audio cues is crucial for creating a cohesive and impactful experience. These elements should work in tandem to convey the VIP’s stress state.
*   **Avoid Repetition:** Cycle through variations of vocal lines and music motifs to prevent sounds from becoming repetitive and predictable.



---