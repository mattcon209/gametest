Okay, here's the asset design specifications and a breakdown of my vision for contract objective visuals – environment assets and UI icons specifically as requested. I’ll organize this into sections: Environment Assets, UI Icons (with detailed style guides), and overall Art Direction Notes.  I'm presenting what *would* be outputted as files from my production pipeline.

**1. ENVIRONMENT ASSETS - Contract Objective Markers**

These markers will visually communicate the objective location within a level. Given the physics-driven chaos, they need to be readable but also stylistically integrated into varied environments.  They'll be modular and placeable by designers for flexibility.

*   **Rescue Marker (File: `rescue_marker_01.fbx`, `rescue_marker_01_diffuse.png`, `rescue_marker_01_normal.png`):**
    *   **Description:** A stylized, slightly distressed lamppost with a single, glowing blue lantern hanging from it. The lantern emits a soft pulse of light.  Base material is aged metal with subtle grime and rust detail.  Should look integrated into city scenes *and* more rundown environments.
    *   **Poly Count Target:** < 500 tris (optimize for performance)
    *   **Scale:** Roughly 1.5m tall, to be visible from a distance.
    * **Texture resolution:** 2048x2048 diffuse and normal

*   **Sabotage Marker (File: `sabotage_marker_01.fbx`, `sabotage_marker_01_diffuse.png`, `sabotage_marker_01_normal.png`):**
    *   **Description:**  A crude, hastily painted stencil of a wrench on a brick wall. The paint is peeling and faded, with a subtle red glow emanating from the wrench’s center. The stencil will have a slightly tilted/irregular placement to suggest urgency.
    *   **Poly Count Target:** < 300 tris (can be a simple plane with a texture).
    * **Texture resolution:** 1024x1024 diffuse and normal

*   **Escort Marker (File: `escort_marker_01.fbx`, `escort_marker_01_diffuse.png`, `escort_marker_01_normal.png`):**
    *   **Description:** A tall, slightly crooked banner strung between two poles. The banner features a stylized arrow pointing forward in a bright yellow color against a dark blue background.  The banner material will have subtle wrinkles and folds to avoid appearing flat.
    *   **Poly Count Target:** <700 tris (allowing for some cloth simulation style).
    * **Texture resolution:** 2048x1024 diffuse and normal

**2. UI ICONS - Contract Objective Display**

These icons will be used in the contract selection screen and potentially during gameplay as a reminder of the current objective.  Stylized, clear at small sizes, and visually distinct.

*   **Rescue Icon (File: `icon_rescue.png`, dimensions 128x128):**
    *   **Style:** Silhouette-based. A stylized figure being pulled from rubble by a hand. Very simple shapes, limited color palette (blues, grays). Outline is thin and sharp.
    *   **Color Palette:** Primarily muted blues/grays with a highlight of brighter blue for the 'rescue' glow effect.
    *   **File Format:** PNG - transparent background required.

*   **Sabotage Icon (File: `icon_sabotage.png`, dimensions 128x128):**
    *   **Style:** Slightly more chaotic and distressed than the rescue icon. A stylized gear with a cracked appearance and sparks emanating from it. Uses overlapping shapes to imply destruction.
    *   **Color Palette:** Red/Orange/Dark Gray – conveying danger and disruption. Slight chromatic aberration effect for added visual noise.
    *   **File Format:** PNG - transparent background required.

*   **Escort Icon (File: `icon_escort.png`, dimensions 128x128):**
    *   **Style:** Clean, directional, and formal-feeling. A stylized arrow within a shield shape. Simple gradients.
    *   **Color Palette:** Yellow/Dark Blue - conveying guidance and protection.  Subtle inner glow effect.
    *   **File Format:** PNG - transparent background required.



**3. ART DIRECTION NOTES (Overall)**

*   **Visual Tone:** Slightly cartoonish but grounded in a believable reality.  Exaggeration is key for comedic effect, but assets shouldn't be *too* unrealistic. A bit of "dieselpunk" influence could work well: aged machinery and materials.
*   **Material Style:** Focus on stylized realism - not hyper-detailed photorealism.  Subtle imperfections and wear are important to convey the budget/low-tech feel.
*   **Lighting:** Environmental lighting should be dynamic and often harsh, emphasizing the chaotic nature of the gameplay. The objective markers themselves *should* glow softly to provide visual cues even in dimly lit areas.
* **Resolution:** Target 1080p display resolution, optimize models and textures accordingly for smooth performance on a range of hardware.



---

This is my initial response based on your prompt. I am ready for any follow-up questions or modifications you require concerning environment assets/UI icons.