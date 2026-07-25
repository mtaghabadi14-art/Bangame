from rubika import (
    send_keypad,
    send_message,
    remove_keypad
)

from handlers.menu import room_menu

from games import tictactoe

from rooms.manager import (
    leave_room,
    delete_room,
    get_player_room
)


# ==========================================
# شروع بازی
# ==========================================

def start(room):

    room.started = True

    room.data["board"] = tictactoe.create_board()

    room.data["turn"] = room.players[0]

    update(room)


# ==========================================
# ساخت دکمه‌ها
# ==========================================

def board_buttons(board):

    buttons = []

    for row in range(3):

        line = []

        for col in range(3):

            line.append(
                {
                    "text": board[row][col],
                    "id": f"{row}_{col}"
                }
            )

        buttons.append(line)


    buttons.append(
        [
            {
                "text": "🚪 خروج از بازی",
                "id": "exit"
            }
        ]
    )

    return buttons


# ==========================================
# آپدیت صفحه
# ==========================================

def update(room):

    if not room.started:
        return

    keypad = board_buttons(
        room.data["board"]
    )


    for player in room.players:

        if player == room.data["turn"]:

            text = "🎮 نوبت تو است."

        else:

            text = "⏳ منتظر حرکت حریف..."


        send_keypad(
            player,
            text,
            keypad
        )


# ==========================================
# پایان بازی
# ==========================================

def end(room):

    room.started = False

    room.data.clear()

    delete_room(
        room.room_id
    )
    # ==========================================
# ثبت حرکت
# ==========================================

def move(room, player, button_id):

    if not room.started:

        send_message(
            player,
            "🏁 این بازی تمام شده است."
        )

        return


    if room.data["turn"] != player:

        send_message(
            player,
            "⏳ الان نوبت تو نیست!"
        )

        return


    try:

        row, col = button_id.split("_")

        row = int(row)
        col = int(col)

    except:

        return


    board = room.data["board"]


    if not tictactoe.play(
        board,
        row,
        col
    ):

        send_message(
            player,
            "❌ این خانه قبلاً انتخاب شده است."
        )

        return



    # -------------------------
    # بررسی برنده
    # -------------------------

    win = tictactoe.winner(board)


    if win:


        winner_player = (
            room.players[0]
            if win == tictactoe.X
            else room.players[1]
        )


        for p in room.players:

            remove_keypad(
                p,
                "🏁 بازی تمام شد."
            )


            if p == winner_player:

                send_message(
                    p,
                    "🏆 تبریک! تو برنده شدی."
                )

            else:

                send_message(
                    p,
                    "😢 حریفت برنده شد."
                )


            room_menu(p)



        end(room)

        return



    # -------------------------
    # بررسی مساوی
    # -------------------------

    if tictactoe.draw(board):


        for p in room.players:


            remove_keypad(
                p,
                "🏁 بازی تمام شد."
            )


            send_message(
                p,
                "🤝 بازی مساوی شد."
            )


            room_menu(p)



        end(room)

        return



    # -------------------------
    # تغییر نوبت
    # -------------------------

    if player == room.players[0]:

        room.data["turn"] = room.players[1]

    else:

        room.data["turn"] = room.players[0]


    update(room)




# ==========================================
# مدیریت کلیک دکمه‌ها
# ==========================================

def handle(room, player, data):

    button_id = data.get("button_id")


    if not button_id:

        return



    # -------------------------
    # خروج از بازی
    # -------------------------

    if button_id == "exit":


        other_players = [
            p for p in room.players
            if p != player
        ]


        room.started = False

        room.data.clear()



        leave_room(player)


        remove_keypad(
            player,
            "🚪 از بازی خارج شدی."
        )


        send_message(
            player,
            "🚪 از دوز خارج شدی."
        )


        room_menu(player)



        for p in other_players:


            send_message(
                p,
                "⚠️ حریف از بازی خارج شد."
            )


            remove_keypad(
                p,
                "🏁 بازی پایان یافت."
            )


            room_menu(p)


            leave_room(p)



        delete_room(
            room.room_id
        )


        return



    # -------------------------
    # حرکت دوز
    # -------------------------

    move(
        room,
        player,
        button_id
    )