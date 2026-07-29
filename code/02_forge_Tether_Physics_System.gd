```gdscript
# TetherPhysics.gd
extends Node2D

# Signals
signal tether_tension_changed(tension)
signal tether_slack_changed(slack)

# Constants
const MAX_TENSION = 100.0
const MIN_SLACK = 0.1
const IDEAL_TENSION_RANGE = (30.0, 70.0) # Tuple for ideal tension range

# Variables
var bodyguards = []
var vip_position : Vector2
var tether_length : float
var current_tension : float
var current_slack : float

func _ready():
    connect("tether_tension_changed", self, "_on_tether_tension_changed")
    connect("tether_slack_changed", self, "_on_tether_slack_changed")

# Add bodyguards to the tether system
func add_bodyguard(bodyguard):
    bodyguards.append(bodyguard)

# Update function
func _process(delta):
    update_tether_physics()
    untangle_with_environment()

# Update tether physics: tension and slack calculations
func update_tether_physics():
    var total_length = 0.0
    for bodyguard in bodyguards:
        total_length += position.distance_to(bodyguard.position)
    current_tension = clamp(total_length / len(bodyguards), MIN_SLACK, MAX_TENSION)
    current_slack = current_tension - IDEAL_TENSION_RANGE.x

    emit_signal("tether_tension_changed", current_tension)
    emit_signal("tether_slack_changed", current_slack)

# Collision detection with environmental objects and automatic tangling/untangling mechanics
func untangle_with_environment():
    for bodyguard in bodyguards:
        var collision_objects = get_colliding_objects()
        for obj in collision_objects:
            if obj.is_in_group("Environment"):
                # Calculate the direction vector from the bodyguard to the environment object
                var dir = (obj.position - bodyguard.position).normalized()

                # Apply a small force away from the object to untangle
                bodyguard.apply_force(dir * 5.0)

# Signal handler for tension change events
func _on_tether_tension_changed(tension):
    if tension > MAX_TENSION:
        vip_position += (vip_position - position).normalized() * tension

# Signal handler for slack change events
func _on_tether_slack_changed(slack):
    if slack < MIN_SLACK:
        vip_position -= (position - vip_position).normalized() * slack
```