from rubika import send_keypad


def main_menu(chat_id):

    send_keypad(
        chat_id,
        "👋 دوباره خوش آمدی به Bangame!\n\nاز منوی زیر انتخاب کن 👇",
        [
            ["🎮 بازی‌ها", "👤 پروفایل"],
            ["🪙 کیف پول", "🎁 جایزه روزانه"],
            ["🏠 اتاق بازی"]
        ]
    )


def games_menu(chat_id):

    send_keypad(
        chat_id,
        "🎮 یکی از بازی‌ها را انتخاب کن:",
        [
            ["✂️ سنگ کاغذ قیچی"],
            ["🔢 حدس عدد"],
            ["🎲 تاس"],
            ["🚪 خروج"]
        ]
    )


def room_menu(chat_id):

    send_keypad(
        chat_id,
        "🏠 مدیریت اتاق",
        [
            ["➕ ساخت اتاق"],
            ["🚪 ورود به اتاق"],
            ["⬅️ برگشت"]
        ]
    )


def create_room_menu(chat_id):

    send_keypad(
        chat_id,
        "🎮 بازی موردنظر را انتخاب کن:",
        [
            ["✂️ سنگ کاغذ قیچی"],
            ["⭕ دوز"],
            ["🃏 UNO"],
            ["🎭 مافیا"],
            ["🕵️ جاسوس"],
            ["🚪 خروج"]
        ]
    )