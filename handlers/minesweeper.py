from rubika import (
    send_message,
    send_keypad,
    send_inline_keypad
)

from games.minesweeper import (
    create_game,
    reveal_cell,
    toggle_flag,
    is_finished,
    is_won,
    get_remaining_mines,
    get_flag_count,
    BOARD_SIZE
)

from handlers.menu import room_menu


# ==========================================
# بازی‌های فعال ماین‌یاب
# ==========================================

active_games = {}


# ==========================================
# ساخت متن صفحه
# ==========================================

def build_board_text(game):

    text = (
        "💣 ماین‌یاب Vexon\n\n"
        f"💣 مین‌ها: {get_remaining_mines(game)}\n"
        f"🚩 پرچم‌ها: {get_flag_count(game)}\n\n"
    )

    if game["finished"]:

        if game["won"]:
            text += "🏆 تبریک! همه خانه‌های امن را باز کردی!\n\n"
        else:
            text += "💥 BOOM! روی مین رفتی!\n\n"

    else:

        text += "👇 یک خانه را انتخاب کن:\n\n"

    return text


# ==========================================
# ساخت Chat Keypad صفحه بازی
# ==========================================

def build_board_keypad(game):

    buttons = []

    for row in range(BOARD_SIZE):

        row_buttons = []

        for col in range(BOARD_SIZE):

            position = (
                row,
                col
            )

            # خانه باز شده
            if position in game["revealed"]:

                value = game["board"][row][col]

                if value == 0:
                    button_text = "·"

                else:
                    button_text = str(value)

            # خانه پرچم‌گذاری شده
            elif position in game["flags"]:

                button_text = "🚩"

            # خانه بسته
            else:

                button_text = "⬜"

            row_buttons.append({
                "id": f"mine_{row}_{col}",
                "text": button_text
            })

        buttons.append(row_buttons)

    return buttons


# ==========================================
# ساخت Inline Keypad کنترل‌ها
# ==========================================

def build_control_buttons(game):

    if game["finished"]:

        return [
            [
                {
                    "id": "minesweeper_new",
                    "text": "🔄 بازی جدید"
                },
                {
                    "id": "minesweeper_exit",
                    "text": "🚪 خروج"
                }
            ]
        ]

    return [
        [
            {
                "id": "minesweeper_reveal",
                "text": "🔓 باز کردن"
            },
            {
                "id": "minesweeper_flag",
                "text": "🚩 پرچم"
            }
        ],
        [
            {
                "id": "minesweeper_exit",
                "text": "🚪 خروج"
            }
        ]
    ]


# ==========================================
# ارسال صفحه بازی
# ==========================================

def send_board(
    chat_id,
    game
):

    text = build_board_text(game)

    # صفحه بازی = Chat Keypad
    board_keypad = build_board_keypad(game)

    send_keypad(
        chat_id,
        text,
        board_keypad
    )

    # کنترل‌ها = Inline Keypad
    control_buttons = build_control_buttons(game)

    send_inline_keypad(
        chat_id,
        "🎮 کنترل ماین‌یاب:",
        control_buttons
    )


# ==========================================
# شروع بازی
# ==========================================

def start(
    chat_id
):

    game = create_game()

    active_games[chat_id] = game

    send_board(
        chat_id,
        game
    )


# ==========================================
# حالت فعلی بازیکن
# ==========================================

def get_mode(chat_id):

    game_data = active_games.get(
        chat_id
    )

    if not game_data:

        return None

    return game_data.get(
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

    if is_finished(game):

        send_message(
            chat_id,
            "🏁 این بازی تمام شده است."
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

            if result["reason"] == "already_revealed":

                send_message(
                    chat_id,
                    "❌ این خانه قبلاً باز شده است."
                )

            return True

        send_board(
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

        if result["reason"] == "already_revealed":

            send_message(
                chat_id,
                "❌ این خانه قبلاً باز شده است."
            )

        elif result["reason"] == "flagged":

            send_message(
                chat_id,
                "🚩 این خانه پرچم دارد؛ "
                "اول پرچم را بردار."
            )

        return True

    # نمایش نتیجه
    send_board(
        chat_id,
        game
    )

    return True


# ==========================================
# دکمه‌های Inline
# ==========================================

def handle_control(
    chat_id,
    action
):

    game = active_games.get(
        chat_id
    )

    # ======================================
    # باز کردن
    # ======================================

    if action == "minesweeper_reveal":

        if not game:
            return False

        set_mode(
            chat_id,
            "reveal"
        )

        send_message(
            chat_id,
            "🔓 حالت باز کردن فعال شد.\n"
            "حالا یک خانه را انتخاب کن."
        )

        return True

    # ======================================
    # پرچم
    # ======================================

    if action == "minesweeper_flag":

        if not game:
            return False

        set_mode(
            chat_id,
            "flag"
        )

        send_message(
            chat_id,
            "🚩 حالت پرچم فعال شد.\n"
            "حالا یک خانه را انتخاب کن."
        )

        return True

    # ======================================
    # بازی جدید
    # ======================================

    if action == "minesweeper_new":

        start(
            chat_id
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

    # برگشت به کافه بازی
    room_menu(
        chat_id
    )