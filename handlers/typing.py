import time

from rubika import (
    send_keypad,
    send_message
)

from database import (
    add_coins,
    update_typing_stats
)

from level import give_xp


games = {}

waiting_level = set()



# ==========================================
# شروع انتخاب سطح
# ==========================================

def start(chat_id):

    waiting_level.add(chat_id)


    send_keypad(
        chat_id,

        "⌨️ سرعت تایپ\n\n"
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
# شروع بازی
# ==========================================

def select_level(chat_id, level):

    from games.typing import create_game


    game = create_game(level)


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



    # محاسبه زمان

    elapsed = round(
        time.time() - game["start_time"],
        2
    )


    sentence = game["sentence"]


    chars = len(sentence)


    minutes = elapsed / 60



    if minutes > 0:

        wpm = round(
            (chars / 5) / minutes
        )

    else:

        wpm = 0



    # جایزه سطح

    level_bonus = {

        "easy": 1,

        "medium": 3,

        "hard": 5

    }


    bonus = level_bonus.get(
        game.get("level"),
        1
    )



    coins = 5 + bonus + (wpm // 10)

    xp = 3 + bonus



    add_coins(
        chat_id,
        coins
    )


    give_xp(
        chat_id,
        xp
    )


    # ذخیره رکورد

    update_typing_stats(
        chat_id,
        elapsed,
        wpm
    )



    send_message(
        chat_id,

        "🎉 آفرین!\n\n"

        f"⭐ سطح: {game.get('level')}\n"
        f"⏱ زمان: {elapsed} ثانیه\n"
        f"⌨️ سرعت: {wpm} WPM\n\n"

        f"🪙 +{coins} سکه\n"
        f"⭐ +{xp} XP\n\n"

        "🏆 رکوردت ذخیره شد!"
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
        "🚪 از بازی سرعت تایپ خارج شدی."
    )


    games_menu(chat_id)