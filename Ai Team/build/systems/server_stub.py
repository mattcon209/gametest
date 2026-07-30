class ServerStub:
    def __init__(self): self.sync_count = 0
    def start(self): pass
    def sync_tether(self, vip, bgs): self.sync_count += 1
    def stop(self): pass
    def status(self): return f"Running {self.sync_count}"
