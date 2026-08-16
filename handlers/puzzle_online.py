from rubika import send_message, send_keypad
from database import get_nickname
from handlers.rooms import open_room_menu

from games.puzzle_online.manager import (
    get_puzzle_game,
    create_puzzle_game,
    remove_puzzle_game
)


# ==========================================
# Button IDs
# ==========================================

START_ID = "puzzle_start"
EXIT_ID = "puzzle_exit"


# ==========================================
# نمایش Lobby
# ==========================================

def show_lobby(room):

    for player in room.players:

        players_text = ""

        for index, p in enumerate(
            room.players,
            start=1
        ):

            nickname = get_nickname(p)

            if not nickname:
                nickname = "بازیکن"

            if p == room.host:

                players_text += (
                    f"{index}. 👑 {nickname}\n"
                )

            else:

                players_text += (
                    f"{index}. 🧩 {nickname}\n"
                )

        text = (
            "🧩 پازل چندنفره — VEXON\n\n"
            f"🔑 کد اتاق: {room.room_id}\n\n"
            f"👥 بازیکنان: "
            f"{len(room.players)} / "
            f"{room.max_players}\n\n"
            f"{players_text}\n"
        )

        if len(room.players) < room.min_players:

            text += (
                "⏳ برای شروع هنوز بازیکن کافی نیست."
            )

        else:

            text += (
                "✅ بازیکنان آماده‌اند!"
            )

        buttons = []

        if player == room.host:

            if len(room.players) >= room.min_players:

                buttons.append([
                    {
                        "id": START_ID,
                        "text": "▶️ شروع پازل"
                    }
                ])

        buttons.append([
            {
                "id": EXIT_ID,
                "text": "🚪 خروج از اتاق"
            }
        ])

        send_keypad(
            player,
            text,
            buttons
        )


# ==========================================
# شروع بازی
# ==========================================

def start_game(
    room,
    chat_id
):

    if chat_id != room.host:

        send_message(
            chat_id,
            "❌ فقط میزبان می‌تواند بازی را شروع کند."
        )

        return

    if len(room.players) < room.min_players:

        send_message(
            chat_id,
            f"❌ حداقل "
            f"{room.min_players} بازیکن لازم است."
        )

        return

    if room.started:

        send_message(
            chat_id,
            "⚠️ بازی قبلاً شروع شده است."
        )

        return

    game = create_puzzle_game(
        room
    )

    if not game.start():

        remove_puzzle_game(
            room
        )

        send_message(
            chat_id,
            "❌ شروع بازی پازل ناموفق بود."
        )

        return

    room.started = True

    for player in room.players:

        send_message(
            player,
            "🧩 پازل چندنفره شروع شد! 🔥"
        )

    render_question(
        room
    )


# ==========================================
# ساخت متن سؤال
# ==========================================

def build_question_text(
    game,
    player
):

    question = game.get_question()

    if question is None:

        return (
            "🧩 پازل\n\n"
            "❌ سؤال فعالی وجود ندارد."
        )

    nickname = get_nickname(
        player
    )

    if not nickname:
        nickname = "بازیکن"

    answered = game.has_answered(
        player
    )

    text = (
        "🧩 پازل چندنفره — VEXON\n\n"
        f"📚 دسته: {question['category']}\n"
        f"🔢 سؤال {game.round_number()} "
        f"از {game.TOTAL_ROUNDS}\n\n"
        f"❓ {question['question']}\n\n"
    )

    if answered:

        text += (
            "✅ جواب این سؤال را ثبت کردی.\n"
            "⏳ منتظر بقیه بازیکنان..."
        )

    else:

        text += (
            f"👤 {nickname}\n\n"
            "💬 جواب خودت را به صورت پیام "
            "ارسال کن."
        )

    return text


# ==========================================
# نمایش سؤال برای همه
# ==========================================

def render_question(room):

    game = get_puzzle_game(
        room
    )

    if game is None:
        return

    question = game.get_question()

    if question is None:
        return

    for player in room.players:

        text = build_question_text(
            game,
            player
        )

        send_keypad(
            player,
            text,
            [
                [
                    {
                        "id": EXIT_ID,
                        "text": "🚪 خروج از بازی"
                    }
                ]
            ]
        )


# ==========================================
# پایان دور
# ==========================================

def finish_round(room):

    game = get_puzzle_game(
        room
    )

    if game is None:
        return

    if game.finished:

        finish_game(
            room,
            game
        )

        return

    if not game.finish_round():

        finish_game(
            room,
            game
        )

        return

    render_question(
        room
    )


# ==========================================
# پایان بازی
# ==========================================

def finish_game(
    room,
    game
):

    winner = game.winner()

    winner_name = "نامشخص"

    if winner:

        winner_name = get_nickname(
            winner
        )

        if not winner_name:
            winner_name = "بازیکن"

    text = (
        "🏆━━━━━━━━━━━━━━━━🏆\n"
        "      🧩 پایان پازل!\n"
        "🏆━━━━━━━━━━━━━━━━🏆\n\n"
        f"🥇 برنده: {winner_name}\n\n"
        "📊 جدول امتیازات:\n\n"
    )

    leaderboard = game.leaderboard()

    for index, (
        player,
        score
    ) in enumerate(
        leaderboard,
        start=1
    ):

        nickname = get_nickname(
            player
        )

        if not nickname:
            nickname = "بازیکن"

        if index == 1:
            icon = "🥇"

        elif index == 2:
            icon = "🥈"

        elif index == 3:
            icon = "🥉"

        else:
            icon = "👤"

        text += (
            f"{icon} {nickname} — "
            f"{score} امتیاز\n"
        )

    # ==========================================
    # جواب‌های صحیح مسابقه
    # ==========================================

    text += (
        "\n━━━━━━━━━━━━━━━━━━\n"
        "📝 جواب‌های صحیح مسابقه:\n\n"
    )

    for index, question in enumerate(
        game.questions[:game.TOTAL_ROUNDS],
        start=1
    ):

        text += (
            f"{index}️⃣ {question['answer']}\n"
        )

    text += (
        "\n━━━━━━━━━━━━━━━━━━\n"
    )

    room.started = False

    for player in room.players:

        send_message(
            player,
            text
        )

        send_keypad(
            player,
            "🎮 بازی تمام شد!\n\n"
            "می‌توانی از کافه بازی دوباره "
            "یک اتاق بسازی.",
            [
                [
                    {
                        "id": EXIT_ID,
                        "text": "🚪 خروج از بازی"
                    }
                ]
            ]
        )

    remove_puzzle_game(
        room
    )


# ==========================================
# خروج
# ==========================================

def exit_game(
    room,
    chat_id
):

    from rooms.manager import delete_room

    other_players = [
        player
        for player in room.players
        if player != chat_id
    ]

    delete_room(
        room.room_id
    )

    remove_puzzle_game(
        room
    )

    send_message(
        chat_id,
        "🚪 از بازی پازل خارج شدی."
    )

    open_room_menu(
        chat_id
    )

    for player in other_players:

        send_message(
            player,
            "⚠️ یکی از بازیکنان از بازی خارج شد."
        )


# ==========================================
# دریافت جواب
# ==========================================

def receive_answer(
    room,
    chat_id,
    answer
):

    game = get_puzzle_game(
        room
    )

    if game is None:
        return False

    if game.finished:
        return True

    result = game.answer(
        chat_id,
        answer
    )

    if not result["success"]:

        send_message(
            chat_id,
            result["message"]
        )

        return True

    if result["correct"]:

        send_message(
            chat_id,
            "✅ جواب درست بود! 🎉\n"
            "+1 امتیاز"
        )

    else:

        send_message(
            chat_id,
            "❌ جواب اشتباه بود!"
        )

    if game.everyone_answered():

        finish_round(
            room
        )

    else:

        send_keypad(
            chat_id,
            build_question_text(
                game,
                chat_id
            ),
            [
                [
                    {
                        "id": EXIT_ID,
                        "text": "🚪 خروج از بازی"
                    }
                ]
            ]
        )

    return True


# ==========================================
# کنترل دکمه‌ها
# ==========================================

def handle(
    room,
    chat_id,
    button_id
):

    if button_id == EXIT_ID:

        exit_game(
            room,
            chat_id
        )

        return True

    if button_id == START_ID:

        start_game(
            room,
            chat_id
        )

        return True

    return False