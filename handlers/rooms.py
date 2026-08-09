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

    # نمایش Lobby به میزبان
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

    # اگر کاربر برگشت زد
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
            "❌ اتاق پیدا نشد یا ظرفیت اتاق پر است."
        )

        return True

    # ==========================================
    # اسم و فامیل → ورود به Lobby
    # ==========================================

    if room.game == "esm_famil":

        from handlers.esm_famil import show_lobby

        show_lobby(room)

        return True

    # ==========================================
    # بازی‌های 2 نفره → شروع خودکار
    # ==========================================

    for player in room.players:

        send_message(
            player,
            f"🎉 بازیکن جدید وارد شد.\n"
            f"👥 {len(room.players)} / {room.max_players}"
        )

    # ==========================================
    # دوز
    # ==========================================

    if room.game == "tictactoe":

        for player in room.players:

            send_message(
                player,
                "🔥 بازی دوز شروع شد!"
            )

        tictactoe.start(room)

    # ==========================================
    # سنگ کاغذ قیچی
    # ==========================================

    elif room.game == "rps":

        for player in room.players:

            send_message(
                player,
                "✂️ بازی سنگ کاغذ قیچی شروع شد!"
            )

        rps.start(room)

    return True

    # ==========================================
    # اسم و فامیل
    # ==========================================

    if room.game == "esm_famil":

        # اطلاع به همه بازیکنان
        for player in room.players:

            esm_lobby_menu(
                player,
                room,
                is_host=(player == room.host)
            )

        # ❗ بازی اینجا شروع نمی‌شود
        # فقط Lobby به‌روزرسانی می‌شود.

        return True

    # ==========================================
    # اطلاع به بازیکنان بازی‌های ۲ نفره
    # ==========================================

    for player in room.players:

        send_message(
            player,
            f"🎉 بازیکن دوم وارد شد.\n"
            f"👥 {len(room.players)} / {room.max_players}"
        )

    # ==========================================
    # شروع خودکار دوز
    # ==========================================

    if room.game == "tictactoe":

        for player in room.players:

            send_message(
                player,
                "🔥 بازی دوز شروع شد!"
            )

        tictactoe.start(room)

    # ==========================================
    # شروع خودکار سنگ کاغذ قیچی
    # ==========================================

    elif room.game == "rps":

        for player in room.players:

            send_message(
                player,
                "✂️ بازی سنگ کاغذ قیچی شروع شد!"
            )

        rps.start(room)

    return True


# ==========================================
# شروع بازی اسم و فامیل
# ==========================================

def start_esm_famil_room(chat_id):

    room = get_player_room(chat_id)

    if room is None:

        send_message(
            chat_id,
            "❌ داخل اتاقی نیستی."
        )

        return

    # فقط میزبان
    if chat_id != room.host:

        send_message(
            chat_id,
            "❌ فقط میزبان می‌تواند بازی را شروع کند."
        )

        return

    # حداقل بازیکن
    if len(room.players) < room.min_players:

        send_message(
            chat_id,
            f"❌ برای شروع حداقل "
            f"{room.min_players} بازیکن لازم است."
        )

        return

    # اگر بازی قبلاً شروع شده
    if room.started:

        send_message(
            chat_id,
            "⚠️ بازی قبلاً شروع شده است."
        )

        return

    # ==========================================
    # شروع واقعی بازی
    # ==========================================

    room.started = True

    for player in room.players:

        send_message(
            player,
            "🎉 بازی اسم و فامیل شروع شد!"
        )

    esm_famil.start(room)


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

    delete_room(
        room.room_id
    )

    send_message(
        chat_id,
        "🚪 از اتاق خارج شدی."
    )

    for player in other_players:

        send_message(
            player,
            "⚠️ یکی از بازیکنان از اتاق خارج شد."
        )