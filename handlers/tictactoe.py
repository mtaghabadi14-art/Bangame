from rubika import (
    send_keypad,
    send_message,
    remove_keypad
)

from handlers.menu import main_menu

from games import tictactoe

from rooms.manager import (
    leave_room,
    delete_room
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
                "text": "🚪 خروج",
                "id": "exit"
            }
        ]
    )


    return buttons



# ==========================================
# آپدیت صفحه
# ==========================================

def update(room):

    keypad = board_buttons(
        room.data["board"]
    )


    for player in room.players:

        if not room.started:

            text = "🏁 بازی تمام شده است."

        elif player == room.data["turn"]:

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

    update(room)

    # حذف اتاق
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



    row, col = button_id.split("_")

    row = int(row)
    col = int(col)


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



    win = tictactoe.winner(board)



    if win:


        winner_player = None


        if win == tictactoe.X:

            winner_player = room.players[0]

        else:

            winner_player = room.players[1]



        for p in room.players:


            if p == winner_player:

                send_message(
                    p,
                    "🏆 تبریک! تو برنده شدی."
                )

            else:

                send_message(
                    p,
                    "😢 بازی تمام شد.\nحریفت برنده شد."
                )



        end(room)

        return




    if tictactoe.draw(board):


        for p in room.players:

            send_message(
                p,
                "🤝 بازی مساوی شد."
            )


        end(room)

        return




    # تعویض نوبت

    if player == room.players[0]:

        room.data["turn"] = room.players[1]

    else:

        room.data["turn"] = room.players[0]


    update(room)



# ==========================================
# مدیریت کلیک‌ها
# ==========================================

def handle(room, player, data):


    button_id = data.get("button_id")


    if not button_id:

        return



    # -------------------------
    # خروج
    # -------------------------

    if button_id == "exit":


        other_players = [
            p for p in room.players
            if p != player
        ]



        leave_room(player)



        remove_keypad(
            player,
            "🚪 از بازی خارج شدی."
        )


        main_menu(player)



        for p in other_players:


            send_message(
                p,
                "⚠️ حریف از بازی خارج شد."
            )


            remove_keypad(
                p,
                "🏁 بازی تمام شد."
            )


            main_menu(p)


            leave_room(p)



        return




    # -------------------------
    # حرکت
    # -------------------------

    move(
        room,
        player,
        button_id
    )