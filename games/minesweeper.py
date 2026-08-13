import random


# ==========================================
# تنظیمات بازی
# ==========================================

BOARD_SIZE = 5
MINE_COUNT = 5


# ==========================================
# ساخت صفحه
# ==========================================

def create_board():
    """
    ساخت یک صفحه 5×5 و قرار دادن مین‌ها
    """

    board = [
        [0 for _ in range(BOARD_SIZE)]
        for _ in range(BOARD_SIZE)
    ]

    positions = [
        (row, col)
        for row in range(BOARD_SIZE)
        for col in range(BOARD_SIZE)
    ]

    mines = random.sample(
        positions,
        MINE_COUNT
    )

    for row, col in mines:

        board[row][col] = -1

    # محاسبه تعداد مین‌های اطراف
    for row in range(BOARD_SIZE):

        for col in range(BOARD_SIZE):

            if board[row][col] == -1:
                continue

            count = 0

            for dr in (-1, 0, 1):

                for dc in (-1, 0, 1):

                    if dr == 0 and dc == 0:
                        continue

                    nr = row + dr
                    nc = col + dc

                    if (
                        0 <= nr < BOARD_SIZE
                        and 0 <= nc < BOARD_SIZE
                        and board[nr][nc] == -1
                    ):

                        count += 1

            board[row][col] = count

    return board


# ==========================================
# ساخت بازی
# ==========================================

def create_game():

    board = create_board()

    return {
        "board": board,

        # خانه‌هایی که باز شده‌اند
        "revealed": set(),

        # خانه‌هایی که پرچم دارند
        "flags": set(),

        "finished": False,

        "won": False
    }


# ==========================================
# بررسی مختصات
# ==========================================

def valid_position(row, col):

    return (
        0 <= row < BOARD_SIZE
        and 0 <= col < BOARD_SIZE
    )


# ==========================================
# گرفتن مقدار یک خانه
# ==========================================

def get_cell(game, row, col):

    if not valid_position(row, col):

        return None

    return game["board"][row][col]


# ==========================================
# باز کردن خانه
# ==========================================

def reveal_cell(game, row, col):

    if game["finished"]:

        return {
            "success": False,
            "reason": "finished"
        }

    if not valid_position(row, col):

        return {
            "success": False,
            "reason": "invalid"
        }

    position = (row, col)

    # خانه قبلاً باز شده
    if position in game["revealed"]:

        return {
            "success": False,
            "reason": "already_revealed"
        }

    # خانه پرچم دارد
    if position in game["flags"]:

        return {
            "success": False,
            "reason": "flagged"
        }

    # ======================================
    # برخورد با مین
    # ======================================

    if game["board"][row][col] == -1:

        game["revealed"].add(position)

        game["finished"] = True
        game["won"] = False

        return {
            "success": True,
            "mine": True,
            "finished": True,
            "won": False
        }

    # ======================================
    # خانه امن
    # ======================================

    reveal_empty_area(
        game,
        row,
        col
    )

    # بررسی برد
    if check_win(game):

        game["finished"] = True
        game["won"] = True

        return {
            "success": True,
            "mine": False,
            "finished": True,
            "won": True
        }

    return {
        "success": True,
        "mine": False,
        "finished": False,
        "won": False
    }


# ==========================================
# باز کردن خودکار خانه‌های صفر
# ==========================================

def reveal_empty_area(game, row, col):

    queue = [(row, col)]
    visited = set()

    while queue:

        current_row, current_col = queue.pop(0)

        position = (
            current_row,
            current_col
        )

        if position in visited:
            continue

        visited.add(position)

        if not valid_position(
            current_row,
            current_col
        ):
            continue

        if position in game["flags"]:
            continue

        if game["board"][
            current_row
        ][
            current_col
        ] == -1:

            continue

        game["revealed"].add(position)

        # اگر عدد صفر نیست،
        # دیگر اطرافش را باز نمی‌کنیم
        if game["board"][
            current_row
        ][
            current_col
        ] != 0:

            continue

        # اضافه کردن خانه‌های اطراف
        for dr in (-1, 0, 1):

            for dc in (-1, 0, 1):

                if dr == 0 and dc == 0:
                    continue

                nr = current_row + dr
                nc = current_col + dc

                if valid_position(nr, nc):

                    neighbour = (
                        nr,
                        nc
                    )

                    if neighbour not in visited:

                        queue.append(
                            neighbour
                        )


# ==========================================
# گذاشتن / برداشتن پرچم
# ==========================================

def toggle_flag(game, row, col):

    if game["finished"]:

        return {
            "success": False,
            "reason": "finished"
        }

    if not valid_position(row, col):

        return {
            "success": False,
            "reason": "invalid"
        }

    position = (
        row,
        col
    )

    # خانه باز شده را نمی‌توان پرچم زد
    if position in game["revealed"]:

        return {
            "success": False,
            "reason": "already_revealed"
        }

    # اگر پرچم دارد، بردار
    if position in game["flags"]:

        game["flags"].remove(position)

        return {
            "success": True,
            "flagged": False
        }

    # پرچم جدید
    game["flags"].add(position)

    return {
        "success": True,
        "flagged": True
    }


# ==========================================
# بررسی برد
# ==========================================

def check_win(game):

    total_cells = (
        BOARD_SIZE * BOARD_SIZE
    )

    safe_cells = (
        total_cells - MINE_COUNT
    )

    return len(
        game["revealed"]
    ) >= safe_cells


# ==========================================
# تعداد مین‌های باقی‌مانده
# ==========================================

def get_remaining_mines(game):

    return (
        MINE_COUNT
        - len(game["flags"])
    )


# ==========================================
# تعداد پرچم‌ها
# ==========================================

def get_flag_count(game):

    return len(
        game["flags"]
    )


# ==========================================
# وضعیت بازی
# ==========================================

def is_finished(game):

    return game.get(
        "finished",
        False
    )


# ==========================================
# برنده شدن
# ==========================================

def is_won(game):

    return game.get(
        "won",
        False
    )