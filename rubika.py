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
        print("RESULT:", result)

        return result


    except Exception as e:

        print("Rubika Error:", e)

        return {
            "status": "ERROR",
            "error": str(e)
        }



def get_me():

    return call_api(
        "getMe"
    )



def get_updates(offset_id=None, limit=10):

    data = {
        "limit": limit
    }

    if offset_id:
        data["offset_id"] = offset_id


    return call_api(
        "getUpdates",
        data
    )



def send_message(chat_id, text):

    return call_api(
        "sendMessage",
        {
            "chat_id": chat_id,
            "text": text,
            "reply_to_message_id": None
        }
    )



def update_bot_endpoint(url):

    return call_api(
        "updateBotEndpoints",
        {
            "url": url,
            "type": "ReceiveUpdate"
        }
    )