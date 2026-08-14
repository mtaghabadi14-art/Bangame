from rubika import (
    send_message,
    send_keypad
)

from database import get_nickname
from handlers.esm_buttons import CATEGORIES


# ==========================================
# گرفتن نام بازیکن
# ==========================================

def get_player_name(player):

    nickname = get_nickname(player)

    if nickname:
        return nickname

    return "بازیکن"


# ==========================================
# تمیز کردن جواب
# ==========================================

def normalize_answer(answer):

    if not answer:
        return ""

    return " ".join(
        str(answer).strip().split()
    )


# ==========================================
# بررسی جواب
# ==========================================

def check_answer(
    letter,
    answer
):

    answer = normalize_answer(answer)
    letter = normalize_answer(letter)

    if not answer:
        return False

    if not letter:
        return False

    return answer.startswith(letter)


# ==========================================
# امتیاز یک دسته
# ==========================================

def calculate_category_score(
    letter,
    players_answers,
    category
):

    results = {}
    answers = {}

    for player, data in players_answers.items():

        answer = data.get(
            category,
            ""
        )

        answer = normalize_answer(
            answer
        )

        if check_answer(
            letter,
            answer
        ):

            answers[player] = answer

        else:

            answers[player] = None

    correct_answers = [
        answer
        for answer in answers.values()
        if answer is not None
    ]

    for player, answer in answers.items():

        if answer is None:

            results[player] = 0

        elif correct_answers.count(answer) > 1:

            results[player] = 5

        else:

            results[player] = 20

    return results


# ==========================================
# محاسبه کل امتیاز
# ==========================================

def check_game(room):

    letter = room.data.get(
        "letter",
        ""
    )

    players_answers = room.data.get(
        "answers",
        {}
    )

    scores = {}

    for player in players_answers:

        scores[player] = 0

    for category in CATEGORIES:

        result = calculate_category_score(
            letter,
            players_answers,
            category
        )

        for player, score in result.items():

            scores[player] += score

    return scores


# ==========================================
# ساخت دکمه‌های نتیجه
# ==========================================

def build_result_keyboard():

    return [
        [
            {
                "id": "esm_complain",
                "text": "⚖️ اعتراض به نتیجه"
            }
        ],
        [
            {
                "id": "esm_exit_result",
                "text": "🚪 خروج"
            }
        ]
    ]


# ==========================================
# نمایش نتیجه
# ==========================================

def show_result(room):

    scores = check_game(
        room
    )

    # ذخیره امتیاز اولیه
    room.data["scores"] = scores.copy()

    # وضعیت اعتراض
    room.data["complaint"] = None

    letter = room.data.get(
        "letter",
        "؟"
    )

    text = (
        "🎉 نتیجه اسم و فامیل\n\n"
        f"🔤 حرف انتخاب شده: {letter}\n\n"
    )

    # ======================================
    # جواب‌ها
    # ======================================

    for category in CATEGORIES:

        text += (
            f"{category}:\n"
        )

        for player, answers in room.data.get(
            "answers",
            {}
        ).items():

            answer = answers.get(
                category,
                "❌"
            )

            if not answer:
                answer = "❌"

            nickname = get_player_name(
                player
            )

            text += (
                f"👤 {nickname}: "
                f"{answer}\n"
            )

        text += "\n"

    # ======================================
    # امتیاز
    # ======================================

    text += (
        "🏆 امتیاز نهایی:\n\n"
    )

    sorted_scores = sorted(
        scores.items(),
        key=lambda item: item[1],
        reverse=True
    )

    for index, (
        player,
        score
    ) in enumerate(
        sorted_scores,
        start=1
    ):

        nickname = get_player_name(
            player
        )

        if index == 1:

            medal = "🥇"

        elif index == 2:

            medal = "🥈"

        elif index == 3:

            medal = "🥉"

        else:

            medal = "👤"

        text += (
            f"{medal} {nickname}\n"
            f"⭐ {score} امتیاز\n\n"
        )

    text += (
        "⚖️ اگر فکر می‌کنی امتیاز یک جواب اشتباه محاسبه شده، "
        "می‌توانی اعتراض ثبت کنی."
    )

    # ======================================
    # ارسال نتیجه
    # ======================================

    for player in room.players:

        send_keypad(
            player,
            text,
            build_result_keyboard()
        )

    return scores