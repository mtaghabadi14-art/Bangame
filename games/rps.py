import random


choices = [
    "🪨 سنگ",
    "📄 کاغذ",
    "✂️ قیچی"
]


# -----------------------------
# بازی با ربات
# -----------------------------
def play_bot(player):

    bot = random.choice(choices)

    result = check(player, bot)

    if result == "player1":
        result = "win"
    elif result == "player2":
        result = "lose"
    else:
        result = "draw"

    return {
        "player": player,
        "bot": bot,
        "result": result
    }


# -----------------------------
# بازی دو نفره
# -----------------------------
def play(player1, player2):

    return check(player1, player2)


# -----------------------------
# بررسی برنده
# -----------------------------
def check(player1, player2):

    if player1 == player2:
        return "draw"

    if (
        (player1 == "🪨 سنگ" and player2 == "✂️ قیچی")
        or
        (player1 == "📄 کاغذ" and player2 == "🪨 سنگ")
        or
        (player1 == "✂️ قیچی" and player2 == "📄 کاغذ")
    ):
        return "player1"

    return "player2"