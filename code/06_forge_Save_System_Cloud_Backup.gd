```gdscript
extends Resource

# Constants for Cloud Storage
const CLOUD_STORAGE_URL = "https://your-cloud-storage-url.com"
const API_KEY = "your_api_key_here"

var save_data : Dictionary
var last_version_saved : int = 0

func _init():
    # Initialize the save data dictionary
    save_data = {
        "save_state": {},
        "version": 1
    }
    load_cloud_save()

# Save data locally and to cloud
func save_game(save_state : Dictionary):
    # Update local save data
    save_data["save_state"] = save_state
    save_data["version"] += 1

    var json_string = to_json(save_data)
    FileAccess.open("user://save_file.json", FileAccess.WRITE).store_string(json_string)

    upload_save_to_cloud()

# Load local save and cloud save, resolving conflicts
func load_game() -> Dictionary:
    if FileAccess.file_exists("user://save_file.json"):
        var json_string = FileAccess.open("user://save_file.json", FileAccess.READ).get_as_text()
        save_data = parse_json(json_string)

    download_cloud_save()

    return save_data["save_state"]

# Upload the latest save to cloud
func upload_save_to_cloud():
    # Convert dictionary to JSON string for HTTP request payload
    var json_string = to_json(save_data)
    var url = CLOUD_STORAGE_URL + "/upload?api_key=" + API_KEY

    var http_request = HTTPRequest.new()
    add_child(http_request)

    http_request.request_completed.connect(self._on_http_request_completed)
    var error = http_request.request(url, [], true, HTTPClient.METHOD_POST, json_string)
    if error != OK:
        print("Error in uploading save to cloud: ", error)

# Download the latest save from cloud
func download_cloud_save():
    var url = CLOUD_STORAGE_URL + "/download?api_key=" + API_KEY

    var http_request = HTTPRequest.new()
    add_child(http_request)

    http_request.request_completed.connect(self._on_http_request_completed)
    var error = http_request.request(url, [], true, HTTPClient.METHOD_GET, "")
    if error != OK:
        print("Error in downloading save from cloud: ", error)

# Handle HTTP request completion
func _on_http_request_completed(request, result, response_code, headers, body):
    if response_code == 200 and result == HTTPRequest.RESULT_SUCCESS:
        if headers["Content-Type"] == "application/json":
            var json_data = parse_json(body.get_string_from_utf8())
            # Conflict resolution: latest version wins
            if int(json_data.version) > save_data.version:
                save_data = json_data
                FileAccess.open("user://save_file.json", FileAccess.WRITE).store_string(to_json(save_data))
    else:
        print("HTTP request failed with code ", response_code, ": ", body.get_string_from_utf8())
```

This script provides a basic framework for saving and loading game data both locally and to the cloud, including conflict resolution based on version numbers. You should replace `"https://your-cloud-storage-url.com"` and `"your_api_key_here"` with your actual cloud storage URL and API key.

For production-ready code, you'd want to handle more edge cases such as network failures, rate limiting, encryption of save data, etc., depending on the requirements.