class Contract:
    def __init__(self, id, name, prereqs=None):
        self.id = int(id)
        self.name = name
        self.prereqs = [int(p) for p in (prereqs or [])]
    def are_prereqs_met(self, unlock_status):
        norm = {int(k): bool(v) for k, v in unlock_status.items()}
        for pid in self.prereqs:
            if not norm.get(int(pid), False):
                return False
        return True

class ContractProgressionLock:
    def __init__(self):
        self.contracts = [Contract(1, "Daily VIP Escort", []), Contract(2, "Tether Stress Test", [1])]
        self.unlock_status = {int(c.id): False for c in self.contracts}
        self.unlock_status[1] = True
    def current_id(self):
        unlocked = [int(k) for k,v in self.unlock_status.items() if v]
        return max(unlocked) if unlocked else 1
    def current_contract(self):
        return "Daily VIP Escort"
    def progress_to_next(self, cid):
        return True
    def get_save_data(self):
        return self.unlock_status
    def restore(self, d):
        pass
