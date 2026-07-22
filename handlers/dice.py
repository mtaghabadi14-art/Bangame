from rubika import send_keypad

from games import dice

from database import add_coins

from level import give_xp


def keypad():

    return [
        ["🎲 ریختن تاس"],
        ["🚪 خروج"]
    ]



def start(chat_id):

    send_keypad(
        chat_id,
        "🎲 برای انداختن تاس روی دکمه زیر بزن.",
        keypad()
    )



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
        keypad()
    )
    