from rubika import send_message, send_keypad

from games.uno.cards import (
    RED,
    GREEN,
    BLUE,
    YELLOW,
    WILD,
    WILD_DRAW_FOUR,
    COLOR_EMOJIS
)

from games.uno.manager import (
    get_uno_game,
    create_uno_game,
    remove_uno_game
)


# ==========================================
# Button IDs
# ==========================================

START_ID = "uno_start"
DRAW_ID = "uno_draw"
UNO_ID = "uno_call"
EXIT_ID = "uno_exit"

CARD_PREFIX = "uno_card_"
COLOR_PREFIX = "uno_color_"


# ==========================================
# نمایش Lobby
# ==========================================

def show_lobby(room):

    for player in room.players:

        buttons = []

        if player == room.host:

            buttons.append([
                {
                    "id": START_ID,
                    "text": "▶️ شروع UNO"
                }
            ])

        buttons.append([
            {
                "id": EXIT_ID,
                "text": "🚪 خروج از اتاق"
            }
        ])

        text = (
            "🃏 UNO — VEXON\n\n"
            f"🔑 کد اتاق: {room.room_id}\n"
            f"👥 بازیکنان: "
            f"{len(room.players)} / "
            f"{room.max_players}\n\n"
        )

        for index, p in enumerate(
            room.players,
            start=1
        ):

            nickname = _nickname(p)

            if p == room.host:

                text += (
                    f"{index}. 👑 {nickname}\n"
                )

            else:

                text += (
                    f"{index}. 🃏 {nickname}\n"
                )

        if len(room.players) < room.min_players:

            text += (
                "\n⏳ هنوز بازیکن کافی نیست."
            )

        else:

            text += (
                "\n✅ آماده شروع!"
            )

        send_keypad(
            player,
            text,
            buttons
        )


# ==========================================
# گرفتن لقب
# ==========================================

def _nickname(player):

    try:

        from database import get_nickname

        nickname = get_nickname(player)

        if nickname:
            return nickname

    except Exception:

        pass

    return "بازیکن"


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

    game = create_uno_game(
        room
    )

    if not game.start():

        remove_uno_game(
            room
        )

        send_message(
            chat_id,
            "❌ شروع UNO ناموفق بود."
        )

        return

    room.started = True

    for player in room.players:

        send_message(
            player,
            "🃏 UNO شروع شد! 🔥"
        )

    render_all(room)


# ==========================================
# متن بازی
# ==========================================

def build_game_text(
    game,
    player
):

    top = game.top_card()

    top_text = (
        top.display()
        if top
        else "🃏"
    )

    current_color = COLOR_EMOJIS.get(
        game.current_color,
        "❔"
    )

    current_player = game.current_player()

    hand_count = len(
        game.hand(player)
    )

    text = (
        "🃏 UNO — VEXON\n\n"
        f"🃏 روی زمین: {top_text}\n"
        f"🎨 رنگ فعلی: {current_color}\n"
        f"🎴 کارت‌های Deck: "
        f"{game.deck.count()}\n\n"
    )

    if current_player == player:

        text += "🎯 نوبت توست!\n\n"

    else:

        nickname = _nickname(current_player)

        text += (
            f"⏳ نوبت: {nickname}\n\n"
        )

    text += (
        f"🖐️ کارت‌های تو: "
        f"{hand_count}"
    )

    return text


# ==========================================
# ساخت Keypad بازی
# ==========================================

def build_game_keypad(
    game,
    player
):

    buttons = []

    hand = game.hand(player)

    # --------------------------------------
    # کارت‌ها
    # --------------------------------------

    row = []

    for card in hand:

        row.append({
            "id": (
                f"{CARD_PREFIX}"
                f"{card.card_id}"
            ),
            "text": card.display()
        })

        if len(row) == 3:

            buttons.append(row)

            row = []

    if row:

        buttons.append(row)

    # --------------------------------------
    # Draw
    # --------------------------------------

    buttons.append([
        {
            "id": DRAW_ID,
            "text": "🎴 برداشتن کارت"
        }
    ])

    # --------------------------------------
    # UNO
    # --------------------------------------

    if len(hand) == 1:

        buttons.append([
            {
                "id": UNO_ID,
                "text": "🃏 UNO!"
            }
        ])

    # --------------------------------------
    # Exit
    # --------------------------------------

    buttons.append([
        {
            "id": EXIT_ID,
            "text": "🚪 خروج از بازی"
        }
    ])

    return buttons


# ==========================================
# نمایش بازی برای همه
# ==========================================

def render_all(room):

    game = get_uno_game(room)

    if game is None:
        return

    for player in room.players:

        send_keypad(
            player,
            build_game_text(
                game,
                player
            ),
            build_game_keypad(
                game,
                player
            )
        )


# ==========================================
# منوی انتخاب رنگ
# ==========================================

def show_color_menu(chat_id):

    buttons = [
        [
            {
                "id": f"{COLOR_PREFIX}{RED}",
                "text": "🔴 قرمز"
            },
            {
                "id": f"{COLOR_PREFIX}{GREEN}",
                "text": "🟢 سبز"
            }
        ],
        [
            {
                "id": f"{COLOR_PREFIX}{BLUE}",
                "text": "🔵 آبی"
            },
            {
                "id": f"{COLOR_PREFIX}{YELLOW}",
                "text": "🟡 زرد"
            }
        ]
    ]

    send_keypad(
        chat_id,
        "🎨 رنگ کارت Wild را انتخاب کن:",
        buttons
    )


# ==========================================
# پایان بازی
# ==========================================

def finish_game(
    room,
    game
):

    winner = _nickname(
        game.winner
    )

    text = (
        "🏆 بازی UNO تمام شد! 🎉\n\n"
        f"🥇 برنده: {winner}\n\n"
        "🎴 تعداد کارت باقی‌مانده:\n"
    )

    for player in room.players:

        nickname = _nickname(player)

        text += (
            f"👤 {nickname}: "
            f"{len(game.hand(player))} کارت\n"
        )

    for player in room.players:

        send_message(
            player,
            text
        )


# ==========================================
# کنترل بازی
# ==========================================

def handle(
    room,
    chat_id,
    button_id
):

    game = get_uno_game(room)

    # --------------------------------------
    # Lobby
    # --------------------------------------

    if game is None:

        if button_id == START_ID:

            start_game(
                room,
                chat_id
            )

        elif button_id == EXIT_ID:

            exit_game(
                room,
                chat_id
            )

        return

    # --------------------------------------
    # شروع
    # --------------------------------------

    if button_id == START_ID:

        start_game(
            room,
            chat_id
        )

        return

    # --------------------------------------
    # خروج
    # --------------------------------------

    if button_id == EXIT_ID:

        exit_game(
            room,
            chat_id
        )

        return

    # --------------------------------------
    # پایان
    # --------------------------------------

    if game.finished:

        send_message(
            chat_id,
            "🏁 این بازی تمام شده است."
        )

        return

    # --------------------------------------
    # انتخاب رنگ
    # --------------------------------------

    if button_id.startswith(
        COLOR_PREFIX
    ):

        color = button_id.replace(
            COLOR_PREFIX,
            "",
            1
        )

        result = game.choose_color(
            chat_id,
            color
        )

        if not result["success"]:

            send_message(
                chat_id,
                result["message"]
            )

            return

        send_message(
            chat_id,
            "🎨 رنگ انتخاب شد: "
            f"{COLOR_EMOJIS[color]}"
        )

        render_all(room)

        return

    # --------------------------------------
    # UNO
    # --------------------------------------

    if button_id == UNO_ID:

        result = game.call_uno(
            chat_id
        )

        if not result["success"]:

            send_message(
                chat_id,
                result["message"]
            )

            return

        send_message(
            chat_id,
            "🃏 UNO گفتی! 🔥"
        )

        render_all(room)

        return

    # --------------------------------------
    # Draw
    # --------------------------------------

    if button_id == DRAW_ID:

        result = game.draw_for_player(
            chat_id
        )

        if not result["success"]:

            send_message(
                chat_id,
                result["message"]
            )

            return

        card = result["card"]

        if result["playable"]:

            send_message(
                chat_id,
                "🎴 کارت گرفتی:\n\n"
                f"{card.display()}\n\n"
                "✅ این کارت قابل بازی است."
            )

        else:

            send_message(
                chat_id,
                "🎴 کارت گرفتی:\n\n"
                f"{card.display()}\n\n"
                "❌ این کارت قابل بازی نیست.\n"
                "⏭️ نوبت به بازیکن بعدی رسید."
            )

        render_all(room)

        return

    # --------------------------------------
    # کارت
    # --------------------------------------

    if button_id.startswith(
        CARD_PREFIX
    ):

        card_id = button_id.replace(
            CARD_PREFIX,
            "",
            1
        )

        result = game.play_card_by_id(
            chat_id,
            card_id
        )

        if not result["success"]:

            send_message(
                chat_id,
                result["message"]
            )

            return

        card = result["card"]

        # ----------------------------------
        # برنده
        # ----------------------------------

        if "winner" in result:

            finish_game(
                room,
                game
            )

            room.started = False

            return

        send_message(
            chat_id,
            f"✅ {card.display()} بازی شد."
        )

        # ----------------------------------
        # Wild
        # ----------------------------------

        if result["effect"] == "choose_color":

            show_color_menu(
                chat_id
            )

            return

        # ----------------------------------
        # سایر کارت‌ها
        # ----------------------------------

        render_all(room)

        return


# ==========================================
# خروج از بازی
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

    remove_uno_game(
        room
    )

    send_message(
        chat_id,
        "🚪 از UNO خارج شدی."
    )

    for player in other_players:

        send_message(
            player,
            "⚠️ یکی از بازیکنان از UNO خارج شد."
        )