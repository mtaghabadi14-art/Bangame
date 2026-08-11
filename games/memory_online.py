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
# تعداد تلاش هر بازیکن
# ==========================================

MAX_ATTEMPTS = 3


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

    length = random.randint(
        5,
        10
    )

    return random.sample(
        EMOJIS,
        length
    )


# ==========================================
# تبدیل ترتیب به متن
# ==========================================

def sequence_to_text(sequence):

    return " ".join(
        sequence
    )


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

    # تبدیل متن به لیست ایموجی‌ها
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

        "finished": False,

        # تعداد تلاش‌های باقی‌مانده هر بازیکن
        "attempts": {},

        # بازیکنانی که حذف شده‌اند
        "eliminated": set()

    }


# ==========================================
# گرفتن تعداد تلاش باقی‌مانده
# ==========================================

def get_attempts(
    game,
    player
):

    attempts = game.setdefault(
        "attempts",
        {}
    )

    if player not in attempts:

        attempts[player] = MAX_ATTEMPTS

    return attempts[player]


# ==========================================
# ثبت تلاش بازیکن
# ==========================================

def use_attempt(
    game,
    player
):

    attempts = game.setdefault(
        "attempts",
        {}
    )

    if player not in attempts:

        attempts[player] = MAX_ATTEMPTS

    if attempts[player] > 0:

        attempts[player] -= 1

    # اگر تمام تلاش‌ها تمام شد
    if attempts[player] <= 0:

        eliminated = game.setdefault(
            "eliminated",
            set()
        )

        eliminated.add(
            player
        )

    return attempts[player]


# ==========================================
# بررسی اینکه بازیکن حذف شده یا نه
# ==========================================

def is_eliminated(
    game,
    player
):

    eliminated = game.get(
        "eliminated",
        set()
    )

    return player in eliminated


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
    if game.get(
        "finished"
    ):

        return {

            "correct": False,

            "winner": game.get(
                "winner"
            ),

            "finished": True,

            "eliminated": False,

            "attempts_left": 0

        }


    # بازیکن قبلاً حذف شده
    if is_eliminated(
        game,
        player
    ):

        return {

            "correct": False,

            "winner": None,

            "finished": game.get(
                "finished",
                False
            ),

            "eliminated": True,

            "attempts_left": 0

        }


    # تعداد تلاش فعلی
    attempts_left = get_attempts(
        game,
        player
    )


    # بررسی جواب
    sequence = get_sequence(
        game
    )

    correct = check_answer(
        sequence,
        answer
    )


    # ==========================================
    # جواب صحیح
    # ==========================================

    if correct:

        game["winner"] = player

        game["finished"] = True

        return {

            "correct": True,

            "winner": player,

            "finished": True,

            "eliminated": False,

            "attempts_left": attempts_left

        }


    # ==========================================
    # جواب اشتباه
    # ==========================================

    attempts_left = use_attempt(
        game,
        player
    )


    # اگر تلاش‌ها تمام شده
    if attempts_left <= 0:

        return {

            "correct": False,

            "winner": None,

            "finished": game.get(
                "finished",
                False
            ),

            "eliminated": True,

            "attempts_left": 0

        }


    # هنوز تلاش باقی مانده
    return {

        "correct": False,

        "winner": None,

        "finished": False,

        "eliminated": False,

        "attempts_left": attempts_left

    }


# ==========================================
# بررسی اینکه همه بازیکنان حذف شده‌اند
# ==========================================

def check_all_eliminated(
    game,
    players
):

    if not players:

        return False

    for player in players:

        if not is_eliminated(
            game,
            player
        ):

            return False

    game["finished"] = True

    return True


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