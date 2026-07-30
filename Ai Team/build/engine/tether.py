import math
class TetherSystem:
    def __init__(self, max_tension=5.0, **kwargs):
        self.max_t = max_tension
        self.tensions = {}
    def init_tethers(self, bgs, vip): 
        self.tethers = {f"tether_{b['name']}": 0.0 for b in bgs}
    def update_all(self, vip, bgs, delta=0.016):
        for k in self.tensions:
            self.tensions[k] += 0.1
    def get_max_tension(self):
        return max(self.tensions.values()) if self.tensions else 0.0
