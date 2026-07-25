import random


# ==========================================
# داده‌های بازی
# ==========================================

items = [
    "🍎",
    "🚗",
    "⭐",
    "🐱",
    "🌙",
    "🔥",
    "⚽",
    "🎮",
    "🍕",
    "🚀"
]


levels = {

    "easy": 3,

    "medium": 5,

    "hard": 7

}



# ==========================================
# ساخت بازی
# ==========================================

def create_game(level):

    count = levels.get(
        level,
        3
    )


    sequence = random.sample(
        items,
        count
    )


    return {

        "level": level,

        "sequence": sequence,

        "answer": " ".join(sequence)

    }



# ==========================================
# بررسی جواب
# ==========================================

def check(game, text):

    answer = text.strip()


    return answer == game["answer"]