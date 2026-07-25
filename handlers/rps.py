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
    leave_room,
    delete_room
)

from handlers.menu import games_menu


# ==========================================
# شروع بازی
# ==========================================

def start(room):

    room.started = True

    room.data["moves"] = {}

    for player in room.players:

        send_keypad(
            player,
            "✂️ سنگ کاغذ قیچی شروع شد!\n\nیکی را انتخاب کن 👇",
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
                        "text": "🚪 خروج از بازی",
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
        "✅ انتخابت ثبت شد.\n⏳ منتظر انتخاب حریف..."
    )

    # اگر هنوز همه انتخاب نکرده‌اند
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
            f"👤 بازیکن دوم: {move2}\n\n"
            "⭐ +1 XP"
        )

        send_message(p1, text)
        send_message(p2, text)


    elif result == "player1":

        add_coins(p1, 5)

        level = give_xp(p1, 2)

        give_xp(p2, 1)

        text1 = (
            f"🏆 تو بردی!\n\n"
            f"👤 تو: {move1}\n"
            f"👤 حریف: {move2}\n\n"
            "🪙 +5 سکه\n"
            "⭐ +2 XP"
        )

        if level["level_up"]:

            text1 += (
                f"\n\n🎉 LEVEL UP!"
                f"\n⭐ Level {level['level']}"
                f"\n🪙 +{level['reward']} سکه"
            )

        text2 = (
            f"😢 باختی!\n\n"
            f"👤 تو: {move2}\n"
            f"👤 حریف: {move1}\n\n"
            "⭐ +1 XP"
        )

        send_message(p1, text1)
        send_message(p2, text2)


    else:

        add_coins(p2, 5)

        level = give_xp(p2, 2)

        give_xp(p1, 1)

        text2 = (
            f"🏆 تو بردی!\n\n"
            f"👤 تو: {move2}\n"
            f"👤 حریف: {move1}\n\n"
            "🪙 +5 سکه\n"
            "⭐ +2 XP"
        )

        if level["level_up"]:

            text2 += (
                f"\n\n🎉 LEVEL UP!"
                f"\n⭐ Level {level['level']}"
                f"\n🪙 +{level['reward']} سکه"
            )

        text1 = (
            f"😢 باختی!\n\n"
            f"👤 تو: {move1}\n"
            f"👤 حریف: {move2}\n\n"
            "⭐ +1 XP"
        )

        send_message(p1, text1)
        send_message(p2, text2)

    room.started = False

    room.data["moves"] = {}

    delete_room(
        room.room_id
    )
# ==========================================
# مدیریت کلیک‌ها
# ==========================================

def handle(room, player, data):

    button_id = data.get("button_id")
    print("RPS BUTTON:", button_id)

    if not button_id:
        return

    # -------------------------
    # خروج از بازی
    # -------------------------

    if button_id == "exit" or button_id == "🚪 خروج از بازی":

        other_players = [
            p for p in room.players
            if p != player
        ]

        leave_room(player)

        remove_keypad(
            player,
            "🚪 از بازی خارج شدی."
        )

        games_menu(player)

        for p in other_players:

            send_message(
                p,
                "⚠️ حریف از بازی خارج شد."
            )

            remove_keypad(
                p,
                "🏁 بازی پایان یافت."
            )

            games_menu(p)

            leave_room(p)

        return

    # -------------------------
    # انتخاب‌ها
    # -------------------------

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