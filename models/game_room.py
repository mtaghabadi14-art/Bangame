class GameRoom:

    def __init__(self, room_id, game, host, min_players, max_players):

        self.room_id = room_id

        self.game = game

        self.host = host

        self.players = [host]

        self.min_players = min_players

        self.max_players = max_players

        self.started = False

        self.data = {}