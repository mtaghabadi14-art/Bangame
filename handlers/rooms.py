from rubika import send_message

from handlers.menu import (
    create_room_menu,
    room_menu
)

from handlers import tictactoe

from rooms.manager import (
    create_room,
    join_room,
    leave_room,
    get_player_room
)


waiting_for_room_code = set()


# -----------------------------
# منوی اتاق
# -----------------------------

def open_room_menu(chat_id):

    room_menu(chat_id)



def open_create_room(chat_id):

    create_room_menu(chat_id)



# -----------------------------
# ساخت اتاق سنگ کاغذ قیچی
# -----------------------------

def create_rps_room(chat_id):

    room = create_room(
        game="rps",
        host=chat_id,
        min_players=2,
        max_players=2
    )


    if room is None:

        send_message(
            chat_id,
            "❌ ابتدا از اتاق فعلی خارج شو."
        )

        return


    send_message(
        chat_id,
        f"✅ اتاق ساخته شد.\n\n"
        f"🔑 کد اتاق: {room.room_id}\n"
        f"👥 1 / 2 بازیکن\n\n"
        f"⏳ منتظر بازیکن دوم..."
    )



# -----------------------------
# ساخت اتاق دوز
# -----------------------------

def create_tictactoe_room(chat_id):

    room = create_room(
        game="tictactoe",
        host=chat_id,
        min_players=2,
        max_players=2
    )


    if room is None:

        send_message(
            chat_id,
            "❌ ابتدا از اتاق فعلی خارج شو."
        )

        return


    send_message(
        chat_id,
        f"⭕ اتاق دوز ساخته شد.\n\n"
        f"🔑 کد اتاق: {room.room_id}\n"
        f"👥 1 / 2 بازیکن\n\n"
        f"⏳ منتظر بازیکن دوم..."
    )



# -----------------------------
# درخواست ورود به اتاق
# -----------------------------

def request_join(chat_id):

    waiting_for_room_code.add(chat_id)

    send_message(
        chat_id,
        "🔑 کد اتاق را ارسال کن."
    )



# -----------------------------
# دریافت کد اتاق
# -----------------------------

def receive_room_code(chat_id, code):

    if chat_id not in waiting_for_room_code:

        return False


    waiting_for_room_code.remove(chat_id)


    room = join_room(
        code,
        chat_id
    )


    if room is None:

        send_message(
            chat_id,
            "❌ اتاق پیدا نشد."
        )

        return True



    send_message(
        room.host,
        "🎉 بازیکن دوم وارد اتاق شد."
    )


    send_message(
        chat_id,
        "✅ وارد اتاق شدی."
    )


    # شروع بازی دوز
    if room.game == "tictactoe":

        tictactoe.start(room)


    return True



# -----------------------------
# خروج از اتاق
# -----------------------------

def exit_room(chat_id):

    leave_room(chat_id)


    send_message(
        chat_id,
        "🚪 از اتاق خارج شدی."
    )