import json
import telebot

mock_update = {
    "update_id": 123456,
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
        "date": 1234567,
        "text": "Hello, are you working?"
    }
}

try:
    update = telebot.types.Update.de_json(json.dumps(mock_update))
    print("Parsed OK:", update.message.text)
except Exception as e:
    import traceback
    traceback.print_exc()
