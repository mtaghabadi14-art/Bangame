import random


# ==========================================
# Difficulty
# ==========================================

DIFFICULTIES = {
    "easy": {
        "name": "🟢 آسان",
        "size": 5,
        "mines": 5
    },

    "medium": {
        "name": "🟡 متوسط",
        "size": 8,
        "mines": 12
    },

    "hard": {
        "name": "🔴 سخت",
        "size": 9,
        "mines": 20
    }
}


# ==========================================
# Neighbors
# ==========================================

def get_neighbors(row, col, size):

    neighbors = []

    for dr in (-1, 0, 1):

        for dc in (-1, 0, 1):

            if dr == 0 and dc == 0:
                continue

            nr = row + dr
            nc = col + dc

            if (
                0 <= nr < size
                and 0 <= nc < size
            ):
                neighbors.append(
                    (nr, nc)
                )

    return neighbors


# ==========================================
# First-click safe area
# ==========================================

def get_safe_zone(row, col, size):

    safe = {
        (row, col)
    }

    for position in get_neighbors(
        row,
        col,
        size
    ):
        safe.add(position)

    return safe


# ==========================================
# Create empty board
# ==========================================

def create_empty_board(size):

    return [
        [0 for _ in range(size)]
        for _ in range(size)
    ]


# ==========================================
# Place mines AFTER first click
# ==========================================

def place_mines(
    game,
    first_row,
    first_col
):

    size = game["size"]
    mine_count = game["mine_count"]

    safe_zone = get_safe_zone(
        first_row,
        first_col,
        size
    )

    all_cells = [
        (r, c)
        for r in range(size)
        for c in range(size)
        if (r, c) not in safe_zone
    ]

    # در صورت نیاز، اگر تعداد خانه‌های
    # امن زیاد بود، از خود اولین خانه
    # فاصله می‌گیریم ولی همیشه اولین خانه امن است.
    if len(all_cells) < mine_count:

        all_cells = [
            (r, c)
            for r in range(size)
            for c in range(size)
            if (r, c) != (first_row, first_col)
        ]

    mines = set(
        random.sample(
            all_cells,
            mine_count
        )
    )

    game["mines"] = mines

    # ساخت اعداد
    for row in range(size):

        for col in range(size):

            if (row, col) in mines:

                game["board"][row][col] = -1

                continue

            count = 0

            for nr, nc in get_neighbors(
                row,
                col,
                size
            ):

                if (nr, nc) in mines:
                    count += 1

            game["board"][row][col] = count

    game["generated"] = True


# ==========================================
# Create Game
# ==========================================

def create_game(
    difficulty="easy"
):

    config = DIFFICULTIES.get(
        difficulty,
        DIFFICULTIES["easy"]
    )

    size = config["size"]
    mine_count = config["mines"]

    return {
        "difficulty": difficulty,
        "difficulty_name": config["name"],

        "size": size,
        "mine_count": mine_count,

        "board": create_empty_board(size),

        "mines": set(),

        "revealed": set(),
        "flags": set(),

        "generated": False,

        "finished": False,
        "won": False,

        "mode": "reveal"
    }


# ==========================================
# Reveal empty area
# ==========================================

def flood_reveal(
    game,
    start_row,
    start_col
):

    size = game["size"]

    queue = [
        (start_row, start_col)
    ]

    visited = set()

    while queue:

        row, col = queue.pop(0)

        if (row, col) in visited:
            continue

        visited.add(
            (row, col)
        )

        if (row, col) in game["flags"]:
            continue

        if (row, col) in game["mines"]:
            continue

        game["revealed"].add(
            (row, col)
        )

        value = game["board"][row][col]

        # اگر صفر بود اطرافش هم باز شود
        if value == 0:

            for neighbor in get_neighbors(
                row,
                col,
                size
            ):

                if neighbor not in visited:

                    if neighbor not in game["flags"]:

                        queue.append(
                            neighbor
                        )


# ==========================================
# Check Win
# ==========================================

def check_win(game):

    total_cells = (
        game["size"] *
        game["size"]
    )

    safe_cells = (
        total_cells -
        game["mine_count"]
    )

    if len(game["revealed"]) >= safe_cells:

        game["finished"] = True
        game["won"] = True

        return True

    return False


# ==========================================
# Reveal Cell
# ==========================================

def reveal_cell(
    game,
    row,
    col
):

    size = game["size"]

    if not (
        0 <= row < size
        and 0 <= col < size
    ):

        return {
            "success": False,
            "reason": "invalid"
        }

    if game["finished"]:

        return {
            "success": False,
            "reason": "finished"
        }

    position = (
        row,
        col
    )

    if position in game["revealed"]:

        return {
            "success": False,
            "reason": "already_revealed"
        }

    if position in game["flags"]:

        return {
            "success": False,
            "reason": "flagged"
        }

    # ======================================
    # اولین کلیک
    # ======================================

    if not game["generated"]:

        place_mines(
            game,
            row,
            col
        )

    # ======================================
    # مین
    # ======================================

    if position in game["mines"]:

        game["revealed"].add(
            position
        )

        game["finished"] = True
        game["won"] = False

        # نمایش تمام مین‌ها
        for mine in game["mines"]:

            game["revealed"].add(
                mine
            )

        return {
            "success": True,
            "mine": True
        }

    # ======================================
    # خانه امن
    # ======================================

    flood_reveal(
        game,
        row,
        col
    )

    check_win(game)

    return {
        "success": True,
        "mine": False
    }


# ==========================================
# Toggle Flag
# ==========================================

def toggle_flag(
    game,
    row,
    col
):

    size = game["size"]

    if not (
        0 <= row < size
        and 0 <= col < size
    ):

        return {
            "success": False,
            "reason": "invalid"
        }

    if game["finished"]:

        return {
            "success": False,
            "reason": "finished"
        }

    position = (
        row,
        col
    )

    if position in game["revealed"]:

        return {
            "success": False,
            "reason": "already_revealed"
        }

    if position in game["flags"]:

        game["flags"].remove(
            position
        )

        return {
            "success": True,
            "flagged": False
        }

    if len(game["flags"]) >= game["mine_count"]:

        return {
            "success": False,
            "reason": "too_many_flags"
        }

    game["flags"].add(
        position
    )

    return {
        "success": True,
        "flagged": True
    }


# ==========================================
# Finished
# ==========================================

def is_finished(game):

    return game["finished"]


# ==========================================
# Won
# ==========================================

def is_won(game):

    return game["won"]


# ==========================================
# Remaining Mines
# ==========================================

def get_remaining_mines(game):

    return max(
        0,
        game["mine_count"] -
        len(game["flags"])
    )


# ==========================================
# Flag Count
# ==========================================

def get_flag_count(game):

    return len(
        game["flags"]
    )


# ==========================================
# Board Size
# ==========================================

def get_board_size(game):

    return game["size"]