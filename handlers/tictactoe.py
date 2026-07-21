from rubika import (
    send_keypad,
    send_message
)

from games import tictactoe


def start(room):

    room.data["board"] = tictactoe.create_board()

    room.data["turn"] = room.players[0]

    update(room)



def board_buttons(board):

    buttons = []

    for row in range(3):

        line = []

        for col in range(3):

            line.append({
                "text": board[row][col],
                "id": f"{row}_{col}"
            })

        buttons.append(line)

    return buttons



def update(room):

    board = room.data["board"]

    keypad = board_buttons(board)

    keypad.append([
        {
            "text": "🚪 خروج",
            "id": "exit"
        }
    ])


    for player in room.players:

        if player == room.data["turn"]:

            text = "🎮 نوبت تو است"

        else:

            text = "⏳ منتظر حرکت حریف..."


        send_keypad(
            player,
            text,
            keypad
        )



def move(room, player, button_id):

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


    result = tictactoe.play(
        board,
        row,
        col
    )


    if result is False:

        send_message(
            player,
            "❌ این خانه پر است!"
        )

        return


    win = tictactoe.winner(board)


    if win:

        update(room)

        send_message(
            player,
            f"🎉 بازیکن {win} برنده شد!"
        )

        return



    if tictactoe.draw(board):

        update(room)

        send_message(
            player,
            "🤝 بازی مساوی شد!"
        )

        return



    if room.data["turn"] == room.players[0]:

        room.data["turn"] = room.players[1]

    else:

        room.data["turn"] = room.players[0]


    update(room)



def handle(room, player, data):

    button_id = data.get("button_id")


    if not button_id:

        return


    if button_id == "exit":

        send_message(
            player,
            "🚪 از بازی خارج شدی."
        )

        return


    move(
        room,
        player,
        button_id
    )