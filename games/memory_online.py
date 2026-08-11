import random


# ==========================================
# ایموجی‌های معروف
# ==========================================

EMOJIS = [
    "😂",
    "😭",
    "🤣",
    "😎",
    "😍",
    "😡",
    "😱",
    "🤔",
    "🥳",
    "😴",
    "🤯",
    "😢",
    "😆",
    "😅",
    "😉",
    "😋",
    "😐",
    "🙄",
    "😮",
    "😇",
]


# ==========================================
# ایموجی‌های مرتب‌شده برای بررسی سریع‌تر
# ==========================================

SORTED_EMOJIS = sorted(
    EMOJIS,
    key=len,
    reverse=True
)


# ==========================================
# ساخت ترتیب تصادفی
# ==========================================

def generate_sequence():

    length = random.randint(5, 10)

    return random.sample(
        EMOJIS,
        length
    )


# ==========================================
# تبدیل ترتیب به متن
# ==========================================

def sequence_to_text(sequence):

    return " ".join(sequence)


# ==========================================
# نرمال‌سازی جواب
# ==========================================

def normalize_answer(text):

    if not text:

        return []

    # حذف فاصله‌های معمولی
    text = text.replace(
        " ",
        ""
    )

    # حذف فاصله‌های یونیکدی
    text = text.replace(
        "\u200c",
        ""
    )

    text = text.replace(
        "\u200b",
        ""
    )

    # پیدا کردن ایموجی‌ها
    result = []

    position = 0

    while position < len(text):

        found = False

        for emoji in SORTED_EMOJIS:

            if text.startswith(
                emoji,
                position
            ):

                result.append(
                    emoji
                )

                position += len(emoji)

                found = True

                break

        if not found:

            return []

    return result


# ==========================================
# بررسی جواب
# ==========================================

def check_answer(
    correct_sequence,
    player_answer
):

    answer = normalize_answer(
        player_answer
    )

    return answer == correct_sequence


# ==========================================
# ساخت بازی
# ==========================================

def create_game():

    sequence = generate_sequence()

    return {
        "sequence": sequence,
        "winner": None,
        "finished": False
    }


# ==========================================
# گرفتن ترتیب بازی
# ==========================================

def get_sequence(game):

    return game.get(
        "sequence",
        []
    )


# ==========================================
# نمایش ترتیب
# ==========================================

def get_sequence_text(game):

    sequence = get_sequence(
        game
    )

    return sequence_to_text(
        sequence
    )


# ==========================================
# ارسال جواب بازیکن
# ==========================================

def submit_answer(
    game,
    player,
    answer
):

    # بازی قبلاً تمام شده
    if game.get("finished"):

        return {
            "correct": False,
            "winner": game.get(
                "winner"
            ),
            "finished": True
        }

    sequence = get_sequence(
        game
    )

    correct = check_answer(
        sequence,
        answer
    )

    # جواب اشتباه
    if not correct:

        return {
            "correct": False,
            "winner": None,
            "finished": False
        }

    # اولین جواب صحیح
    game["winner"] = player

    game["finished"] = True

    return {
        "correct": True,
        "winner": player,
        "finished": True
    }


# ==========================================
# بررسی پایان بازی
# ==========================================

def is_finished(game):

    return game.get(
        "finished",
        False
    )


# ==========================================
# گرفتن برنده
# ==========================================

def get_winner(game):

    return game.get(
        "winner"
    )
