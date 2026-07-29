```gdscript
extends Node2D

@export var slow_motion_duration = 1.0
@export var time_scale_normal = 1.0
@export var time_scale_slow = 0.25

func _ready():
    # Connect to the diving start signal from the player character
    $PlayerCharacter.connect("start_dive", self, "_on_start_dive")

func _on_start_dive():
    # Start the slow-motion effect
    get_tree().change_scene_paused = true
    get_tree().paused = true

    # Apply dramatic lighting effects
    var ambient_light = $AmbientLight
    ambient_light.light_energy *= 2.0

    # Use tweening to gradually reduce time scale and create a slow-motion effect
    var tween = get_tree().create_tween()
    tween.tween_property(get_tree(), "paused", true, 0.1)
    tween.tween_property(get_tree(), "time_scale", time_scale_slow, slow_motion_duration, Tween.TRANS_LINEAR, Tween.EASE_IN_OUT)

    # Wait for the slow-motion duration and then revert to normal
    yield(get_tree().create_timer(slow_motion_duration), "timeout")

    # Revert time scale and lighting effects back to normal
    tween.tween_property(get_tree(), "time_scale", time_scale_normal, 0.1)
    ambient_light.light_energy /= 2.0

    get_tree().paused = false
    get_tree().change_scene_paused = false
```

This script applies a slow-motion effect with dramatic lighting when the player character starts diving. It uses Godot's tweening system to smoothly transition between normal and slow motion, as well as adjusting ambient light intensity for an enhanced dramatic effect.