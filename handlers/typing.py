import time

from rubika import (
    send_keypad,
    send_message
)

from database import add_coins
from level import give_xp

games = {}


# ==========================================
# شروع بازی
# ==========================================

def start(chat_id):

    from games.typing import create_game

    game = create_game()

    game["start_time"] = time.time()

    games[chat_id] = game

    send_keypad(
        chat_id,
        "⌨️ سرعت تایپ\n\n"
        "جمله زیر را دقیقا بنویس:\n\n"
        f"{game['sentence']}",
        [
            ["🚪 خروج از بازی"]
        ]
    )


# ==========================================
# بررسی پاسخ
# ==========================================

def check(chat_id, text):

    if chat_id not in games:
        return

    from games.typing import check as check_answer

    game = games[chat_id]

    # خروج
    if text == "🚪 خروج از بازی":

        exit(chat_id)

        return

    # جواب اشتباه
    if not check_answer(game, text):

        send_message(
            chat_id,
            "❌ جمله اشتباه است.\n"
            "دوباره تلاش کن."
        )

        return

    elapsed = round(
        time.time() - game["start_time"],
        2
    )

    reward = 8
    xp = 3

    add_coins(
        chat_id,
        reward
    )

    give_xp(
        chat_id,
        xp
    )

    send_message(
        chat_id,
        "🎉 آفرین!\n\n"
        f"⏱ زمان: {elapsed} ثانیه\n"
        f"🪙 +{reward} سکه\n"
        f"⭐ +{xp} XP"
    )

    games.pop(
        chat_id,
        None
    )


# ==========================================
# خروج
# ==========================================

def exit(chat_id):

    from handlers.menu import games_menu

    games.pop(
        chat_id,
        None
    )

    send_message(
        chat_id,
        "🚪 از بازی خارج شدی."
    )

    games_menu(chat_id)