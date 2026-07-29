```gdscript
# DailyContractSaveSystem.gd
extends Node

@export var save_file_path: String = "user://daily_contracts.json"

var daily_contract_data: Dictionary = {}

func _ready():
    load_saved_data()

func save_daily_contract_data(data: Dictionary):
    daily_contract_data = data
    save_to_file()

func load_saved_data() -> Dictionary:
    var file = FileAccess.open(save_file_path, FileAccess.READ)
    if file:
        var json_data = file.get_as_text()
        file.close()
        daily_contract_data = JSON.parse(json_data).result
    else:
        daily_contract_data = {}
    return daily_contract_data

func save_to_file():
    var json_data = JSON.print(daily_contract_data)
    var file = FileAccess.open(save_file_path, FileAccess.WRITE)
    if file:
        file.store_string(json_data)
        file.close()
```