from rubika import (
    send_message,
    send_keypad,
    remove_keypad
)

from handlers.menu import games_menu

from games import guess

from database import add_coins

from level import give_xp


# ==========================================
# شروع بازی
# ==========================================

def start(states, chat_id):

    number = guess.create_game()

    states[chat_id] = {
        "game": "guess",
        "number": number,
        "tries": 0
    }

    send_keypad(
        chat_id,
        "🔢 یک عدد بین 1 تا 100 حدس بزن.",
        [
            ["🚪 خروج از بازی"]
        ]
    )


# ==========================================
# خروج از بازی
# ==========================================

def exit(states, chat_id):

    states.pop(chat_id, None)

    remove_keypad(
        chat_id,
        "🚪 از بازی خارج شدی."
    )

    games_menu(chat_id)


# ==========================================
# بررسی حدس
# ==========================================

def check(states, chat_id, text):

    if not text.isdigit():

        send_message(
            chat_id,
            "❌ فقط عدد وارد کن."
        )

        return

    states[chat_id]["tries"] += 1

    value = int(text)

    result = guess.check(
        states[chat_id]["number"],
        value
    )

    if result == "higher":

        send_message(
            chat_id,
            "⬆️ عدد من بزرگ‌تره."
        )

        return

    if result == "lower":

        send_message(
            chat_id,
            "⬇️ عدد من کوچک‌تره."
        )

        return

    tries = states[chat_id]["tries"]

    if tries == 1:
        coins = 100
        xp = 20
    elif tries == 2:
        coins = 80
        xp = 18
    elif tries == 3:
        coins = 60
        xp = 15
    elif tries <= 5:
        coins = 40
        xp = 10
    elif tries <= 8:
        coins = 25
        xp = 6
    else:
        coins = 10
        xp = 3

    add_coins(chat_id, coins)

    level = give_xp(chat_id, xp)

    states.pop(chat_id)

    message = (
        f"🎉 درست حدس زدی!\n"
        f"🪙 +{coins} سکه\n"
        f"⭐ +{xp} XP"
    )

    if level["level_up"]:

        message += (
            f"\n\n🎉 LEVEL UP!"
            f"\n⭐ Level {level['level']}"
            f"\n🪙 +{level['reward']} سکه"
        )

    remove_keypad(
        chat_id,
        message
    )

    games_menu(chat_id)