from rubika import (
    send_keypad,
    remove_keypad
)

from handlers.menu import games_menu

from games import dice

from database import add_coins

from level import give_xp


# ==========================================
# شروع بازی
# ==========================================

def start(chat_id):

    send_keypad(
        chat_id,
        "🎲 برای انداختن تاس روی دکمه زیر بزن.",
        [
            ["🎲 ریختن تاس"],
            ["🚪 خروج از بازی"]
        ]
    )


# ==========================================
# ریختن تاس
# ==========================================

def roll(chat_id):

    player = dice.roll()
    bot = dice.roll()

    message = (
        f"🎲 تاس تو: {player}\n"
        f"🤖 تاس ربات: {bot}\n\n"
    )

    if player > bot:

        add_coins(chat_id, 10)

        level = give_xp(chat_id, 3)

        message += (
            "🏆 برنده شدی!\n"
            "🪙 +10 سکه\n"
            "⭐ +3 XP"
        )

        if level["level_up"]:

            message += (
                f"\n\n🎉 LEVEL UP!"
                f"\n⭐ Level {level['level']}"
                f"\n🪙 +{level['reward']} سکه"
            )

    elif player < bot:

        give_xp(chat_id, 1)

        message += (
            "😢 ربات برنده شد.\n"
            "⭐ +1 XP"
        )

    else:

        give_xp(chat_id, 1)

        message += (
            "🤝 مساوی شد.\n"
            "⭐ +1 XP"
        )

    send_keypad(
        chat_id,
        message,
        [
            ["🎲 ریختن تاس"],
            ["🚪 خروج از بازی"]
        ]
    )


# ==========================================
# خروج از بازی
# ==========================================

def exit(chat_id):

    remove_keypad(
        chat_id,
        "🚪 از بازی خارج شد."
    )

    games_menu(chat_id)