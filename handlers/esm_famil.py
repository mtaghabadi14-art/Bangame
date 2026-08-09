import random

from rubika import send_message

from rooms.manager import (
    delete_room,
    start_game
)

from handlers.esm_buttons import (
    show_categories
)

from handlers.esm_answers import (
    choose_category,
    save_answer,
    ready
)


# ==========================================
# بازی‌های فعال
# ==========================================

games = {}


# ==========================================
# دسته‌بندی‌ها
# ==========================================

categories = [
    "👤 اسم",
    "🏠 فامیل",
    "🍎 میوه",
    "🍔 غذا",
    "🎨 رنگ",
    "📦 اشیا",
    "🐶 حیوان",
    "🌍 شهر یا کشور",
    "🖐 اعضای بدن",
    "🎬 فیلم یا سریال"
]


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
            is_host=(player == room.host)
        )


# ==========================================
# شروع بازی توسط میزبان
# ==========================================

def start_by_host(room, player):

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

    start(room)

    return True


# ==========================================
# شروع بازی
# ==========================================

def start(room):

    if room.started:
        return

    if len(room.players) < room.min_players:

        return

    start_game(room)

    letter = random.choice(letters)

    room.data["letter"] = letter
    room.data["answers"] = {}
    room.data["ready"] = []
    room.data["waiting"] = {}

    for player in room.players:

        room.data["answers"][player] = {}

    for player in room.players:

        send_message(
            player,
            f"✍️ بازی اسم و فامیل شروع شد!\n\n"
            f"🔤 حرف انتخاب شده: {letter}\n\n"
            f"یکی از دسته‌ها را انتخاب کن."
        )

        show_categories(player)


# ==========================================
# انتخاب دسته
# ==========================================

def select_category(room, player, category):

    if category not in categories:

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

def add_answer(room, player, text):

    return save_answer(
        room,
        player,
        text
    )


# ==========================================
# آماده شدن
# ==========================================

def player_ready(room, player):

    ready(
        room,
        player
    )


# ==========================================
# اطلاعات بازی
# ==========================================

def get_game_data(room):

    return {

        "letter": room.data.get("letter"),

        "answers": room.data.get(
            "answers",
            {}
        ),

        "ready": room.data.get(
            "ready",
            []
        )

    }


# ==========================================
# مدیریت پیام بازیکن
# ==========================================

def handle(room, player, text):

    # خروج از بازی

    if text == "🚪 خروج از بازی":

        exit_game(
            room,
            player
        )

        return True

    # خروج از اتاق

    if text == "🚪 خروج از اتاق":

        exit_game(
            room,
            player
        )

        return True

    # آماده شدن

    if text == "✅ آماده‌ام":

        player_ready(
            room,
            player
        )

        return True

    # انتخاب دسته

    if text in categories:

        select_category(
            room,
            player,
            text
        )

        return True

    # ذخیره جواب

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

def get_player_answers(room, player):

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

def exit_game(room, player):

    from rooms.manager import leave_room
    from handlers.menu import room_menu

    leave_room(player)

    send_message(
        player,
        "🚪 از بازی اسم و فامیل خارج شدی."
    )

    room_menu(player)


# ==========================================
# پایان دور
# ==========================================

def finish_round(room):

    from handlers.menu import room_menu

    for player in room.players:

        send_message(
            player,
            "🎉 دور بازی تمام شد!\n"
            "امتیازدهی به‌زودی اضافه می‌شود."
        )

    delete_room(
        room.room_id
    )

    for player in room.players:

        room_menu(player)


# ==========================================
# ریست بازی
# ==========================================

def reset_game(room):

    room.data["answers"] = {}
    room.data["ready"] = []
    room.data["waiting"] = {}

    for player in room.players:

        room.data["answers"][player] = {}