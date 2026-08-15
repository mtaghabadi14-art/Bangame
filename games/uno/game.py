from .deck import UnoDeck

from .cards import (
    COLORS,
    NUMBER,
    SKIP,
    REVERSE,
    DRAW_TWO,
    WILD,
    WILD_DRAW_FOUR,
    card_matches
)


class UnoGame:

    def __init__(self, players):

        self.players = players.copy()

        self.deck = UnoDeck()

        self.discard = []

        self.hands = {
            player: []
            for player in self.players
        }

        self.current_player_index = 0

        self.direction = 1

        self.current_color = None

        self.started = False

        self.finished = False

        self.winner = None

        self.uno_called = set()

        self.last_draw = {}

        self.pending_color = False

        self.pending_color_player = None


    # ==========================================
    # شروع بازی
    # ==========================================

    def start(self):

        if len(self.players) < 2:
            return False

        if len(self.players) > 4:
            return False

        self.started = True
        self.finished = False
        self.winner = None

        # --------------------------------------
        # 7 کارت برای هر بازیکن
        # --------------------------------------

        for _ in range(7):

            for player in self.players:

                card = self._draw_one()

                if card is None:
                    return False

                self.hands[player].append(card)

        # --------------------------------------
        # کارت اول زمین
        # --------------------------------------

        while True:

            card = self._draw_one()

            if card is None:
                return False

            # شروع با +4 ممنوع
            if card.card_type == WILD_DRAW_FOUR:

                self.deck.cards.insert(
                    0,
                    card
                )

                self.deck.shuffle()

                continue

            self.discard.append(card)

            if card.card_type == WILD:

                self.current_color = None

            else:

                self.current_color = card.color

            break

        return True


    # ==========================================
    # بازیکن فعلی
    # ==========================================

    def current_player(self):

        if not self.players:
            return None

        return self.players[
            self.current_player_index
        ]


    # ==========================================
    # کارت روی زمین
    # ==========================================

    def top_card(self):

        if not self.discard:
            return None

        return self.discard[-1]


    # ==========================================
    # دست بازیکن
    # ==========================================

    def hand(self, player):

        return self.hands.get(
            player,
            []
        )


    # ==========================================
    # پیدا کردن کارت با ID
    # ==========================================

    def find_card_index(
        self,
        player,
        card_id
    ):

        hand = self.hand(player)

        for index, card in enumerate(hand):

            if card.card_id == card_id:

                return index

        return None


    # ==========================================
    # بررسی کارت
    # ==========================================

    def can_play(
        self,
        player,
        card_index
    ):

        if self.finished:

            return (
                False,
                "🏁 بازی تمام شده است."
            )

        if self.pending_color:

            return (
                False,
                "🎨 ابتدا رنگ کارت Wild را انتخاب کن."
            )

        if player != self.current_player():

            return (
                False,
                "⏳ هنوز نوبت تو نیست."
            )

        hand = self.hand(player)

        if (
            card_index < 0
            or card_index >= len(hand)
        ):

            return (
                False,
                "❌ کارت نامعتبر است."
            )

        card = hand[card_index]

        top = self.top_card()

        if top is None:

            return True, None

        # --------------------------------------
        # +4
        # --------------------------------------

        if card.card_type == WILD_DRAW_FOUR:

            for other in hand:

                if other.card_type in (
                    WILD,
                    WILD_DRAW_FOUR
                ):
                    continue

                if other.color == self.current_color:

                    return (
                        False,
                        "❌ چون یک کارت هم‌رنگ قابل بازی داری، "
                        "فعلاً نمی‌توانی 🌈 +4 بگذاری."
                    )

            return True, None

        # --------------------------------------
        # Wild
        # --------------------------------------

        if card.card_type == WILD:

            return True, None

        # --------------------------------------
        # کارت عادی
        # --------------------------------------

        if card_matches(
            card,
            top,
            self.current_color
        ):

            return True, None

        return (
            False,
            "❌ این کارت قابل بازی نیست!\n\n"
            "باید رنگ یا عدد/نوع کارت "
            "با کارت روی زمین مطابقت داشته باشد."
        )


    # ==========================================
    # بازی کارت با ID
    # ==========================================

    def play_card_by_id(
        self,
        player,
        card_id
    ):

        index = self.find_card_index(
            player,
            card_id
        )

        if index is None:

            return {
                "success": False,
                "message": "❌ این کارت دیگر در دستت نیست."
            }

        return self.play_card(
            player,
            index
        )


    # ==========================================
    # بازی کارت
    # ==========================================

    def play_card(
        self,
        player,
        card_index
    ):

        valid, error = self.can_play(
            player,
            card_index
        )

        if not valid:

            return {
                "success": False,
                "message": error
            }

        card = self.hands[player].pop(
            card_index
        )

        self.discard.append(
            card
        )

        # --------------------------------------
        # بروزرسانی رنگ فعلی
        # --------------------------------------

        if card.card_type not in (
            WILD,
            WILD_DRAW_FOUR
        ):
            self.current_color = card.color

        self.last_draw.pop(
            player,
            None
        )

        # --------------------------------------
        # اگر به یک کارت رسید
        # --------------------------------------

        if len(self.hands[player]) == 1:

            self.uno_called.discard(player)

        # --------------------------------------
        # برنده
        # --------------------------------------

        if len(self.hands[player]) == 0:

            self.finished = True
            self.started = False
            self.winner = player

            return {
                "success": True,
                "card": card,
                "winner": player,
                "effect": "win"
            }

        # --------------------------------------
        # Wild
        # --------------------------------------

        if card.card_type in (
            WILD,
            WILD_DRAW_FOUR
        ):

            self.pending_color = True

            self.pending_color_player = player

            if card.card_type == WILD_DRAW_FOUR:

                next_player = self.next_player()

                self.draw_cards(
                    next_player,
                    4
                )

            return {
                "success": True,
                "card": card,
                "effect": "choose_color"
            }

        # --------------------------------------
        # کارت‌های دیگر
        # --------------------------------------

        effect = self.apply_card_effect(
            card
        )

        return {
            "success": True,
            "card": card,
            "effect": effect
        }


    # ==========================================
    # اعمال اثر کارت
    # ==========================================

    def apply_card_effect(
        self,
        card
    ):

        if card.card_type == REVERSE:

            self.direction *= -1

            if len(self.players) == 2:

                self.advance_turn()
                self.advance_turn()

            else:

                self.advance_turn()

            return "reverse"

        if card.card_type == SKIP:

            self.advance_turn()
            self.advance_turn()

            return "skip"

        if card.card_type == DRAW_TWO:

            next_player = self.next_player()

            self.draw_cards(
                next_player,
                2
            )

            self.advance_turn()

            return "draw_two"

        self.advance_turn()

        return "normal"


    # ==========================================
    # انتخاب رنگ
    # ==========================================

    def choose_color(
        self,
        player,
        color
    ):

        if color not in COLORS:

            return {
                "success": False,
                "message": "❌ رنگ نامعتبر است."
            }

        if not self.pending_color:

            return {
                "success": False,
                "message": "❌ الان انتخاب رنگ لازم نیست."
            }

        if player != self.pending_color_player:

            return {
                "success": False,
                "message": (
                    "❌ فقط بازیکنی که Wild گذاشته "
                    "می‌تواند رنگ را انتخاب کند."
                )
            }

        self.current_color = color

        self.pending_color = False

        self.pending_color_player = None

        self.advance_turn()

        return {
            "success": True,
            "color": color
        }


    # ==========================================
    # نفر بعدی
    # ==========================================

    def next_player(self):

        if not self.players:
            return None

        index = (
            self.current_player_index
            + self.direction
        ) % len(self.players)

        return self.players[index]


    # ==========================================
    # جلو بردن نوبت
    # ==========================================

    def advance_turn(self):

        if not self.players:
            return

        self.current_player_index = (
            self.current_player_index
            + self.direction
        ) % len(self.players)


    # ==========================================
    # Draw
    # ==========================================

    def draw_cards(
        self,
        player,
        count=1
    ):

        drawn = []

        for _ in range(count):

            card = self._draw_one()

            if card is None:
                break

            self.hands[player].append(card)

            drawn.append(card)

        self.last_draw[player] = drawn

        return drawn


    # ==========================================
    # Draw برای بازیکن
    # ==========================================

    def draw_for_player(
        self,
        player
    ):

        if self.finished:

            return {
                "success": False,
                "message": "🏁 بازی تمام شده است."
            }

        if self.pending_color:

            return {
                "success": False,
                "message": "🎨 ابتدا رنگ Wild را انتخاب کن."
            }

        if player != self.current_player():

            return {
                "success": False,
                "message": "⏳ هنوز نوبت تو نیست."
            }

        cards = self.draw_cards(
            player,
            1
        )

        if not cards:

            return {
                "success": False,
                "message": "❌ کارت دیگری وجود ندارد."
            }

        card = cards[0]

        playable = card_matches(
            card,
            self.top_card(),
            self.current_color
        )

        if not playable:

            self.advance_turn()

        return {
            "success": True,
            "card": card,
            "playable": playable
        }


    # ==========================================
    # Draw از Deck
    # ==========================================

    def _draw_one(self):

        card = self.deck.draw()

        if card is not None:

            return card

        self._rebuild_deck()

        return self.deck.draw()


    # ==========================================
    # ساخت دوباره Deck
    # ==========================================

    def _rebuild_deck(self):

        if len(self.discard) <= 1:
            return

        top = self.discard[-1]

        old_cards = self.discard[:-1]

        self.discard = [top]

        self.deck.cards.extend(
            old_cards
        )

        self.deck.shuffle()


    # ==========================================
    # UNO
    # ==========================================

    def call_uno(
        self,
        player
    ):

        hand = self.hand(player)

        if len(hand) != 1:

            return {
                "success": False,
                "message": "❌ الان موقع گفتن UNO نیست."
            }

        self.uno_called.add(player)

        return {
            "success": True
        }


    # ==========================================
    # بررسی UNO
    # ==========================================

    def has_called_uno(
        self,
        player
    ):

        return player in self.uno_called


    # ==========================================
    # وضعیت بازی
    # ==========================================

    def status(self):

        return {
            "current_player": self.current_player(),
            "current_color": self.current_color,
            "top_card": self.top_card(),
            "direction": self.direction,
            "deck_count": self.deck.count(),
            "finished": self.finished,
            "winner": self.winner,
            "pending_color": self.pending_color
        }