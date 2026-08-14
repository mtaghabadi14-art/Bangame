from rubika import send_message

from database import get_nickname

from handlers.esm_buttons import CATEGORIES


# ==========================================
# گرفتن نام نمایشی بازیکن
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
# بررسی یک جواب
# ==========================================

def check_answer(
    letter,
    answer
):

    answer = normalize_answer(
        answer
    )

    letter = normalize_answer(
        letter
    )

    if not answer:
        return False

    if not letter:
        return False

    return answer.startswith(
        letter
    )


# ==========================================
# حساب امتیاز یک دسته
# ==========================================

def calculate_category_score(
    letter,
    players_answers,
    category
):

    results = {}

    answers = {}

    # ======================================
    # بررسی جواب تمام بازیکنان
    # ======================================

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

    # ======================================
    # جواب‌های صحیح
    # ======================================

    correct_answers = [
        answer
        for answer in answers.values()
        if answer is not None
    ]

    # ======================================
    # امتیازدهی
    # ======================================

    for player, answer in answers.items():

        # جواب خالی یا اشتباه
        if answer is None:

            results[player] = 0

        # جواب تکراری
        elif correct_answers.count(answer) > 1:

            results[player] = 5

        # جواب صحیح و غیرتکراری
        else:

            results[player] = 20

    return results


# ==========================================
# بررسی کل بازی
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

    # ======================================
    # مقداردهی اولیه امتیازها
    # ======================================

    for player in players_answers:

        scores[player] = 0

    # ======================================
    # بررسی تمام دسته‌ها
    # ======================================

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
# نمایش نتیجه
# ==========================================

def show_result(room):

    scores = check_game(
        room
    )

    letter = room.data.get(
        "letter",
        "؟"
    )

    text = (
        "🎉 نتیجه اسم و فامیل\n\n"
        f"🔤 حرف انتخاب شده: {letter}\n\n"
    )

    # ======================================
    # نمایش جواب‌ها
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
    # امتیاز نهایی
    # ======================================

    text += (
        "🏆 امتیاز نهایی:\n\n"
    )

    # ======================================
    # مرتب‌سازی امتیازها
    # ======================================

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

        # مدال
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

    # ======================================
    # ارسال نتیجه
    # ======================================

    for player in room.players:

        send_message(
            player,
            text
        )

    return scores