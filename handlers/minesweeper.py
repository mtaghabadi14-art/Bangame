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

from handlers.menu import room_menu


# ==========================================
# بازی‌های فعال
# ==========================================

active_games = {}


# ==========================================
# ساخت متن وضعیت
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
        else
        "🚩 پرچم‌گذاری"
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

    buttons = []

    for row in range(size):

        row_buttons = []

        for col in range(size):

            position = (
                row,
                col
            )

            # ==================================
            # خانه باز شده
            # ==================================

            if position in game["revealed"]:

                value = game["board"][row][col]

                if value == -1:

                    button_text = "💣"

                elif value == 0:

                    button_text = "·"

                else:

                    button_text = str(value)

            # ==================================
            # پرچم
            # ==================================

            elif position in game["flags"]:

                button_text = "🚩"

            # ==================================
            # خانه بسته
            # ==================================

            else:

                button_text = "⬜"

            row_buttons.append({
                "id": f"mine_{row}_{col}",
                "text": button_text
            })

        buttons.append(
            row_buttons
        )

    # ==========================================
    # کنترل‌ها
    # ==========================================

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
# ارسال اولیه زمین
# فقط در شروع بازی
# ==========================================

def send_board(
    chat_id,
    game
):

    text = build_status_text(
        game
    )

    keypad = build_board_keypad(
        game
    )

    return send_keypad(
        chat_id,
        text,
        keypad
    )


# ==========================================
# بروزرسانی زمین
# بدون ارسال پیام جدید
# ==========================================

def update_board(
    chat_id,
    game
):

    keypad = build_board_keypad(
        game
    )

    return edit_chat_keypad(
        chat_id,
        keypad
    )


# ==========================================
# شروع بازی
# ==========================================

def start(
    chat_id,
    difficulty="easy"
):

    game = create_game(
        difficulty
    )

    # حالت اولیه
    game["mode"] = "reveal"
    game["finished"] = game.get(
        "finished",
        False
    )

    active_games[chat_id] = game

    # ======================================
    # پیام وضعیت
    # ======================================

    result = send_message(
        chat_id,
        build_status_text(game)
    )

    message_id = (
        result
        .get("data", {})
        .get("message_id")
    )

    game["status_message_id"] = message_id

    # ======================================
    # ارسال اولیه زمین
    # ======================================

    send_board(
        chat_id,
        game
    )

    return game


# ==========================================
# منوی انتخاب سختی
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
# بروزرسانی پیام وضعیت
# بدون پیام جدید
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

    result = edit_message_text(
        chat_id,
        message_id,
        build_status_text(game)
    )

    return result


# ==========================================
# گرفتن حالت فعلی
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

    # فقط پیام وضعیت ویرایش می‌شود
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
    # اگر بازی تمام شده
    # ======================================

    if is_finished(game):

        update_status(
            chat_id,
            game
        )

        return True

    mode = get_mode(
        chat_id
    )

    # ======================================
    # حالت پرچم
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

        # ==================================
        # بروزرسانی پیام وضعیت
        # ==================================

        update_status(
            chat_id,
            game
        )

        # ==================================
        # ویرایش همان کی‌پد
        # ==================================

        update_board(
            chat_id,
            game
        )

        return True

    # ======================================
    # حالت باز کردن
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
    # بروزرسانی وضعیت
    # ======================================

    update_status(
        chat_id,
        game
    )

    # ======================================
    # اگر بازی تمام شد
    # ======================================

    if is_finished(game):

        update_board(
            chat_id,
            game
        )

        return True

    # ======================================
    # بروزرسانی همان کی‌پد
    # ======================================

    update_board(
        chat_id,
        game
    )

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

        game = active_games.get(
            chat_id
        )

        if not game:
            return False

        return set_mode(
            chat_id,
            "reveal"
        )

    # ======================================
    # پرچم
    # ======================================

    if action == "minesweeper_flag":

        game = active_games.get(
            chat_id
        )

        if not game:
            return False

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
# خروج از بازی
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

    room_menu(
        chat_id
    )