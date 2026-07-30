import json
from pathlib import Path
class SaveSystem:
    def __init__(self, save_path="save.json"):
        self.local_path = Path(__file__).parent.parent / "save_file.json"
    def save_game(self, data):
        self.local_path.write_text(json.dumps(data, indent=2))
        return True
    def load_save(self):
        return None
