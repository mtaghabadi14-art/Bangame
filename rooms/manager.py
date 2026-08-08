import random
import string

from rooms.game_room import GameRoom


# -----------------------------
# حافظه اتاق‌ها
# -----------------------------

rooms = {}

# player_id -> room_id
player_rooms = {}


# -----------------------------
# ساخت کد اتاق
# -----------------------------

def generate_room_code(length=6):

    while True:

        code = "".join(
            random.choice(string.ascii_uppercase + string.digits)
            for _ in range(length)
        )

        if code not in rooms:
            return code


# -----------------------------
# ساخت اتاق
# -----------------------------

def create_room(
    game,
    host,
    min_players,
    max_players
):

    if host in player_rooms:
        return None

    room_id = generate_room_code()

    room = GameRoom(
        room_id,
        game,
        host,
        min_players,
        max_players
    )

    rooms[room_id] = room
    player_rooms[host] = room_id

    return room


# -----------------------------
# گرفتن اتاق
# -----------------------------

def get_room(room_id):

    return rooms.get(room_id)


# -----------------------------
# اتاق بازیکن
# -----------------------------

def get_player_room(player):

    room_id = player_rooms.get(player)

    if room_id is None:
        return None

    return rooms.get(room_id)
# -----------------------------
# ورود به اتاق
# -----------------------------

def join_room(room_id, player):

    room = rooms.get(room_id)

    if room is None:
        return None

    if player in player_rooms:
        return None

    if len(room.players) >= room.max_players:
        return None

    room.players.append(player)

    player_rooms[player] = room_id

    return room


# -----------------------------
# خروج از اتاق
# -----------------------------

def leave_room(player):

    room = get_player_room(player)

    if room is None:
        return False

    if player in room.players:
        room.players.remove(player)

    player_rooms.pop(player, None)

    # اگر میزبان خارج شد
    if player == room.host:

        for p in room.players:
            player_rooms.pop(p, None)

        rooms.pop(room.room_id, None)

        return True

    # اگر اتاق خالی شد
    if len(room.players) == 0:

        rooms.pop(room.room_id, None)

    return True


# -----------------------------
# آماده بودن بازی
# -----------------------------

def can_start(room):

    return len(room.players) >= room.min_players


# -----------------------------
# تعداد بازیکنان
# -----------------------------

def player_count(room):

    return len(room.players)


# -----------------------------
# لیست بازیکنان
# -----------------------------

def get_players(room):

    return room.players.copy()


# -----------------------------
# حذف اتاق
# -----------------------------

def delete_room(room_id):

    room = rooms.get(room_id)

    if room is None:
        return False


    print("DELETE ROOM:", room_id)


    # پاک کردن بازیکنان از player_rooms
    for player in room.players:

        print("REMOVE PLAYER:", player)

        player_rooms.pop(
            player,
            None
        )


    # حذف خود اتاق
    rooms.pop(
        room_id,
        None
    )


    print("ROOMS AFTER DELETE:", rooms)
    print("PLAYERS AFTER DELETE:", player_rooms)


    return True


# -----------------------------
# شروع بازی
# -----------------------------

def start_game(room):

    if not can_start(room):
        return False

    room.started = True

    return True


# -----------------------------
# پایان بازی
# -----------------------------

def end_game(room):

    room.started = False


# -----------------------------
# همه اتاق‌ها
# -----------------------------

def get_rooms():

    return rooms


# -----------------------------
# تعداد اتاق‌ها
# -----------------------------

def room_count():

    return len(rooms)
