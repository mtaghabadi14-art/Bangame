from .game import UnoGame


def get_uno_game(room):

    return room.data.get("uno")


def create_uno_game(room):

    game = UnoGame(
        room.players
    )

    room.data["uno"] = game

    return game


def remove_uno_game(room):

    room.data.pop(
        "uno",
        None
    )