from .game import PuzzleGame


# ==========================================
# گرفتن بازی پازل
# ==========================================

def get_puzzle_game(room):

    return room.data.get("puzzle_online")


# ==========================================
# ساخت بازی پازل
# ==========================================

def create_puzzle_game(room):

    game = PuzzleGame(
        room.players
    )

    room.data["puzzle_online"] = game

    return game


# ==========================================
# حذف بازی پازل
# ==========================================

def remove_puzzle_game(room):

    room.data.pop(
        "puzzle_online",
        None
    )