import time

from rubika import (
    send_keypad,
    send_message
)

from database import (
    add_coins
)

from level import give_xp


games = {}

waiting_level = set()


# ==========================================
# شروع بازی
# ==========================================

def start(chat_id):

    waiting_level.add(chat_id)

    send_keypad(
        chat_id,
        "⚡ محاسبات سریع\n\n"
        "سطح بازی را انتخاب کن:",
        [
            [
                "🟢 آسان",
                "🟡 متوسط"
            ],
            [
                "🔴 سخت"
            ],
            [
                "🚪 خروج از بازی"
            ]
        ]
    )


# ==========================================
# شروع مرحله
# ==========================================

def select_level(chat_id, level):

    from games.math_game import create_game

    game = create_game(level)

    game["start_time"] = time.time()

    games[chat_id] = game

    send_keypad(
        chat_id,
        "⚡ جواب این عبارت را بنویس:\n\n"
        f"🧮 {game['question']}",
        [
            [
                "🚪 خروج از بازی"
            ]
        ]
    )


# ==========================================
# بررسی پاسخ
# ==========================================

def check(chat_id, text):

    if chat_id in waiting_level:

        if text == "🟢 آسان":

            waiting_level.remove(chat_id)
            select_level(chat_id, "easy")

        elif text == "🟡 متوسط":

            waiting_level.remove(chat_id)
            select_level(chat_id, "medium")

        elif text == "🔴 سخت":

            waiting_level.remove(chat_id)
            select_level(chat_id, "hard")

        elif text == "🚪 خروج از بازی":

            exit(chat_id)

        return


    if chat_id not in games:

        return


    if text == "🚪 خروج از بازی":

        exit(chat_id)

        return


    from games.math_game import check as check_answer

    game = games[chat_id]


    if not check_answer(game, text):

        send_message(
            chat_id,
            "❌ جواب اشتباه است.\n"
            "دوباره تلاش کن."
        )

        return


    elapsed = round(
        time.time() - game["start_time"],
        2
    )


    bonus = {

        "easy": 1,
        "medium": 2,
        "hard": 4

    }.get(
        game["level"],
        1
    )


    coins = 5 + bonus
    xp = 3 + bonus


    add_coins(
        chat_id,
        coins
    )

    give_xp(
        chat_id,
        xp
    )


    send_message(
        chat_id,
        "🎉 آفرین!\n\n"
        f"⏱ زمان: {elapsed} ثانیه\n"
        f"🪙 +{coins} سکه\n"
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

    waiting_level.discard(chat_id)

    send_message(
        chat_id,
        "🚪 از بازی خارج شدی."
    )

    games_menu(chat_id)