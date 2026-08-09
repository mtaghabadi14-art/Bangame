from rubika import send_message

from handlers.menu import (
    create_room_menu,
    room_menu,
    esm_lobby_menu
)

from handlers import tictactoe
from handlers import rps
from handlers import esm_famil

from rooms.manager import (
    create_room,
    join_room,
    leave_room,
    get_player_room,
    delete_room
)


# ==========================================
# انتظار کد اتاق
# ==========================================

waiting_for_room_code = set()


# ==========================================
# منوی اتاق
# ==========================================

def open_room_menu(chat_id):

    room_menu(chat_id)


def open_create_room(chat_id):

    create_room_menu(chat_id)


# ==========================================
# ساخت اتاق سنگ کاغذ قیچی
# ==========================================

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
        f"✅ اتاق سنگ کاغذ قیچی ساخته شد.\n\n"
        f"🔑 کد اتاق: {room.room_id}\n"
        f"👥 1 / 2 بازیکن\n\n"
        f"⏳ منتظر بازیکن دوم..."
    )


# ==========================================
# ساخت اتاق دوز
# ==========================================

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


# ==========================================
# ساخت اتاق اسم و فامیل
# ==========================================

def create_esm_famil_room(chat_id):

    room = create_room(
        game="esm_famil",
        host=chat_id,
        min_players=2,
        max_players=8
    )

    if room is None:

        send_message(
            chat_id,
            "❌ ابتدا از اتاق فعلی خارج شو."
        )

        return

    esm_lobby_menu(
        chat_id,
        room,
        is_host=True
    )


# ==========================================
# درخواست ورود به اتاق
# ==========================================

def request_join(chat_id):

    waiting_for_room_code.add(chat_id)

    send_message(
        chat_id,
        "🔑 کد اتاق را ارسال کن."
    )


# ==========================================
# دریافت کد اتاق
# ==========================================

def receive_room_code(chat_id, code):

    if code in [
        "⬅️ برگشت",
        "⬅️ برگشت به منوی اصلی",
        "⬅️ برگشت به اتاق بازی"
    ]:

        waiting_for_room_code.discard(chat_id)

        return False

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
            "❌ اتاق پیدا نشد، پر است یا بازی شروع شده."
        )

        return True

    # ======================================
    # اسم و فامیل
    # ======================================

    if room.game == "esm_famil":

        # فقط Lobby را برای همه به‌روزرسانی کن
        # بازی هنوز شروع نمی‌شود.

        for player in room.players:

            esm_lobby_menu(
                player,
                room,
                is_host=(player == room.host)
            )

        return True

    # ======================================
    # اطلاع به بازیکنان
    # ======================================

    for player in room.players:

        send_message(
            player,
            f"🎉 بازیکن جدید وارد شد.\n"
            f"👥 {len(room.players)} / {room.max_players}"
        )

    # ======================================
    # شروع دوز
    # ======================================

    if room.game == "tictactoe":

        for player in room.players:

            send_message(
                player,
                "🔥 بازی دوز شروع شد!"
            )

        tictactoe.start(room)

    # ======================================
    # شروع سنگ کاغذ قیچی
    # ======================================

    elif room.game == "rps":

        for player in room.players:

            send_message(
                player,
                "✂️ بازی سنگ کاغذ قیچی شروع شد!"
            )

        rps.start(room)

    return True


# ==========================================
# خروج از اتاق
# ==========================================

def exit_room(chat_id):

    room = get_player_room(chat_id)

    if room is None:

        send_message(
            chat_id,
            "❌ داخل هیچ اتاقی نیستی."
        )

        return

    other_players = [
        p for p in room.players
        if p != chat_id
    ]

    # اگر اسم و فامیل هنوز شروع نشده
    # Lobby را بعد از خروج به‌روزرسانی می‌کنیم.

    was_esm_lobby = (
        room.game == "esm_famil"
        and not room.started
    )

    leave_room(chat_id)

    send_message(
        chat_id,
        "🚪 از اتاق خارج شدی."
    )

    # اگر اتاق هنوز وجود دارد
    updated_room = get_player_room(
        other_players[0]
    ) if other_players else None

    if was_esm_lobby and updated_room:

        for player in updated_room.players:

            esm_lobby_menu(
                player,
                updated_room,
                is_host=(player == updated_room.host)
            )

    else:

        for player in other_players:

            send_message(
                player,
                "⚠️ یکی از بازیکنان از اتاق خارج شد."
            )