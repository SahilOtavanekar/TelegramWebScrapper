import requests
import json
import time

URL = "https://sahilotavanekar--telegram-lead-bot-webhook.modal.run"

mock_update = {
    "update_id": int(time.time()),
    "message": {
        "message_id": 123,
        "from": {
            "id": 123456789,
            "is_bot": False,
            "first_name": "Test",
            "username": "testuser"
        },
        "chat": {
            "id": 123456789,
            "first_name": "Test",
            "username": "testuser",
            "type": "private"
        },
        "date": int(time.time()),
        "text": "Hello, are you working?"
    }
}

print(f"Sending POST request to {URL}...")
response = requests.post(URL, json=mock_update)

print(f"Status Code: {response.status_code}")
print(f"Response Body: {response.text}")
