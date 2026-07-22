import os
import time
import requests


# ==========================================
# Bangame Rubika API v2
# ==========================================

TOKEN = os.getenv("RUBIKA_TOKEN")

BASE_URL = f"https://botapi.rubika.ir/v3/{TOKEN}/"


# ==========================================
# Session
# ==========================================

session = requests.Session()

session.headers.update({
    "Content-Type": "application/json"
})


# ==========================================
# API
# ==========================================

def call_api(method, data=None):

    if data is None:
        data = {}

    try:

        start = time.time()

        response = session.post(
            BASE_URL + method,
            json=data,
            timeout=10
        )

        response.raise_for_status()

        result = response.json()

        end = time.time()

        print(f"✅ {method} ({end-start:.2f}s)")

        return result

    except requests.exceptions.Timeout:

        print("❌ Timeout")

        return {
            "status": "TIMEOUT"
        }

    except Exception as e:

        print("❌", e)

        return {
            "status": "ERROR",
            "error": str(e)
        }


# ==========================================
# Send Message
# ==========================================

def send_message(chat_id, text):

    return call_api(
        "sendMessage",
        {
            "chat_id": chat_id,
            "text": text
        }
    )


# ==========================================
# Send Keypad
# ==========================================

def send_keypad(chat_id, text, buttons):

    rows = []

    for row in buttons:

        button_row = []

        for button in row:

            if isinstance(button, dict):

                button_row.append(
                    {
                        "id": button["id"],
                        "type": "Simple",
                        "button_text": button["text"]
                    }
                )

            else:

                button_row.append(
                    {
                        "id": button,
                        "type": "Simple",
                        "button_text": button
                    }
                )

        rows.append(
            {
                "buttons": button_row
            }
        )

    return call_api(
        "sendMessage",
        {
            "chat_id": chat_id,
            "text": text,
            "chat_keypad_type": "New",
            "chat_keypad": {
                "rows": rows,
                "resize_keyboard": True
            }
        }
    )
# ==========================================
# Remove Keypad
# ==========================================

def remove_keypad(chat_id, text="✅"):

    return call_api(
        "sendMessage",
        {
            "chat_id": chat_id,
            "text": text,
            "chat_keypad_type": "Remove"
        }
    )


# ==========================================
# Get Bot Information
# ==========================================

def get_me():

    return call_api(
        "getMe"
    )


# ==========================================
# Update Webhook
# ==========================================

def update_bot_endpoint(url):

    return call_api(
        "updateBotEndpoints",
        {
            "url": url,
            "type": "ReceiveUpdate"
        }
    )


# ==========================================
# پایان فایل
# Bangame Rubika API v2
# ==========================================