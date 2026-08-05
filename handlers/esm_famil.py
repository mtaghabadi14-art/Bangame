import random

from rubika import send_message

from rooms.manager import delete_room

from handlers.esm_buttons import (
    show_categories
)

from handlers.esm_answers import (
    choose_category,
    save_answer,
    ready
)


# ==========================================
# بازی های فعال (فعلاً نگه می‌داریم)
# ==========================================

games = {}


# ==========================================
# دسته بندی ها
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
# حروف قابل استفاده
# (ث، ذ، ض، ظ، ژ حذف شده)
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
# شروع بازی
# ==========================================

def start(room):

    letter = random.choice(
        letters
    )


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
# ذخیره جواب بازیکن
# ==========================================

def add_answer(room, player, text):

    return save_answer(
        room,
        player,
        text
    )



# ==========================================
# آماده شدن بازیکن
# ==========================================

def player_ready(room, player):

    ready(
        room,
        player
    )



# ==========================================
# بررسی وضعیت بازی
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
# مدیریت پیام بازیکن
# ==========================================

def handle(room, player, text):
    print("ESM HANDLE:", text)

    # تست خروج خودکار بعد از هر پیام
    if text == "تمام":
    
        delete_room(
            room.room_id
        )
    
        send_message(
            player,
            "✅ بازی اسم و فامیل بسته شد."
        )
    
        return True

    print("ESM HANDLE:", text)


    # خروج از بازی

    if text == "🚪 خروج از بازی":

        exit_game(
            room.room_id,
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
# گرفتن جواب های بازیکن
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
# پاک کردن جواب ها
# ==========================================

def clear_answers(room):

    room.data["answers"] = {}

    for player in room.players:

        room.data["answers"][player] = {}
        # ==========================================
# خروج از بازی اسم و فامیل
# ==========================================

def exit_game(room_id, chat_id):

    # حذف بازیکن از بازی

    if room_id not in games:

        send_message(
            chat_id,
            "🚪 از بازی خارج شدی."
        )

        return



    games[room_id]["players"] = [
        p for p in games[room_id]["players"]
        if p != chat_id
    ]


    send_message(
        chat_id,
        "🚪 از بازی اسم و فامیل خارج شدی."
    )



    # اگر کسی باقی نماند

    if len(
        games[room_id]["players"]
    ) == 0:

        del games[room_id]



# ==========================================
# پایان دور
# ==========================================

def finish_round(room):

    for player in room.players:

        send_message(
            player,
            "🎉 دور بازی تمام شد!\n"
            "به‌زودی امتیازدهی اضافه می‌شود."
        )

    delete_room(
        room.room_id
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