import requests
import os


TOKEN = "BJEHHC0DFLTFEXNDDLULGDUYRUDJOHJYWSLXZVTFBJVISBMORNJPVBHCTEDHBXGC"

if not TOKEN:
    print("⚠️ RUBIKA_TOKEN پیدا نشد!")


API_URL = f"https://botapi.rubika.ir/v3/{TOKEN}"


def send_message(chat_id, text):
    """
    ارسال پیام به کاربر
    """

    url = API_URL + "/sendMessage"

    data = {
        "chat_id": chat_id,
        "text": text
    }

    try:
        response = requests.post(
            url,
            json=data,
            timeout=10
        )

        return response.json()

    except Exception as e:
        print("Send Message Error:", e)
        return None



def get_me():
    """
    تست اتصال ربات
    """

    url = API_URL + "/getMe"

    try:
        response = requests.post(
            url,
            timeout=10
        )

        return response.json()

    except Exception as e:
        print("GetMe Error:", e)
        return None



def get_updates(offset=None):
    """
    دریافت پیام‌های جدید
    """

    url = API_URL + "/getUpdates"

    data = {
        "limit": 10
    }

    if offset:
        data["offset_id"] = offset

    try:
        response = requests.post(
            url,
            json=data,
            timeout=10
        )

        return response.json()

    except Exception as e:
        print("Get Updates Error:", e)
        return None