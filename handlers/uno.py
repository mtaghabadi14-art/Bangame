from rubika import (
    send_message,
    send_keypad,
    remove_keypad
)

from database import get_nickname

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
# گرفتن لقب بازیکن
# ==========================================

def get_player_name(player):

    nickname = get_nickname(player)

    if nickname:
        return nickname

    return "بازیکن"


# ==========================================
# نمایش Lobby
# ==========================================

def show_lobby(room):

    for player in room.players:

        buttons = []

        # --------------------------------------
        # دکمه شروع فقط برای میزبان
        # --------------------------------------

        if player == room.host:

            if len(room.players) >= room.min_players:

                buttons.append([
                    {
                        "id": START_ID,
                        "text": "▶️ شروع UNO"
                    }
                ])

        # --------------------------------------
        # خروج
        # --------------------------------------

        buttons.append([
            {
                "id": EXIT_ID,
                "text": "🚪 خروج از اتاق"
            }
        ])

        # --------------------------------------
        # متن
        # --------------------------------------

        text = (
            "🃏 UNO — VEXON\n\n"
            f"🔑 کد اتاق: {room.room_id}\n\n"
            f"👥 بازیکنان: "
            f"{len(room.players)} / "
            f"{room.max_players}\n\n"
        )

        for index, p in enumerate(
            room.players,
            start=1
        ):

            nickname = get_player_name(p)

            if p == room.host:

                text += (
                    f"{index}. 👑 {nickname}\n"
                )

            else:

                text += (
                    f"{index}. 🃏 {nickname}\n"
                )

        # --------------------------------------
        # وضعیت
        # --------------------------------------

        if len(room.players) < room.min_players:

            text += (
                "\n⏳ منتظر بازیکن دیگر..."
            )

        else:

            if player == room.host:

                text += (
                    "\n✅ آماده شروع!"
                )

            else:

                text += (
                    "\n⏳ منتظر شروع میزبان..."
                )

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

    render_all(
        room
    )


# ==========================================
# متن بازی
# ==========================================

def build_game_text(
    game,
    player
):

    top = game.top_card()

    if top:

        top_text = top.display()

    else:

        top_text = "🃏"

    current_color = (
        COLOR_EMOJIS.get(
            game.current_color,
            "❔"
        )
    )

    current_player = (
        game.current_player()
    )

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

        text += (
            "🎯 نوبت توست!\n\n"
        )

    else:

        nickname = get_player_name(
            current_player
        )

        text += (
            f"⏳ نوبت: "
            f"{nickname}\n\n"
        )

    text += (
        f"🖐️ کارت‌های تو: "
        f"{hand_count}"
    )

    return text


# ==========================================
# ساخت Keypad دست بازیکن
# ==========================================

def build_game_keypad(
    game,
    player
):

    buttons = []

    hand = game.hand(
        player
    )

    # --------------------------------------
    # کارت‌ها
    # --------------------------------------

    row = []

    for index, card in enumerate(hand):

        row.append({
            "id": (
                f"{CARD_PREFIX}"
                f"{index}"
            ),
            "text": card.display()
        })

        if len(row) == 3:

            buttons.append(
                row
            )

            row = []

    if row:

        buttons.append(
            row
        )

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
    # همیشه نمایش داده می‌شود
    # --------------------------------------

    buttons.append([
        {
            "id": UNO_ID,
            "text": "🃏 UNO!"
        }
    ])

    # --------------------------------------
    # خروج
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

    game = get_uno_game(
        room
    )

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

def show_color_menu(
    chat_id
):

    buttons = [
        [
            {
                "id": (
                    f"{COLOR_PREFIX}"
                    f"{RED}"
                ),
                "text": "🔴 قرمز"
            },
            {
                "id": (
                    f"{COLOR_PREFIX}"
                    f"{GREEN}"
                ),
                "text": "🟢 سبز"
            }
        ],
        [
            {
                "id": (
                    f"{COLOR_PREFIX}"
                    f"{BLUE}"
                ),
                "text": "🔵 آبی"
            },
            {
                "id": (
                    f"{COLOR_PREFIX}"
                    f"{YELLOW}"
                ),
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

    winner = game.winner

    winner_name = get_player_name(
        winner
    )

    text = (
        "🏆 بازی UNO تمام شد! 🎉\n\n"
        f"🥇 برنده: {winner_name}\n\n"
        "🎴 تعداد کارت باقی‌مانده:\n"
    )

    for player in room.players:

        nickname = get_player_name(
            player
        )

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
# خروج از UNO
# ==========================================

def exit_uno(
    room,
    chat_id
):

    if chat_id not in room.players:

        send_message(
            chat_id,
            "❌ تو داخل این اتاق نیستی."
        )

        return

    nickname = get_player_name(
        chat_id
    )

    other_players = [
        player
        for player in room.players
        if player != chat_id
    ]

    # --------------------------------------
    # حذف کی‌پد بازی برای فرد خارج‌شده
    # --------------------------------------

    remove_keypad(
        chat_id,
        "🚪 از UNO خارج شدی."
    )

    # --------------------------------------
    # حذف بازی
    # --------------------------------------

    remove_uno_game(
        room
    )

    room.started = False

    # --------------------------------------
    # حذف اتاق
    # --------------------------------------

    from rooms.manager import delete_room

    delete_room(
        room.room_id
    )

    # --------------------------------------
    # اطلاع به بازیکنان دیگر
    # --------------------------------------

    for player in other_players:

        send_message(
            player,
            f"⚠️ {nickname} از اتاق UNO خارج شد."
        )

    # --------------------------------------
    # رفتن به کافه بازی
    # --------------------------------------

    from handlers.menu import room_menu

    room_menu(
        chat_id
    )


# ==========================================
# کنترل بازی
# ==========================================

def handle(
    room,
    chat_id,
    button_id
):

    game = get_uno_game(
        room
    )

    # ======================================
    # خروج
    # ======================================

    if button_id == EXIT_ID:

        exit_uno(
            room,
            chat_id
        )

        return

    # ======================================
    # اگر بازی هنوز شروع نشده
    # ======================================

    if game is None:

        if button_id == START_ID:

            start_game(
                room,
                chat_id
            )

        return

    # ======================================
    # شروع
    # ======================================

    if button_id == START_ID:

        start_game(
            room,
            chat_id
        )

        return

    # ======================================
    # بازی تمام شده
    # ======================================

    if game.finished:

        send_message(
            chat_id,
            "🏁 این بازی تمام شده است."
        )

        return

    # ======================================
    # انتخاب رنگ
    # ======================================

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

        render_all(
            room
        )

        return

    # ======================================
    # UNO
    # ======================================

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

        nickname = get_player_name(
            chat_id
        )

        # ----------------------------------
        # اطلاع به همه
        # ----------------------------------

        for player in room.players:

            send_message(
                player,
                f"🃏 {nickname} گفت UNO! 🔥\n"
                "🖐️ این بازیکن فقط ۱ کارت دارد!"
            )

        return

    # ======================================
    # Draw
    # ======================================

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
                "✅ این کارت قابل بازی است.\n"
                "اگر خواستی روی دکمه‌اش بزن."
            )

        else:

            send_message(
                chat_id,
                "🎴 کارت گرفتی:\n\n"
                f"{card.display()}\n\n"
                "❌ این کارت قابل بازی نیست.\n"
                "⏭️ نوبت به بازیکن بعدی رسید."
            )

        render_all(
            room
        )

        return

    # ======================================
    # کارت
    # ======================================

    if button_id.startswith(
        CARD_PREFIX
    ):

        try:

            index = int(
                button_id.replace(
                    CARD_PREFIX,
                    "",
                    1
                )
            )

        except ValueError:

            send_message(
                chat_id,
                "❌ کارت نامعتبر است."
            )

            return

        result = game.play_card(
            chat_id,
            index
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

            if card.card_type == WILD_DRAW_FOUR:

                next_player = game.next_player()

                next_name = get_player_name(
                    next_player
                )

                send_message(
                    next_player,
                    "🌈 +4 دریافت کردی!\n"
                    "🎴 چهار کارت به دستت اضافه شد."
                )

            show_color_menu(
                chat_id
            )

            return

        # ----------------------------------
        # سایر کارت‌ها
        # ----------------------------------

        render_all(
            room
        )

        return