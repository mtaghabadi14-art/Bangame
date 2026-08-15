import random

from rubika import (
    send_message,
    edit_message_text
)

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
    ready,
    cancel_answer
)

from database import get_nickname


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
# شروع توسط میزبان
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

    start_game(
        room
    )

    letter = random.choice(
        letters
    )

    room.data["letter"] = letter
    room.data["answers"] = {}
    room.data["ready"] = []
    room.data["waiting"] = {}
    room.data["status_messages"] = {}

    for player in room.players:

        room.data["answers"][player] = {}

    for player in room.players:

        result = send_message(
            player,
            (
                "✍️ بازی اسم و فامیل شروع شد!\n\n"
                f"🔤 حرف انتخاب شده: {letter}\n\n"
                "📚 یکی از دسته‌ها را انتخاب کن."
            )
        )

        message_id = (
            result
            .get("data", {})
            .get("message_id")
        )

        room.data["status_messages"][player] = message_id

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

    if category not in categories:

        return False

    return choose_category(
        room,
        player,
        category
    )


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
        )
    }

# ==========================================
# مدیریت پیام
# ==========================================

def handle(
    room,
    player,
    text
):

    # --------------------------------------
    # شروع بازی
    # --------------------------------------

    if text == "▶️ شروع بازی":

        start_by_host(
            room,
            player
        )

        return True

    # --------------------------------------
    # خروج از بازی / اتاق
    # --------------------------------------

    if text in (
        "🚪 خروج از بازی",
        "🚪 خروج از اتاق"
    ):

        exit_game(
            room,
            player
        )

        return True

    # ==========================================
    # تأیید نتیجه
    # ==========================================

    if text == "✅ قانونیه":

        from handlers.esm_check import vote_exit_result

        vote_exit_result(
            room,
            player
        )

        return True

    # --------------------------------------
    # اعتراض به نتیجه
    # --------------------------------------

    if text == "⚖️ اعتراض به نتیجه":

        from handlers.esm_check import start_protest

        start_protest(
            room,
            player
        )

        return True

    # --------------------------------------
    # لغو اعتراض
    # --------------------------------------

    if text == "❌ لغو":

        room.data.pop(
            "protest_selector",
            None
        )

        room.data.pop(
            "protest_category",
            None
        )

        show_categories(
            player
        )

        return True

    # --------------------------------------
    # انتخاب دسته اعتراض
    # --------------------------------------

    if (
        room.data.get("protest_selector") == player
        and text in categories
    ):

        from handlers.esm_check import select_protest_category

        select_protest_category(
            room,
            player,
            text
        )

        return True

    # --------------------------------------
    # انتخاب بازیکن مورد اعتراض
    # --------------------------------------

    if (
        room.data.get("protest_selector") == player
        and room.data.get("protest_category")
        and text.startswith("👤 ")
    ):

        target = None

        for opponent in room.players:

            nickname = get_nickname(
                opponent
            ) or "بازیکن"

            if text == f"👤 {nickname}":

                target = opponent

                break

        if target:

            from handlers.esm_check import select_protest_player

            select_protest_player(
                room,
                player,
                target
            )

            return True

    # --------------------------------------
    # تأیید اعتراض
    # --------------------------------------

    if text == "✅ تأیید اعتراض":

        from handlers.esm_check import vote_protest

        vote_protest(
            room,
            player,
            True
        )

        return True

    # --------------------------------------
    # رد اعتراض
    # --------------------------------------

    if text == "❌ رد اعتراض":

        from handlers.esm_check import vote_protest

        vote_protest(
            room,
            player,
            False
        )

        return True

    # --------------------------------------
    # لغو نوشتن جواب
    # --------------------------------------

    if text == "⬅️ انصراف":

        cancel_answer(
            room,
            player
        )

        return True

    # --------------------------------------
    # آماده
    # --------------------------------------

    if text == "✅ آماده‌ام":

        player_ready(
            room,
            player
        )

        return True

    # --------------------------------------
    # انتخاب دسته معمولی
    # --------------------------------------

    if text in categories:

        select_category(
            room,
            player,
            text
        )

        return True

    # --------------------------------------
    # ثبت جواب
    # --------------------------------------

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
# جواب‌های بازیکن
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
# خروج
# ==========================================

def exit_game(
    room,
    player
):

    from rooms.manager import leave_room
    from handlers.menu import room_menu

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

    from handlers.esm_check import show_result

    show_result(
        room
    )


# ==========================================
# ریست بازی
# ==========================================

def reset_game(room):

    room.data["answers"] = {}
    room.data["ready"] = []
    room.data["waiting"] = {}
    room.data["status_messages"] = {}

    for player in room.players:

        room.data["answers"][player] = {}