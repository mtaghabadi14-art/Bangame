import random

from rubika import send_message

from rooms.manager import (
    start_game
)

from handlers.esm_buttons import (
    show_categories,
    CATEGORIES
)

from handlers.esm_answers import (
    choose_category,
    save_answer,
    ready,
    cancel_answer
)


# ==========================================
# بازی‌های فعال
# ==========================================

games = {}


# ==========================================
# حروف
# ==========================================

letters = [
    "ا",
    "ب",
    "پ",
    "ت",
    "ج",
    "چ",
    "ح",
    "خ",
    "د",
    "ر",
    "ز",
    "س",
    "ش",
    "ص",
    "ط",
    "ع",
    "غ",
    "ف",
    "ق",
    "ک",
    "گ",
    "ل",
    "م",
    "ن",
    "و",
    "ه",
    "ی"
]


# ==========================================
# نمایش Lobby
# ==========================================

def show_lobby(room):

    from handlers.menu import esm_lobby_menu

    for player in room.players:

        esm_lobby_menu(
            player,
            room,
            is_host=(
                player == room.host
            )
        )


# ==========================================
# شروع بازی توسط میزبان
# ==========================================

def start_by_host(
    room,
    player
):

    if player != room.host:

        send_message(
            player,
            "❌ فقط میزبان می‌تواند بازی را شروع کند."
        )

        return False

    if room.started:

        send_message(
            player,
            "❌ بازی قبلاً شروع شده است."
        )

        return False

    if len(room.players) < room.min_players:

        send_message(
            player,
            f"❌ حداقل {room.min_players} بازیکن لازم است."
        )

        return False

    start(
        room
    )

    return True


# ==========================================
# شروع بازی
# ==========================================

def start(room):

    if room.started:
        return

    if len(room.players) < room.min_players:
        return

    # شروع اتاق
    start_game(
        room
    )

    # انتخاب حرف
    letter = random.choice(
        letters
    )

    # ======================================
    # ساخت اطلاعات بازی
    # ======================================

    room.data["letter"] = letter

    room.data["answers"] = {}

    room.data["ready"] = []

    room.data["waiting"] = {}

    # برای هر بازیکن جواب خالی
    for player in room.players:

        room.data["answers"][player] = {}

    # ======================================
    # ارسال بازی به بازیکنان
    # ======================================

    for player in room.players:

        send_message(
            player,
            (
                "✍️ بازی اسم و فامیل شروع شد!\n\n"
                f"🔤 حرف انتخاب شده: {letter}\n\n"
                "📚 برای هر دسته جواب خودت را وارد کن.\n"
                "در پایان روی «✅ آماده‌ام» بزن."
            )
        )

        show_categories(
            player
        )


# ==========================================
# انتخاب دسته
# ==========================================

def select_category(
    room,
    player,
    category
):

    if category not in CATEGORIES:

        return False

    choose_category(
        room,
        player,
        category
    )

    return True


# ==========================================
# ذخیره جواب
# ==========================================

def add_answer(
    room,
    player,
    text
):

    return save_answer(
        room,
        player,
        text
    )


# ==========================================
# آماده شدن
# ==========================================

def player_ready(
    room,
    player
):

    ready(
        room,
        player
    )


# ==========================================
# اطلاعات بازی
# ==========================================

def get_game_data(room):

    return {

        "letter": room.data.get(
            "letter"
        ),

        "answers": room.data.get(
            "answers",
            {}
        ),

        "ready": room.data.get(
            "ready",
            []
        ),

        "waiting": room.data.get(
            "waiting",
            {}
        )

    }


# ==========================================
# مدیریت پیام بازیکن
# ==========================================

def handle(
    room,
    player,
    text
):

    # ======================================
    # شروع بازی
    # ======================================

    if text == "▶️ شروع بازی":

        start_by_host(
            room,
            player
        )

        return True

    # ======================================
    # خروج از بازی
    # ======================================

    if text == "🚪 خروج از بازی":

        exit_game(
            room,
            player
        )

        return True

    # ======================================
    # خروج از اتاق
    # ======================================

    if text == "🚪 خروج از اتاق":

        exit_game(
            room,
            player
        )

        return True

    # ======================================
    # انصراف از نوشتن جواب
    # ======================================

    if text == "⬅️ انصراف":

        cancel_answer(
            room,
            player
        )

        return True

    # ======================================
    # آماده شدن
    # ======================================

    if text == "✅ آماده‌ام":

        player_ready(
            room,
            player
        )

        return True

    # ======================================
    # انتخاب دسته
    # ======================================

    if text in CATEGORIES:

        select_category(
            room,
            player,
            text
        )

        return True

    # ======================================
    # ذخیره جواب
    # ======================================

    if player in room.data.get(
        "waiting",
        {}
    ):

        add_answer(
            room,
            player,
            text
        )

        return True

    return False


# ==========================================
# گرفتن جواب‌های بازیکن
# ==========================================

def get_player_answers(
    room,
    player
):

    return room.data.get(
        "answers",
        {}
    ).get(
        player,
        {}
    )


# ==========================================
# پاک کردن جواب‌ها
# ==========================================

def clear_answers(room):

    room.data["answers"] = {}

    for player in room.players:

        room.data["answers"][player] = {}


# ==========================================
# خروج از بازی
# ==========================================

def exit_game(
    room,
    player
):

    from rooms.manager import leave_room
    from handlers.menu import room_menu

    # حذف حالت انتظار
    room.data.get(
        "waiting",
        {}
    ).pop(
        player,
        None
    )

    # خارج کردن بازیکن
    leave_room(
        player
    )

    send_message(
        player,
        "🚪 از بازی اسم و فامیل خارج شدی."
    )

    room_menu(
        player
    )


# ==========================================
# پایان دور
# ==========================================

def finish_round(room):

    from handlers.menu import room_menu
    from rooms.manager import delete_room

    # پیام پایان
    for player in room.players:

        send_message(
            player,
            (
                "🎉 دور بازی تمام شد!\n\n"
                "📊 نتیجه در حال نمایش است..."
            )
        )

    # حذف اتاق
    delete_room(
        room.room_id
    )

    # منوی اتاق
    for player in room.players:

        room_menu(
            player
        )


# ==========================================
# ریست بازی
# ==========================================

def reset_game(room):

    room.data["answers"] = {}

    room.data["ready"] = []

    room.data["waiting"] = {}

    for player in room.players:

        room.data["answers"][player] = {}