import threading

from rubika import (
    send_message,
    delete_message
)

from handlers.menu import room_menu

from games.memory_online import (
    create_game,
    get_sequence_text,
    submit_answer
)

from rooms.manager import (
    start_game,
    leave_room
)


# ==========================================
# زمان نمایش ترتیب
# ==========================================

MEMORY_SHOW_TIME = 5


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

    start_game(room)

    start(room)

    return True


# ==========================================
# شروع بازی
# ==========================================

def start(room):

    # جلوگیری از شروع دوباره
    if not room.started:

        return

    # ساخت بازی
    game = create_game()

    room.data["memory_game"] = game

    room.data["memory_waiting"] = False

    room.data["memory_message_ids"] = {}

    sequence_text = get_sequence_text(
        game
    )

    text = (
        "🧠 بازی حافظه شروع شد!\n\n"
        "👀 ترتیب زیر را خوب به خاطر بسپار:\n\n"
        f"{sequence_text}\n\n"
        f"⏳ فقط {MEMORY_SHOW_TIME} ثانیه وقت داری!"
    )

    # ارسال ترتیب به همه بازیکنان
    for player in room.players:

        result = send_message(
            player,
            text
        )

        if (
            isinstance(result, dict)
            and result.get("status") == "OK"
        ):

            message_data = result.get(
                "data",
                {}
            )

            message_id = message_data.get(
                "message_id"
            )

            if message_id:

                room.data[
                    "memory_message_ids"
                ][player] = message_id

    # بعد از چند ثانیه وارد مرحله پاسخ شو
    timer = threading.Timer(
        MEMORY_SHOW_TIME,
        hide_sequence,
        args=(room,)
    )

    timer.daemon = True

    timer.start()


# ==========================================
# حذف نمایش ترتیب
# ==========================================

def hide_sequence(room):

    # اگر بازی دیگر وجود ندارد
    if room.data.get(
        "memory_game"
    ) is None:

        return

    game = room.data.get(
        "memory_game"
    )

    # اگر بازی تمام شده
    if game.get("finished"):

        return

    message_ids = room.data.get(
        "memory_message_ids",
        {}
    )

    # حذف پیام برای هر بازیکن
    for player, message_id in message_ids.items():

        try:

            delete_message(
                player,
                message_id
            )

        except Exception as e:

            print(
                "MEMORY DELETE ERROR:",
                e
            )

    room.data["memory_waiting"] = True

    # پیام جدید برای پاسخ
    for player in room.players:

        send_message(
            player,
            "🧠 حالا نوبت توئه!\n\n"
            "😂 ترتیب ایموجی‌ها را دقیقاً "
            "همان‌طور که دیدی بفرست.\n\n"
            "⚠️ فاصله مهم نیست؛ ترتیب مهم است!"
        )


# ==========================================
# دریافت جواب بازیکن
# ==========================================

def handle_answer(room, player, text):

    if room.data.get(
        "memory_waiting"
    ) is not True:

        return False

    game = room.data.get(
        "memory_game"
    )

    if not game:

        return False

    result = submit_answer(
        game,
        player,
        text
    )

    # ==========================================
    # جواب اشتباه
    # ==========================================

    if not result["correct"]:

        if not result["finished"]:

            send_message(
                player,
                "❌ ترتیب اشتباه بود!\n"
                "دوباره تلاش کن."
            )

        return True

    # ==========================================
    # جواب صحیح
    # ==========================================

    room.data["memory_waiting"] = False

    winner = result["winner"]

    winner_text = (
        "🏆 برنده بازی حافظه!\n\n"
        f"🎉 بازیکن برنده: {winner}\n\n"
        "⚡ اولین نفری بود که ترتیب را درست فرستاد!"
    )

    # اعلام برنده به همه
    for player_id in room.players:

        send_message(
            player_id,
            winner_text
        )

    # پایان وضعیت بازی
    room.started = False

    return True


# ==========================================
# خروج از بازی
# ==========================================

def exit_game(room, player):

    if player not in room.players:

        return False

    leave_room(
        player
    )

    send_message(
        player,
        "🚪 از بازی حافظه خارج شدی."
    )

    # برگشت مستقیم به کافه بازی
    room_menu(
        player
    )

    # اگر اتاق هنوز وجود دارد
    if room.players:

        for player_id in room.players:

            send_message(
                player_id,
                "👤 یکی از بازیکنان از بازی خارج شد."
            )

    return True


# ==========================================
# پایان بازی
# ==========================================

def end_game(room):

    room.data["memory_waiting"] = False

    room.data["memory_game"] = None

    room.data["memory_message_ids"] = {}

    room.started = False