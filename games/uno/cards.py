from dataclasses import dataclass
import uuid


# ==========================================
# UNO Colors
# ==========================================

RED = "red"
GREEN = "green"
BLUE = "blue"
YELLOW = "yellow"

COLORS = (
    RED,
    GREEN,
    BLUE,
    YELLOW
)

COLOR_EMOJIS = {
    RED: "🔴",
    GREEN: "🟢",
    BLUE: "🔵",
    YELLOW: "🟡"
}

COLOR_NAMES = {
    RED: "قرمز",
    GREEN: "سبز",
    BLUE: "آبی",
    YELLOW: "زرد"
}


# ==========================================
# Card Types
# ==========================================

NUMBER = "number"
SKIP = "skip"
REVERSE = "reverse"
DRAW_TWO = "draw_two"
WILD = "wild"
WILD_DRAW_FOUR = "wild_draw_four"


# ==========================================
# Card
# ==========================================

@dataclass
class Card:

    color: str | None
    value: str
    card_type: str

    # شناسه یکتا برای هر کارت
    card_id: str = ""

    def __post_init__(self):

        if not self.card_id:

            self.card_id = uuid.uuid4().hex[:10]

    # ==========================================
    # نمایش کارت
    # ==========================================

    def display(self):

        if self.card_type == NUMBER:

            return (
                f"{COLOR_EMOJIS[self.color]} "
                f"{self.value}"
            )

        if self.card_type == SKIP:

            return (
                f"{COLOR_EMOJIS[self.color]} 🚫"
            )

        if self.card_type == REVERSE:

            return (
                f"{COLOR_EMOJIS[self.color]} 🔄"
            )

        if self.card_type == DRAW_TWO:

            return (
                f"{COLOR_EMOJIS[self.color]} +2"
            )

        if self.card_type == WILD:

            return "🌈 Wild"

        if self.card_type == WILD_DRAW_FOUR:

            return "🌈 +4"

        return "🃏"


# ==========================================
# بررسی قابل بازی بودن کارت
# ==========================================

def card_matches(
    card,
    top_card,
    current_color
):

    if top_card is None:

        return True

    # Wild ها همیشه قابل بازی هستند
    if card.card_type in (
        WILD,
        WILD_DRAW_FOUR
    ):

        return True

    # رنگ فعلی
    if card.color == current_color:

        return True

    # نوع مشابه کارت‌های ویژه
    if card.card_type == top_card.card_type:

        if card.card_type != NUMBER:

            return True

    # عدد یکسان
    if (
        card.card_type == NUMBER
        and top_card.card_type == NUMBER
        and card.value == top_card.value
    ):

        return True

    return False