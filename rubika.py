import os
import requests


TOKEN = os.getenv("RUBIKA_TOKEN")

BASE_URL = f"https://botapi.rubika.ir/v3/{TOKEN}/"



def call_api(method, data=None):

    if data is None:
        data = {}

    try:

        response = requests.post(
            BASE_URL + method,
            json=data,
            timeout=30
        )

        result = response.json()

        print("API:", method)
        print("DATA:", data)
        print("RESULT:", result)

        return result


    except Exception as e:

        print("Rubika Error:", e)

        return {
            "status": "ERROR",
            "error": str(e)
        }



def send_message(chat_id, text):

    return call_api(
        "sendMessage",
        {
            "chat_id": chat_id,
            "text": text
        }
    )



def send_keypad(chat_id, text):

    return call_api(
        "sendMessage",
        {
            "chat_id": chat_id,
            "text": text,
            "chat_keypad_type": "New",
            "chat_keypad": {
                "rows": [
                    {
                        "buttons": [
                            {
                                "id": "profile",
                                "type": "Simple",
                                "button_text": "👤 پروفایل"
                            },
                            {
                                "id": "games",
                                "type": "Simple",
                                "button_text": "🎮 بازی‌ها"
                            }
                        ]
                    },
                    {
                        "buttons": [
                            {
                                "id": "wallet",
                                "type": "Simple",
                                "button_text": "🪙 کیف پول"
                            },
                            {
                                "id": "daily",
                                "type": "Simple",
                                "button_text": "🎁 جایزه روزانه"
                            }
                        ]
                    }
                ],
                "resize_keyboard": True
            }
        }
    )



def get_me():

    return call_api(
        "getMe"
    )



def update_bot_endpoint(url):

    return call_api(
        "updateBotEndpoints",
        {
            "url": url,
            "type": "ReceiveUpdate"
        }
    )