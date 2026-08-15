import os
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

def call_api(
    method,
    data=None
):

    if data is None:
        data = {}

    try:

        response = session.post(
            BASE_URL + method,
            json=data,
            timeout=(5, 20)
        )

        result = response.json()

        status = result.get(
            "status",
            "UNKNOWN"
        )

        if status == "OK":

            print(
                f"📤 {method} → OK"
            )

        else:

            print(
                f"❌ {method} → {status}"
            )

        return result

    except requests.exceptions.ConnectTimeout:

        print(
            f"⏱️ {method} → CONNECT TIMEOUT"
        )

        return {
            "status": "TIMEOUT",
            "error": "connect_timeout"
        }

    except requests.exceptions.ReadTimeout:

        print(
            f"⏱️ {method} → READ TIMEOUT"
        )

        return {
            "status": "TIMEOUT",
            "error": "read_timeout"
        }

    except requests.exceptions.ConnectionError as e:

        print(
            f"🔌 {method} → CONNECTION ERROR"
        )

        return {
            "status": "ERROR",
            "error": str(e)
        }

    except requests.exceptions.HTTPError as e:

        print(
            f"🌐 {method} → HTTP ERROR"
        )

        return {
            "status": "ERROR",
            "error": str(e)
        }

    except Exception as e:

        print(
            f"❌ {method} → ERROR"
        )

        return {
            "status": "ERROR",
            "error": str(e)
        }

# ==========================================
# Send Message
# ==========================================

def send_message(
    chat_id,
    text
):

    return call_api(
        "sendMessage",
        {
            "chat_id": chat_id,
            "text": text
        }
    )


# ==========================================
# ساخت Button
# ==========================================

def build_button(button):

    if isinstance(button, dict):

        button_id = button.get(
            "id",
            button.get(
                "text",
                ""
            )
        )

        button_text = button.get(
            "text",
            str(button_id)
        )

    else:

        button_id = str(
            button
        )

        button_text = str(
            button
        )

    return {
        "id": button_id,
        "type": "Simple",
        "button_text": button_text
    }


# ==========================================
# ساخت Rows
# ==========================================

def build_rows(buttons):

    rows = []

    for row in buttons:

        button_row = []

        for button in row:

            button_row.append(
                build_button(
                    button
                )
            )

        rows.append({
            "buttons": button_row
        })

    return rows


# ==========================================
# Send Chat Keypad
# ==========================================

def send_keypad(
    chat_id,
    text,
    buttons
):

    rows = build_rows(
        buttons
    )

    data = {
        "chat_id": chat_id,
        "text": text,
        "chat_keypad_type": "New",
        "chat_keypad": {
            "rows": rows,
            "resize_keyboard": True
        }
    }

    return call_api(
        "sendMessage",
        data
    )


# ==========================================
# Edit Chat Keypad
# ==========================================

def edit_chat_keypad(
    chat_id,
    buttons
):

    rows = build_rows(
        buttons
    )

    data = {
        "chat_id": chat_id,
        "chat_keypad_type": "New",
        "chat_keypad": {
            "rows": rows,
            "resize_keyboard": True
        }
    }

    return call_api(
        "editChatKeypad",
        data
    )


# ==========================================
# Remove Chat Keypad
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

def update_bot_endpoint(
    url
):

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


# ==========================================
# Edit Message Text
# ==========================================

def edit_message_text(
    chat_id,
    message_id,
    text
):

    return call_api(
        "editMessageText",
        {
            "chat_id": chat_id,
            "message_id": message_id,
            "text": text
        }
    )