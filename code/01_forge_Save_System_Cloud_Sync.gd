```gdscript
# SaveSystem.gd (Save System with Cloud Sync)
extends Node

var save_data := {}
var api_url := "https://your-api-endpoint.com/save"

func _ready():
    # Load saved data from cloud at startup
    load_save_from_cloud()

func save_game(data):
    # Update local save data
    save_data = data

    # Save to cloud
    save_to_cloud()

    # Optionally, save locally as well
    var file := FileAccess.open("user://save.json", FileAccess.WRITE)
    if file:
        file.store_string(to_json(save_data))
        file.close()

func load_save_from_cloud():
    var request = HTTPRequest.new()
    add_child(request)

    # Set the URL for retrieving save data
    request.request_completed.connect(func(response):
        if response.result != HTTPClient.RESULT_OK:
            print("Failed to retrieve save from cloud: ", response.get_status())
            return

        var json_data = JSON.parse(response.get_body().get_string_from_utf8()).result
        save_data = json_data
    end)

    request.request(request_completed)
    request.set_request_url(api_url + "/retrieve")
    request.post([])
    request.connect()

func save_to_cloud():
    # Convert save data to JSON string for API request
    var json_string = to_json(save_data)

    var headers = [
        "Content-Type: application/json"
    ]

    # Send the save data to the cloud endpoint
    var request = HTTPRequest.new()
    add_child(request)
    request.request_completed.connect(func(response):
        if response.result != HTTPClient.RESULT_OK:
            print("Failed to save to cloud: ", response.get_status())
            return

        print("Save data uploaded successfully.")
    end)

    request.set_request_url(api_url + "/save")
    request.set_headers(headers)
    var request_data = [
        json_string
    ]
    request.post(request_data)
```

This script handles the loading and saving of game save data to a cloud endpoint using JSON storage. The `save_game` function updates the local save data and uploads it to the cloud, while the `load_save_from_cloud` function retrieves the latest saved data from the cloud when starting the game.

Note: Replace `"https://your-api-endpoint.com/save"` with your actual API endpoint for handling save data. Also, ensure proper security measures are in place on both client and server side to secure sensitive data and prevent unauthorized access.

This code is designed for use within a Godot project using GDScript.