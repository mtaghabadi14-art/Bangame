from rubika import send_message, send_keypad
from handlers.rooms import open_room_menu

from handlers.menu import (
    create_room_menu,
    room_menu,
    esm_lobby_menu
)

from handlers import tictactoe
from handlers import rps
from handlers import esm_famil
from handlers import puzzle_online

from handlers.memory_online_buttons import (
    memory_lobby_menu
)

from rooms.manager import (
    create_room,
    join_room,
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

    room_menu(
        chat_id
    )


def open_create_room(chat_id):

    create_room_menu(
        chat_id
    )


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
        f"📨 این کد را برای دوستت بفرست.\n"
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
        f"📨 این کد را برای دوستت بفرست.\n"
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
# ساخت اتاق حافظه آنلاین
# ==========================================

def create_memory_online_room(chat_id):

    room = create_room(
        game="memory_online",
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

    memory_lobby_menu(
        chat_id,
        room,
        is_host=True
    )


# ==========================================
# ساخت اتاق UNO
# ==========================================

def create_uno_room(chat_id):

    room = create_room(
        game="uno",
        host=chat_id,
        min_players=2,
        max_players=4
    )

    if room is None:

        send_message(
            chat_id,
            "❌ ابتدا از اتاق فعلی خارج شو."
        )

        return

    send_message(
        chat_id,
        f"🃏 اتاق UNO ساخته شد! 🔥\n\n"
        f"🔑 کد اتاق: {room.room_id}\n"
        f"👥 بازیکنان: 1 / 4\n\n"
        f"📨 کد اتاق را برای دوستانت بفرست.\n"
        f"⏳ منتظر بازیکنان..."
    )


# ==========================================
# ساخت اتاق پازل آنلاین
# ==========================================

def create_puzzle_online_room(chat_id):

    room = create_room(
        game="puzzle_online",
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

    puzzle_online.show_lobby(
        room
    )


# ==========================================
# درخواست ورود به اتاق
# ==========================================

def request_join(chat_id):

    waiting_for_room_code.add(
        chat_id
    )

    send_message(
        chat_id,
        "🔑 کد اتاق را ارسال کن."
    )


# ==========================================
# دریافت کد اتاق
# ==========================================

def receive_room_code(
    chat_id,
    code
):

    # --------------------------------------
    # برگشت
    # --------------------------------------

    if code in (
        "⬅️ برگشت",
        "⬅️ برگشت به منوی اصلی",
        "⬅️ برگشت به اتاق بازی"
    ):

        waiting_for_room_code.discard(
            chat_id
        )

        return False

    # --------------------------------------
    # کاربر منتظر کد نیست
    # --------------------------------------

    if chat_id not in waiting_for_room_code:

        return False

    waiting_for_room_code.remove(
        chat_id
    )

    # --------------------------------------
    # ورود به اتاق
    # --------------------------------------

    room = join_room(
        code.strip().upper(),
        chat_id
    )

    if room is None:

        send_message(
            chat_id,
            "❌ اتاق پیدا نشد یا ظرفیت اتاق پر است."
        )

        return True

    # ======================================
    # UNO
    # ======================================

    if room.game == "uno":

        from handlers.uno import show_lobby

        show_lobby(
            room
        )

        return True

    # ======================================
    # پازل چندنفره
    # ======================================

    if room.game == "puzzle_online":

        puzzle_online.show_lobby(
            room
        )

        return True

    # ======================================
    # اسم و فامیل
    # ======================================

    if room.game == "esm_famil":

        from handlers.esm_famil import show_lobby

        show_lobby(
            room
        )

        return True

    # ======================================
    # حافظه آنلاین
    # ======================================

    if room.game == "memory_online":

        for player in room.players:

            memory_lobby_menu(
                player,
                room,
                is_host=(
                    player == room.host
                )
            )

        return True

    # ======================================
    # اطلاع به بازیکنان
    # ======================================

    for player in room.players:

        send_message(
            player,
            f"🎉 بازیکن جدید وارد شد.\n"
            f"👥 {len(room.players)} / "
            f"{room.max_players}"
        )

    # ======================================
    # دوز
    # ======================================

    if room.game == "tictactoe":

        for player in room.players:

            send_message(
                player,
                "🔥 بازی دوز شروع شد!"
            )

        tictactoe.start(
            room
        )

        return True

    # ======================================
    # سنگ کاغذ قیچی
    # ======================================

    if room.game == "rps":

        for player in room.players:

            send_message(
                player,
                "✂️ بازی سنگ کاغذ قیچی شروع شد!"
            )

        rps.start(
            room
        )

        return True

    return True


# ==========================================
# شروع بازی اسم و فامیل
# ==========================================

def start_esm_famil_room(chat_id):

    room = get_player_room(
        chat_id
    )

    if room is None:

        send_message(
            chat_id,
            "❌ داخل اتاقی نیستی."
        )

        return

    if chat_id != room.host:

        send_message(
            chat_id,
            "❌ فقط میزبان می‌تواند بازی را شروع کند."
        )

        return

    if len(room.players) < room.min_players:

        send_message(
            chat_id,
            f"❌ برای شروع حداقل "
            f"{room.min_players} بازیکن لازم است."
        )

        return

    if room.started:

        send_message(
            chat_id,
            "⚠️ بازی قبلاً شروع شده است."
        )

        return

    room.started = True

    for player in room.players:

        send_message(
            player,
            "🎉 بازی اسم و فامیل شروع شد!"
        )

    esm_famil.start(
        room
    )


# ==========================================
# خروج از اتاق
# ==========================================

def exit_room(chat_id):

    room = get_player_room(
        chat_id
    )

    if room is None:

        send_message(
            chat_id,
            "❌ داخل هیچ اتاقی نیستی."
        )

        return

    other_players = [
        player
        for player in room.players
        if player != chat_id
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