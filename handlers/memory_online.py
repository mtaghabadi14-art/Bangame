import threading

from rubika import (
    send_message,
    delete_message
)

from handlers.menu import room_menu

from handlers.memory_online_buttons import (
    memory_answer_message,
    wrong_answer_message,
    eliminated_message,
    winner_message,
    no_winner_message
)

from games.memory_online import (
    create_game,
    get_sequence_text,
    submit_answer,
    check_all_eliminated
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
        f"⏳ فقط {MEMORY_SHOW_TIME} ثانیه وقت داری!\n"
        "❤️❤️❤️ هر بازیکن ۳ تلاش دارد!"
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

    # تایمر حذف ترتیب
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

    # حذف پیام ترتیب برای هر بازیکن
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

    # پیام پاسخ
    for player in room.players:

        memory_answer_message(
            player,
            attempts=3
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
    # جواب صحیح
    # ==========================================

    if result["correct"]:

        room.data["memory_waiting"] = False

        winner = result["winner"]

        for player_id in room.players:

            winner_message(
                player_id,
                winner
            )

        # پایان بازی
        room.started = False

        return True


    # ==========================================
    # بازیکن حذف شده
    # ==========================================

    if result["eliminated"]:

        eliminated_message(
            player
        )

        # بررسی حذف شدن همه بازیکنان
        all_eliminated = check_all_eliminated(
            game,
            room.players
        )

        if all_eliminated:

            room.data[
                "memory_waiting"
            ] = False

            for player_id in room.players:

                no_winner_message(
                    player_id
                )

            room.started = False

        return True


    # ==========================================
    # جواب اشتباه ولی تلاش باقی مانده
    # ==========================================

    attempts_left = result[
        "attempts_left"
    ]

    wrong_answer_message(
        player,
        attempts_left
    )

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

    # اطلاع به بازیکنان باقی‌مانده
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

    room.started = False