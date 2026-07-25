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

        "🧠 بازی حافظه\n\n"
        "سطح را انتخاب کن:",

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
# انتخاب سطح
# ==========================================

def select_level(chat_id, level):

    from games.memory import create_game


    game = create_game(level)


    game["start_time"] = time.time()


    games[chat_id] = game



    sequence = " ".join(
        game["sequence"]
    )


    send_message(
        chat_id,

        "🧠 حافظه را به خاطر بسپار!\n\n"
        f"{sequence}\n\n"
        "⏳ ۵ ثانیه فرصت داری..."
    )


    time.sleep(5)


    send_keypad(
        chat_id,

        "✅ حالا دنباله را وارد کن:",

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


    # انتخاب سطح

    if chat_id in waiting_level:


        if text == "🟢 آسان":

            waiting_level.remove(chat_id)

            select_level(
                chat_id,
                "easy"
            )


        elif text == "🟡 متوسط":

            waiting_level.remove(chat_id)

            select_level(
                chat_id,
                "medium"
            )


        elif text == "🔴 سخت":

            waiting_level.remove(chat_id)

            select_level(
                chat_id,
                "hard"
            )


        elif text == "🚪 خروج از بازی":

            exit(chat_id)


        return



    if chat_id not in games:

        return



    from games.memory import check as check_answer


    game = games[chat_id]



    if text == "🚪 خروج از بازی":

        exit(chat_id)

        return



    if not check_answer(
        game,
        text
    ):


        send_message(
            chat_id,

            "❌ اشتباه بود!\n\n"
            f"جواب درست:\n"
            f"{game['answer']}"
        )


        games.pop(
            chat_id,
            None
        )

        return



    elapsed = round(
        time.time() - game["start_time"],
        2
    )



    rewards = {

        "easy": 5,

        "medium": 10,

        "hard": 20

    }


    xp_rewards = {

        "easy": 3,

        "medium": 5,

        "hard": 8

    }



    coins = rewards.get(
        game["level"],
        5
    )


    xp = xp_rewards.get(
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

        "🎉 عالی بود!\n\n"
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


    waiting_level.discard(
        chat_id
    )


    send_message(
        chat_id,
        "🚪 از بازی حافظه خارج شدی."
    )


    games_menu(chat_id)