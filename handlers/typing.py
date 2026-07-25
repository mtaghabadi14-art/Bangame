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

        "⌨️ سرعت تایپ شروع شد!\n\n"
        "جمله زیر را دقیقا تایپ کن:\n\n"
        f"📝 {game['sentence']}",

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

    if chat_id not in games:
        return


    from games.typing import check as check_answer


    game = games[chat_id]


    # خروج

    if text == "🚪 خروج از بازی":

        exit(chat_id)

        return



    # بررسی جمله

    if not check_answer(game, text):

        send_message(
            chat_id,

            "❌ اشتباه بود!\n\n"
            "دوباره تلاش کن."
        )

        return



    # زمان

    elapsed = round(
        time.time() - game["start_time"],
        2
    )


    sentence = game["sentence"]


    # محاسبه سرعت تایپ

    chars = len(sentence)

    minutes = elapsed / 60


    if minutes > 0:

        wpm = round(
            (chars / 5) / minutes
        )

    else:

        wpm = 0



    # امتیاز

    score = max(
        5,
        wpm // 5
    )


    coins = score + 5

    xp = score



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
        f"⌨️ سرعت: {wpm} کلمه در دقیقه\n"
        f"🏆 امتیاز: {score}\n\n"

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


    send_message(
        chat_id,

        "🚪 از بازی سرعت تایپ خارج شدی."
    )


    games_menu(chat_id)