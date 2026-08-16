import random

from .cards import (
    Card,
    COLORS,
    NUMBER,
    SKIP,
    REVERSE,
    DRAW_TWO,
    WILD,
    WILD_DRAW_FOUR
)


class UnoDeck:

    def __init__(self):

        self.cards = []

        self._build()

        self.shuffle()

    # ==========================================
    # ساخت Deck
    # ==========================================

    def _build(self):

        for color in COLORS:

            # صفر
            self.cards.append(
                Card(
                    color,
                    "0",
                    NUMBER
                )
            )

            # 1 تا 9
            for number in range(1, 10):

                self.cards.append(
                    Card(
                        color,
                        str(number),
                        NUMBER
                    )
                )

                self.cards.append(
                    Card(
                        color,
                        str(number),
                        NUMBER
                    )
                )

            # Skip
            for _ in range(2):

                self.cards.append(
                    Card(
                        color,
                        "skip",
                        SKIP
                    )
                )

            # Reverse
            for _ in range(2):

                self.cards.append(
                    Card(
                        color,
                        "reverse",
                        REVERSE
                    )
                )

            # +2
            for _ in range(2):

                self.cards.append(
                    Card(
                        color,
                        "+2",
                        DRAW_TWO
                    )
                )

        # Wild
        for _ in range(4):

            self.cards.append(
                Card(
                    None,
                    "wild",
                    WILD
                )
            )

        # Wild +4
        for _ in range(4):

            self.cards.append(
                Card(
                    None,
                    "+4",
                    WILD_DRAW_FOUR
                )
            )

    # ==========================================
    # Shuffle
    # ==========================================

    def shuffle(self):

        random.shuffle(
            self.cards
        )

    # ==========================================
    # Draw
    # ==========================================

    def draw(self):

        if not self.cards:
            return None

        return self.cards.pop()

    # ==========================================
    # تعداد کارت
    # ==========================================

    def count(self):

        return len(self.cards)