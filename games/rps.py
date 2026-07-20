import random


choices = [
    "🪨 سنگ",
    "📄 کاغذ",
    "✂️ قیچی"
]


def play(player):

    bot = random.choice(choices)

    if player == bot:
        result = "draw"

    elif (
        (player == "🪨 سنگ" and bot == "✂️ قیچی")
        or
        (player == "📄 کاغذ" and bot == "🪨 سنگ")
        or
        (player == "✂️ قیچی" and bot == "📄 کاغذ")
    ):
        result = "win"

    else:
        result = "lose"

    return {
        "player": player,
        "bot": bot,
        "result": result
    }