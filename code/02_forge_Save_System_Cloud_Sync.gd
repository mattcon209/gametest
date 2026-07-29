```gdscript
# SaveSystem.gd (Godot Script)
extends Node

var save_data = {}
var cloud_save_url = "https://your-cloud-save-endpoint.com/save"

func _ready():
    var save_file = FileAccess.open("user://save.json", FileAccess.READ)
    if save_file:
        save_data = JSON.parse(save_file.get_as_text()).result
        save_file.close()
    else:
        save_data = {}

# Save to local and cloud
func save_game(data):
    save_data = data
    var save_json = JSON.print(save_data)
    var save_file = FileAccess.open("user://save.json", FileAccess.WRITE)
    save_file.store_string(save_json)
    save_file.close()

    # Sync with cloud
    var error = _cloud_sync_save(save_json)
    if error != OK:
        print("Failed to sync save with cloud: ", error)

# Load from local and cloud
func load_game():
    _load_from_cloud()
    if not FileAccess.file_exists("user://save.json"):
        _create_local_save_file()

    var save_file = FileAccess.open("user://save.json", FileAccess.READ)
    save_data = JSON.parse(save_file.get_as_text()).result
    save_file.close()

# Load from cloud and update local file if needed
func _load_from_cloud():
    var http_request = HTTPRequest.new()
    add_child(http_request)

    var err = http_request.request(cloud_save_url)
    if err != OK:
        print("Failed to load save from cloud: ", err)
        return

    # Wait for response and update local file
    yield(http_request, "request_completed")
    if http_request.result == HTTPRequest.RESULT_OK:
        var save_json = http_request.get_response_body().get_string_from_utf8()
        var save_file = FileAccess.open("user://save.json", FileAccess.WRITE)
        save_file.store_string(save_json)
        save_file.close()

# Sync local save to cloud
func _cloud_sync_save(save_data):
    var http_request = HTTPRequest.new()
    add_child(http_request)

    var response_body = Vary.new()
    response_body.set_var("save", save_data)

    var err = http_request.request(cloud_save_url, [], true, HTTPClient.METHOD_POST, response_body)
    if err != OK:
        print("Failed to sync save with cloud: ", err)
        return err

    yield(http_request, "request_completed")
    if http_request.result == HTTPRequest.RESULT_OK:
        return OK
    else:
        return ERR_FAILURE

# Create local save file from initial data
func _create_local_save_file():
    var default_data = {"player": {"health": 100}, "progress": {"level": 1}}
    var save_json = JSON.print(default_data)
    var save_file = FileAccess.open("user://save.json", FileAccess.WRITE)
    save_file.store_string(save_json)
    save_file.close()
```