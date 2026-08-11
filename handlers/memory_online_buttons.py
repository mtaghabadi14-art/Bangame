from rubika import send_keypad


# ==========================================
# منوی Lobby بازی حافظه آنلاین
# ==========================================

def memory_lobby_menu(
    chat_id,
    room,
    is_host=False
):

    players_text = ""

    for player in room.players:

        if player == room.host:
            players_text += f"👑 {player}\n"

        else:
            players_text += f"👤 {player}\n"

    text = (
        "🧠 اتاق بازی حافظه\n\n"
        f"🔑 کد اتاق: {room.room_id}\n\n"
        f"👥 بازیکنان: "
        f"{len(room.players)} / "
        f"{room.max_players}\n\n"
        f"{players_text}\n"
    )

    if len(room.players) < room.min_players:

        text += (
            "\n⏳ منتظر بازیکنان بیشتر..."
        )

    else:

        text += (
            "\n✅ بازیکنان کافی هستند."
        )

    # ==========================================
    # منوی میزبان
    # ==========================================

    if is_host:

        if len(room.players) >= room.min_players:

            send_keypad(
                chat_id,
                text,
                [
                    ["▶️ شروع بازی"],
                    ["🚪 خروج از اتاق"]
                ]
            )

        else:

            send_keypad(
                chat_id,
                text,
                [
                    ["🚪 خروج از اتاق"]
                ]
            )

    # ==========================================
    # منوی بازیکن
    # ==========================================

    else:

        send_keypad(
            chat_id,
            text,
            [
                ["🚪 خروج از اتاق"]
            ]
        )


# ==========================================
# پیام نمایش ترتیب
# ==========================================

def memory_show_message(
    chat_id,
    sequence_text,
    seconds
):

    send_keypad(
        chat_id,
        (
            "🧠 بازی حافظه شروع شد!\n\n"
            "👀 ترتیب را به خاطر بسپار:\n\n"
            f"{sequence_text}\n\n"
            f"⏳ {seconds} ثانیه وقت داری!"
        ),
        []
    )


# ==========================================
# پیام بعد از حذف ترتیب
# ==========================================

def memory_answer_message(chat_id):

    send_keypad(
        chat_id,
        (
            "🧠 حالا ترتیب را بفرست!\n\n"
            "😂 ایموجی‌ها را دقیقاً "
            "با همان ترتیب ارسال کن.\n\n"
            "⚠️ فاصله مهم نیست؛ "
            "ترتیب مهم است."
        ),
        [
            ["🚪 خروج از بازی"]
        ]
    )


# ==========================================
# پیام جواب اشتباه
# ==========================================

def wrong_answer_message(chat_id):

    send_keypad(
        chat_id,
        (
            "❌ ترتیب اشتباه بود!\n\n"
            "دوباره تلاش کن. 🧠"
        ),
        [
            ["🚪 خروج از بازی"]
        ]
    )


# ==========================================
# پیام برنده
# ==========================================

def winner_message(
    chat_id,
    nickname
):

    send_keypad(
        chat_id,
        (
            "🏆 برنده بازی حافظه!\n\n"
            f"🥇 {nickname}\n\n"
            "⚡ اولین نفری بود که "
            "ترتیب را درست فرستاد!"
        ),
        [
            ["🚪 خروج از بازی"]
        ]
    )