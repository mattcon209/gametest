```python
class VIP:
    def __init__(self, personality):
        self.personality = personality
        self.stress = 0
        self.position = (0, 0)
        self.destination = (100, 100)

    def update_stress(self, amount):
        if self.personality == "The Paranoid":
            self.stress += amount * 2
        else:
            self.stress += amount

    def get_panic_direction(self, obstacles):
        # Simplified panic pathfinding logic
        target = self.destination
        current = self.position
        direction = (target[0] - current[0], target[1] - current[1])
        
        # Avoid obstacles by modifying direction
        for obstacle in obstacles:
            if self.is_near(obstacle):
                direction = self.avoid_obstacle(direction, obstacle)
        
        return direction

    def is_near(self, obstacle):
        # Check if VIP is near an obstacle
        return abs(self.position[0] - obstacle[0]) < 5 and abs(self.position[1] - obstacle[1]) < 5

    def avoid_obstacle(self, direction, obstacle):
        # Simple avoidance logic
        new_direction = (direction[0], direction[1])
        if self.position[0] < obstacle[0]:
            new_direction = (new_direction[0] + 2, new_direction[1])
        elif self.position[0] > obstacle[0]:
            new_direction = (new_direction[0] - 2, new_direction[1])
        
        if self.position[1] < obstacle[1]:
            new_direction = (new_direction[0], new_direction[1] + 2)
        elif self.position[1] > obstacle[1]:
            new_direction = (new_direction[0], new_direction[1] - 2)
        
        return new_direction

# Example usage
vip = VIP("The Paranoid")
obstacles = [(30, 40), (50, 60)]
panic_direction = vip.get_panic_direction(obstacles)
print(f"Panic Direction: {panic_direction}")
```

This code refines the VIP's panic pathfinding algorithm to ensure it avoids obstacles and navigates complex environments effectively during stress-induced sprints. It tests with the "The Paranoid" personality, but can be extended to other personalities by adjusting the `update_stress` method accordingly.