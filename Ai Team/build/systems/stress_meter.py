class StressMeter:
    def __init__(self):
        self.value = 0.0
    def update(self, tension, delta=0.016):
        self.value = min(100, self.value + tension*0.1)
    def is_panicking(self):
        return self.value > 80
