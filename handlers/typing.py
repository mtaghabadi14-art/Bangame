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
# شروع بازی
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
# ساخت بازی
# ==========================================

def select_level(chat_id, level):

    from games.typing import create_game

    game = create_game(level)

    game["level"] = level
    game["start_time"] = time.time()

    games[chat_id] = game

    send_keypad(
        chat_id,
        "⌨️ سرعت تایپ\n\n"
        "جمله زیر را دقیقا تایپ کن:\n\n"
        f"📝 {game['sentence']}",
        [
            [
                "🚪 خروج از بازی"
            ]
        ]
    )
    # ==========================================
# بررسی پیام
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


    # ------------------------------
    # خروج
    # ------------------------------

    if text == "🚪 خروج از بازی":

        exit(chat_id)

        return


    from games.typing import check as check_answer

    game = games[chat_id]


    # ------------------------------
    # جواب اشتباه
    # ------------------------------

    if not check_answer(game, text):

        send_message(
            chat_id,
            "❌ جمله اشتباه است.\n"
            "دوباره تلاش کن."
        )

        return


    # ------------------------------
    # محاسبه زمان
    # ------------------------------

    elapsed = round(
        time.time() - game["start_time"],
        2
    )

    chars = len(game["sentence"])

    minutes = elapsed / 60

    if minutes > 0:

        wpm = round(
            (chars / 5) / minutes
        )

    else:

        wpm = 0


    # ------------------------------
    # پاداش
    # ------------------------------

    bonus = {

        "easy": 1,
        "medium": 2,
        "hard": 4

    }.get(
        game["level"],
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


    # ------------------------------
    # ذخیره آمار
    # ------------------------------

    records = update_typing_stats(
        chat_id,
        elapsed,
        wpm
    )


    record_text = ""

    if records["new_time_record"]:

        record_text += "\n🏆 رکورد جدید زمان!"

    if records["new_wpm_record"]:

        record_text += "\n⚡ رکورد جدید سرعت!"


    send_message(
        chat_id,
        "🎉 آفرین!\n\n"
        f"⭐ سطح: {game['level']}\n"
        f"⏱ زمان: {elapsed} ثانیه\n"
        f"⌨️ سرعت: {wpm} WPM\n\n"
        f"🪙 +{coins} سکه\n"
        f"⭐ +{xp} XP"
        f"{record_text}"
    )

    games.pop(
        chat_id,
        None
    )
    # ==========================================
# خروج از بازی
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