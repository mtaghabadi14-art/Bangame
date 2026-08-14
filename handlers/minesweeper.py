from rubika import (
    send_message,
    send_keypad,
    edit_message_text,
    edit_chat_keypad
)

from games.minesweeper import (
    create_game,
    reveal_cell,
    toggle_flag,
    is_finished,
    get_flag_count,
    get_board_size
)

from handlers.menu import games_menu


# ==========================================
# بازی‌های فعال
# ==========================================

active_games = {}


# ==========================================
# متن وضعیت
# ==========================================

def build_status_text(game):

    if game["finished"]:

        if game["won"]:

            return (
                "🏆 بازی تمام شد!\n\n"
                "💣 ماین‌یاب Vexon\n"
                f"{game['difficulty_name']}\n\n"
                "🎉 تبریک! همه خانه‌های امن را باز کردی!\n\n"
                f"💣 مین‌ها: {game['mine_count']}\n"
                f"🚩 پرچم‌ها: {get_flag_count(game)}"
            )

        return (
            "💥 BOOM!\n\n"
            "💣 ماین‌یاب Vexon\n"
            f"{game['difficulty_name']}\n\n"
            "💣 روی مین رفتی!\n\n"
            f"💣 مین‌ها: {game['mine_count']}\n"
            f"🚩 پرچم‌ها: {get_flag_count(game)}"
        )

    mode_text = (
        "🔓 باز کردن"
        if game.get("mode", "reveal") == "reveal"
        else "🚩 پرچم‌گذاری"
    )

    return (
        "🎮 ماین‌یاب Vexon\n\n"
        f"{game['difficulty_name']}\n"
        f"💣 مین‌ها: {game['mine_count']}\n"
        f"🚩 پرچم‌ها: {get_flag_count(game)}\n\n"
        f"🎯 حالت فعلی شما: {mode_text}\n\n"
        "👇 یک خانه را انتخاب کن."
    )


# ==========================================
# ساخت کی‌پد زمین
# ==========================================

def build_board_keypad(game):

    size = get_board_size(game)

    print(f"🟦 Minesweeper size={size}")

    buttons = []

    for row in range(size):

        row_buttons = []

        for col in range(size):

            position = (
                row,
                col
            )

            if position in game["revealed"]:

                value = game["board"][row][col]

                if value == -1:
                    button_text = "💣"

                elif value == 0:
                    button_text = "·"

                else:
                    button_text = str(value)

            elif position in game["flags"]:

                button_text = "🚩"

            else:

                button_text = "⬜"

            row_buttons.append({
                "id": f"mine_{row}_{col}",
                "text": button_text
            })

        buttons.append(row_buttons)

    # ======================================
    # کنترل‌های بازی
    # ======================================

    buttons.append([
        {
            "id": "minesweeper_reveal",
            "text": "🔓 باز کردن"
        },
        {
            "id": "minesweeper_flag",
            "text": "🚩 پرچم"
        }
    ])

    buttons.append([
        {
            "id": "minesweeper_new",
            "text": "🔄 بازی جدید"
        },
        {
            "id": "minesweeper_exit",
            "text": "🚪 خروج"
        }
    ])

    return buttons


# ==========================================
# ارسال زمین
# ==========================================

def send_board(
    chat_id,
    game
):

    return send_keypad(
        chat_id,
        "🎮 زمین ماین‌یاب:",
        build_board_keypad(game)
    )


# ==========================================
# بروزرسانی زمین
# ==========================================

def update_board(
    chat_id,
    game
):

    return edit_chat_keypad(
        chat_id,
        build_board_keypad(game)
    )


def start(
    chat_id,
    difficulty="easy"
):

    game = create_game(
        difficulty
    )

    game["mode"] = "reveal"

    active_games[chat_id] = game

    # ارسال زمین و وضعیت در یک پیام
    result = send_keypad(
        chat_id,
        build_status_text(game),
        build_board_keypad(game)
    )

    message_id = (
        result
        .get("data", {})
        .get("message_id")
    )

    game["status_message_id"] = message_id

    return game
# ==========================================
# انتخاب سطح
# ==========================================

def show_difficulty_menu(
    chat_id
):

    buttons = [
        [
            {
                "id": "minesweeper_easy",
                "text": "🟢 آسان"
            }
        ],
        [
            {
                "id": "minesweeper_medium",
                "text": "🟡 متوسط"
            }
        ],
        [
            {
                "id": "minesweeper_hard",
                "text": "🔴 سخت"
            }
        ],
        [
            {
                "id": "minesweeper_exit",
                "text": "🚪 خروج"
            }
        ]
    ]

    send_keypad(
        chat_id,
        (
            "💣 ماین‌یاب Vexon\n\n"
            "🎯 سطح بازی را انتخاب کن:"
        ),
        buttons
    )


# ==========================================
# بروزرسانی وضعیت
# ==========================================

def update_status(
    chat_id,
    game
):

    message_id = game.get(
        "status_message_id"
    )

    if not message_id:
        return False

    return edit_message_text(
        chat_id,
        message_id,
        build_status_text(game)
    )


# ==========================================
# حالت فعلی
# ==========================================

def get_mode(chat_id):

    game = active_games.get(
        chat_id
    )

    if not game:
        return None

    return game.get(
        "mode",
        "reveal"
    )


# ==========================================
# تغییر حالت
# ==========================================

def set_mode(
    chat_id,
    mode
):

    game = active_games.get(
        chat_id
    )

    if not game:
        return False

    if mode not in (
        "reveal",
        "flag"
    ):
        return False

    game["mode"] = mode

    update_status(
        chat_id,
        game
    )

    return True


# ==========================================
# انتخاب خانه
# ==========================================

def handle_cell(
    chat_id,
    row,
    col
):

    game = active_games.get(
        chat_id
    )

    if not game:
        return False

    # ======================================
    # بازی تمام شده
    # ======================================

    if is_finished(game):
        return True

    mode = get_mode(
        chat_id
    )

    # ======================================
    # پرچم
    # ======================================

    if mode == "flag":

        result = toggle_flag(
            game,
            row,
            col
        )

        if not result["success"]:

            reason = result["reason"]

            if reason == "already_revealed":

                send_message(
                    chat_id,
                    "❌ این خانه قبلاً باز شده است."
                )

            elif reason == "too_many_flags":

                send_message(
                    chat_id,
                    "🚩 تعداد پرچم‌ها به تعداد مین‌ها رسیده است."
                )

            return True

        update_status(
            chat_id,
            game
        )

        update_board(
            chat_id,
            game
        )

        return True

    # ======================================
    # باز کردن
    # ======================================

    result = reveal_cell(
        game,
        row,
        col
    )

    if not result["success"]:

        reason = result["reason"]

        if reason == "already_revealed":

            send_message(
                chat_id,
                "❌ این خانه قبلاً باز شده است."
            )

        elif reason == "flagged":

            send_message(
                chat_id,
                "🚩 این خانه پرچم دارد؛ اول پرچم را بردار."
            )

        return True

    # ======================================
    # وضعیت و زمین
    # ======================================

    update_status(
        chat_id,
        game
    )

    update_board(
        chat_id,
        game
    )

    # ======================================
    # پایان بازی
    # ======================================

    if is_finished(game):

        active_games.pop(
            chat_id,
            None
        )

        games_menu(
            chat_id
        )

        return True

    return True    


# ==========================================
# کنترل‌های بازی
# ==========================================

def handle_control(
    chat_id,
    action
):

    # ======================================
    # آسان
    # ======================================

    if action == "minesweeper_easy":

        start(
            chat_id,
            "easy"
        )

        return True

    # ======================================
    # متوسط
    # ======================================

    if action == "minesweeper_medium":

        start(
            chat_id,
            "medium"
        )

        return True

    # ======================================
    # سخت
    # ======================================

    if action == "minesweeper_hard":

        start(
            chat_id,
            "hard"
        )

        return True

    # ======================================
    # باز کردن
    # ======================================

    if action == "minesweeper_reveal":

        return set_mode(
            chat_id,
            "reveal"
        )

    # ======================================
    # پرچم
    # ======================================

    if action == "minesweeper_flag":

        return set_mode(
            chat_id,
            "flag"
        )

    # ======================================
    # بازی جدید
    # ======================================

    if action == "minesweeper_new":

        old_game = active_games.get(
            chat_id
        )

        difficulty = "easy"

        if old_game:

            difficulty = old_game.get(
                "difficulty",
                "easy"
            )

        start(
            chat_id,
            difficulty
        )

        return True

    # ======================================
    # خروج
    # ======================================

    if action == "minesweeper_exit":

        exit_game(
            chat_id
        )

        return True

    return False


# ==========================================
# خروج
# ==========================================

def exit_game(
    chat_id
):

    active_games.pop(
        chat_id,
        None
    )

    send_message(
        chat_id,
        "🚪 از ماین‌یاب خارج شدی."
    )

    games_menu(
        chat_id
    )