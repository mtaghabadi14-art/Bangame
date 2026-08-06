from rubika import send_keypad


def profile_menu(chat_id):

    send_keypad(
        chat_id,
        "👤 مدیریت پروفایل:",
        [
            ["✏️ تغییر لقب"],
            ["برگشت"]
        ]
    )