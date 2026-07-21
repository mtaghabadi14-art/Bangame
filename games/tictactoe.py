EMPTY = "⬜"

X = "❌"

O = "⭕"


def create_board():

    return [
        [EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY]
    ]


def current_player(board):

    x = 0
    o = 0

    for row in board:

        for cell in row:

            if cell == X:
                x += 1

            elif cell == O:
                o += 1


    if x <= o:
        return X

    return O



def play(board, row, col):

    if board[row][col] != EMPTY:

        return False


    board[row][col] = current_player(board)

    return True



def winner(board):

    lines = []

    lines.extend(board)


    lines.append([
        board[0][0],
        board[1][0],
        board[2][0]
    ])

    lines.append([
        board[0][1],
        board[1][1],
        board[2][1]
    ])

    lines.append([
        board[0][2],
        board[1][2],
        board[2][2]
    ])


    lines.append([
        board[0][0],
        board[1][1],
        board[2][2]
    ])


    lines.append([
        board[0][2],
        board[1][1],
        board[2][0]
    ])


    for line in lines:

        if line[0] != EMPTY and line[0] == line[1] == line[2]:

            return line[0]


    return None



def draw(board):

    for row in board:

        for cell in row:

            if cell == EMPTY:

                return False


    return winner(board) is None