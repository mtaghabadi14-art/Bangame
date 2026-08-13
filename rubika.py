import os
import time
import requests

from requests.adapters import HTTPAdapter


# ==========================================
# Vexon Rubika API
# ==========================================

TOKEN = os.getenv("RUBIKA_TOKEN")

BASE_URL = (
    f"https://botapi.rubika.ir/v3/{TOKEN}/"
)


# ==========================================
# Session
# ==========================================

session = requests.Session()

adapter = HTTPAdapter(
    pool_connections=20,
    pool_maxsize=20,
    max_retries=0
)

session.mount(
    "https://",
    adapter
)

session.headers.update({
    "Content-Type": "application/json",
    "Connection": "keep-alive"
})


# ==========================================
# API
# ==========================================

def call_api(method, data=None):

    if data is None:
        data = {}

    start = time.time()

    try:

        response = session.post(
            BASE_URL + method,
            json=data,
            timeout=(2, 10)
        )

        response.raise_for_status()

        result = response.json()

        elapsed = time.time() - start

        print(
            f"✅ {method} "
            f"({elapsed:.2f}s)"
        )

        return result

    except requests.exceptions.Timeout:

        print(
            f"❌ {method} Timeout"
        )

        return {
            "status": "TIMEOUT"
        }

    except requests.exceptions.RequestException as e:

        print(
            f"❌ {method}: {e}"
        )

        return {
            "status": "ERROR",
            "error": str(e)
        }

    except Exception as e:

        print(
            f"❌ {method}: {e}"
        )

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
# Send Chat Keypad
# ==========================================

def send_keypad(
    chat_id,
    text,
    buttons
):

    rows = []

    for row in buttons:

        button_row = []

        for button in row:

            if isinstance(button, dict):

                button_row.append({
                    "id": button["id"],
                    "type": "Simple",
                    "button_text": button["text"]
                })

            else:

                button_row.append({
                    "id": button,
                    "type": "Simple",
                    "button_text": button
                })

        rows.append({
            "buttons": button_row
        })

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
# Send Inline Keypad
# ==========================================

def send_inline_keypad(
    chat_id,
    text,
    buttons
):

    rows = []

    for row in buttons:

        button_row = []

        for button in row:

            button_row.append({
                "id": button["id"],
                "type": "Simple",
                "button_text": button["text"]
            })

        rows.append({
            "buttons": button_row
        })

    return call_api(
        "sendMessage",
        {
            "chat_id": chat_id,
            "text": text,
            "inline_keypad": {
                "rows": rows
            }
        }
    )


# ==========================================
# Remove Keypad
# ==========================================

def remove_keypad(
    chat_id,
    text="✅"
):

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
# Delete Message
# ==========================================

def delete_message(
    chat_id,
    message_id
):

    return call_api(
        "deleteMessage",
        {
            "chat_id": chat_id,
            "message_id": message_id
        }
    )