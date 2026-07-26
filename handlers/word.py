import time

from rubika import (
    send_keypad,
    send_message
)

from database import add_coins
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

        "📝 کامل کردن کلمه\n\n"
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

    from games.word import create_game

    game = create_game(level)

    game["start_time"] = time.time()

    games[chat_id] = game

    send_keypad(

        chat_id,

        "📝 کلمه را کامل کن:\n\n"
        f"{game['hidden']}",

        [
            [
                "🚪 خروج از بازی"
            ]
        ]

    )
    # ==========================================
# بررسی جواب
# ==========================================

def check(chat_id, text):

    # ------------------------------
    # انتخاب سطح
    # ------------------------------

    if chat_id in waiting_level:

        if text == "🟢 آسان":

            waiting_level.remove(chat_id)

            select_level(
                chat_id,
                "easy"
            )

            return


        elif text == "🟡 متوسط":

            waiting_level.remove(chat_id)

            select_level(
                chat_id,
                "medium"
            )

            return


        elif text == "🔴 سخت":

            waiting_level.remove(chat_id)

            select_level(
                chat_id,
                "hard"
            )

            return


        elif text == "🚪 خروج از بازی":

            exit(chat_id)

            return


    # ------------------------------
    # اگر بازی فعال نیست
    # ------------------------------

    if chat_id not in games:

        return


    # ------------------------------
    # خروج
    # ------------------------------

    if text == "🚪 خروج از بازی":

        exit(chat_id)

        return


    from games.word import check as check_answer

    game = games[chat_id]


    # ------------------------------
    # جواب اشتباه
    # ------------------------------

    if not check_answer(
        game,
        text
    ):

        send_message(

            chat_id,

            "❌ اشتباه بود!\n\n"
            f"✅ جواب درست: {game['word']}"

        )

        games.pop(
            chat_id,
            None
        )

        return


    # ------------------------------
    # زمان
    # ------------------------------

    elapsed = round(
        time.time() - game["start_time"],
        2
    )


    # ------------------------------
    # جایزه
    # ------------------------------

    coins = {

        "easy": 5,

        "medium": 10,

        "hard": 20

    }.get(
        game["level"],
        5
    )


    xp = {

        "easy": 3,

        "medium": 5,

        "hard": 8

    }.get(
        game["level"],
        3
    )


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

        "🎉 درست بود!\n\n"

        f"⏱ زمان: {elapsed} ثانیه\n\n"

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

    waiting_level.discard(
        chat_id
    )

    send_message(
        chat_id,
        "🚪 از بازی کامل کردن کلمه خارج شدی."
    )

    games_menu(chat_id)