import threading

from rubika import (
    send_message,
    delete_message
)

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
# تنظیمات بازی
# ==========================================

MEMORY_SHOW_TIME = 5

MAX_ATTEMPTS = 3


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

    if not room.started:

        return

    # ساخت بازی
    game = create_game()

    room.data["memory_game"] = game

    room.data["memory_waiting"] = False

    room.data["memory_message_ids"] = {}

    # تعداد تلاش هر بازیکن
    room.data["memory_attempts"] = {
        player: MAX_ATTEMPTS
        for player in room.players
    }

    # بازیکنان فعال
    room.data["memory_active_players"] = set(
        room.players
    )

    sequence_text = get_sequence_text(
        game
    )

    text = (
        "🧠 بازی حافظه شروع شد!\n\n"
        "👀 ترتیب زیر را خوب به خاطر بسپار:\n\n"
        f"{sequence_text}\n\n"
        f"⏳ فقط {MEMORY_SHOW_TIME} ثانیه وقت داری!"
    )

    # ارسال ترتیب به همه
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

    # شروع تایمر
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

    if room.data.get(
        "memory_game"
    ) is None:

        return

    game = room.data.get(
        "memory_game"
    )

    if game.get("finished"):

        return

    message_ids = room.data.get(
        "memory_message_ids",
        {}
    )

    # حذف پیام اصلی
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

    # پیام مرحله پاسخ
    for player in room.players:

        attempts = room.data[
            "memory_attempts"
        ].get(
            player,
            MAX_ATTEMPTS
        )

        send_message(
            player,
            "🧠 حالا نوبت توئه!\n\n"
            "😂 ترتیب ایموجی‌ها را همان‌طور "
            "که دیدی بفرست.\n\n"
            "⚠️ فاصله مهم نیست؛ ترتیب مهم است!\n\n"
            f"❤️ تلاش باقی‌مانده: {attempts}/{MAX_ATTEMPTS}"
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

    # اگر بازیکن از دور خارج شده
    active_players = room.data.get(
        "memory_active_players",
        set()
    )

    if player not in active_players:

        return True

    # تعداد تلاش فعلی
    attempts = room.data[
        "memory_attempts"
    ].get(
        player,
        MAX_ATTEMPTS
    )

    if attempts <= 0:

        return True

    result = submit_answer(
        game,
        player,
        text
    )

    # ==========================================
    # جواب اشتباه
    # ==========================================

    if not result["correct"]:

        attempts -= 1

        room.data[
            "memory_attempts"
        ][player] = attempts

        # هنوز تلاش دارد
        if attempts > 0:

            send_message(
                player,
                "❌ جواب اشتباه بود!\n\n"
                f"❤️ تلاش باقی‌مانده: "
                f"{attempts}/{MAX_ATTEMPTS}\n\n"
                "🔄 دوباره تلاش کن."
            )

            return True

        # ==========================================
        # تمام شدن تلاش بازیکن
        # ==========================================

        active_players.discard(
            player
        )

        send_message(
            player,
            "💔 هر ۳ تلاش را از دست دادی!\n\n"
            "❌ از این دور خارج شدی.\n"
            "⏳ منتظر نتیجه بازی باش..."
        )

        # ==========================================
        # اگر دیگر بازیکن فعالی نمانده
        # ==========================================

        if not active_players:

            room.data[
                "memory_waiting"
            ] = False

            for player_id in room.players:

                send_message(
                    player_id,
                    "🤷 هیچ‌کس نتوانست ترتیب را درست حدس بزند!\n\n"
                    "🏁 بازی تمام شد."
                )

            end_game(room)

        return True

    # ==========================================
    # جواب صحیح
    # ==========================================

    room.data[
        "memory_waiting"
    ] = False

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

    end_game(room)

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

    room.data[
        "memory_waiting"
    ] = False

    room.data[
        "memory_game"
    ] = None

    room.data[
        "memory_message_ids"
    ] = {}

    room.data[
        "memory_attempts"
    ] = {}

    room.data[
        "memory_active_players"
    ] = set()

    room.started = False
