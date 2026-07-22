from rubika import (
    send_keypad,
    send_message,
    remove_keypad
)

from games import rps

from database import add_coins

from level import give_xp

from rooms.manager import (
    get_player_room,
    leave_room
)

from handlers.menu import main_menu


# ==========================================
# شروع بازی
# ==========================================

def start(room):

    room.started = True

    room.data["moves"] = {}

    for player in room.players:

        send_keypad(
            player,
            "✂️ سنگ کاغذ قیچی شروع شد!\n\nانتخاب کن 👇",
            [
                [
                    {
                        "text": "🪨 سنگ",
                        "id": "rock"
                    },
                    {
                        "text": "📄 کاغذ",
                        "id": "paper"
                    },
                    {
                        "text": "✂️ قیچی",
                        "id": "scissors"
                    }
                ],
                [
                    {
                        "text": "🚪 خروج",
                        "id": "exit"
                    }
                ]
            ]
        )


# ==========================================
# انتخاب بازیکن
# ==========================================

def choose(player, choice):

    room = get_player_room(player)

    if room is None:
        return

    if room.game != "rps":
        return


    room.data["moves"][player] = choice


    send_message(
        player,
        "✅ انتخابت ثبت شد.\nمنتظر حریف باش..."
    )


    # هنوز نفر دوم انتخاب نکرده
    if len(room.data["moves"]) < len(room.players):

        return


    finish(room)



# ==========================================
# پایان بازی
# ==========================================

def finish(room):

    players = room.players

    p1 = players[0]
    p2 = players[1]


    move1 = room.data["moves"][p1]
    move2 = room.data["moves"][p2]


    result = rps.play(
        move1,
        move2
    )


    if result == "draw":

        give_xp(p1, 1)
        give_xp(p2, 1)

        text = (
            "🤝 مساوی شد!\n\n"
            f"👤 بازیکن اول: {move1}\n"
            f"👤 بازیکن دوم: {move2}"
        )


        send_message(p1, text)
        send_message(p2, text)



    elif result == "player1":

        add_coins(p1, 5)

        give_xp(p1, 2)
        give_xp(p2, 1)


        send_message(
            p1,
            f"🏆 تو بردی!\n\n"
            f"👤 تو: {move1}\n"
            f"👤 حریف: {move2}\n\n"
            "🪙 +5 سکه\n"
            "⭐ +2 XP"
        )


        send_message(
            p2,
            f"😢 باختی!\n\n"
            f"👤 تو: {move2}\n"
            f"👤 حریف: {move1}\n\n"
            "⭐ +1 XP"
        )



    else:

        add_coins(p2, 5)

        give_xp(p2, 2)
        give_xp(p1, 1)


        send_message(
            p2,
            f"🏆 تو بردی!\n\n"
            f"👤 تو: {move2}\n"
            f"👤 حریف: {move1}\n\n"
            "🪙 +5 سکه\n"
            "⭐ +2 XP"
        )


        send_message(
            p1,
            f"😢 باختی!\n\n"
            f"👤 تو: {move1}\n"
            f"👤 حریف: {move2}\n\n"
            "⭐ +1 XP"
        )


    room.started = False

    room.data["moves"] = {}



# ==========================================
# مدیریت کلیک‌ها
# ==========================================

def handle(room, player, data):

    button_id = data.get("button_id")


    if not button_id:
        return


    # خروج

    if button_id == "exit":

        leave_room(player)

        remove_keypad(
            player,
            "🚪 از بازی خارج شدی."
        )

        main_menu(player)

        return



    # انتخاب‌ها

    choices = {
        "rock": "سنگ",
        "paper": "کاغذ",
        "scissors": "قیچی"
    }


    if button_id in choices:

        choose(
            player,
            choices[button_id]
        )