from rubika import send_keypad, send_message

from games import rps

from database import add_coins

from level import give_xp

from rooms.manager import (
    get_player_room,
    can_start
)


# -----------------------------
# ساخت اتاق سنگ کاغذ قیچی
# -----------------------------

def start_rps(room):

    room.data["moves"] = {}

    for player in room.players:

        send_keypad(
            player,
            "✂️ بازی شروع شد!\n\nیکی را انتخاب کن 👇",
            [
                ["🪨 سنگ", "📄 کاغذ", "✂️ قیچی"]
            ]
        )


# -----------------------------
# انتخاب بازیکن
# -----------------------------

def choose(player, choice):

    room = get_player_room(player)

    if room is None:
        return

    if room.game != "rps":
        return

    room.data["moves"][player] = choice

    # هنوز همه انتخاب نکرده‌اند
    if len(room.data["moves"]) < len(room.players):

        send_message(
            player,
            "✅ انتخاب ثبت شد.\nمنتظر بازیکن دیگر..."
        )

        return
    
        finish(room)



def finish(room):

    players = room.players

    p1 = players[0]
    p2 = players[1]

    move1 = room.data["moves"][p1]
    move2 = room.data["moves"][p2]

    result = rps.play(move1, move2)

    if result == "draw":

        give_xp(p1, 1)
        give_xp(p2, 1)

        text = (
            f"🤝 مساوی!\n\n"
            f"👤 بازیکن اول: {move1}\n"
            f"👤 بازیکن دوم: {move2}"
        )

        send_message(p1, text)
        send_message(p2, text)

    elif result == "player1":

        add_coins(p1, 5)
        level = give_xp(p1, 2)
        give_xp(p2, 1)

        text1 = (
            f"🏆 برنده شدی!\n"
            f"👤 تو: {move1}\n"
            f"👤 حریف: {move2}\n\n"
            f"🪙 +5 سکه\n"
            f"⭐ +2 XP"
        )

        if level["level_up"]:

            text1 += (
                f"\n\n🎉 LEVEL UP!"
                f"\n⭐ Level {level['level']}"
                f"\n🪙 +{level['reward']} سکه"
            )

        text2 = (
            f"😢 باختی!\n"
            f"👤 تو: {move2}\n"
            f"👤 حریف: {move1}\n\n"
            f"⭐ +1 XP"
        )

        send_message(p1, text1)
        send_message(p2, text2)

    else:

        add_coins(p2, 5)
        level = give_xp(p2, 2)
        give_xp(p1, 1)

        text2 = (
            f"🏆 برنده شدی!\n"
            f"👤 تو: {move2}\n"
            f"👤 حریف: {move1}\n\n"
            f"🪙 +5 سکه\n"
            f"⭐ +2 XP"
        )

        if level["level_up"]:

            text2 += (
                f"\n\n🎉 LEVEL UP!"
                f"\n⭐ Level {level['level']}"
                f"\n🪙 +{level['reward']} سکه"
            )

        text1 = (
            f"😢 باختی!\n"
            f"👤 تو: {move1}\n"
            f"👤 حریف: {move2}\n\n"
            f"⭐ +1 XP"
        )

        send_message(p1, text1)
        send_message(p2, text2)

    room.data["moves"] = {}