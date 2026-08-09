from rubika import send_message

from database import get_nickname


# ==========================================
# گرفتن نام نمایشی بازیکن
# ==========================================

def get_player_name(player):

    nickname = get_nickname(player)

    if nickname:

        return nickname

    return "بازیکن"


# ==========================================
# بررسی یک جواب
# ==========================================

def check_answer(letter, answer):

    if not answer:

        return False

    answer = answer.strip()

    if answer.startswith(letter):

        return True

    return False


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

    for player, data in players_answers.items():

        answer = data.get(
            category,
            ""
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
        if answer
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
# بررسی کل بازی
# ==========================================

def check_game(room):

    letter = room.data.get(
        "letter"
    )

    players_answers = room.data.get(
        "answers",
        {}
    )

    scores = {}

    categories = [
        "👤 اسم",
        "🏠 فامیل",
        "🍎 میوه",
        "🍔 غذا",
        "🎨 رنگ",
        "📦 اشیا",
        "🐶 حیوان",
        "🌍 شهر یا کشور",
        "🖐 اعضای بدن",
        "🎬 فیلم یا سریال"
    ]

    for player in players_answers:

        scores[player] = 0

    for category in categories:

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

    scores = check_game(room)

    letter = room.data.get(
        "letter"
    )

    categories = [
        "👤 اسم",
        "🏠 فامیل",
        "🍎 میوه",
        "🍔 غذا",
        "🎨 رنگ",
        "📦 اشیا",
        "🐶 حیوان",
        "🌍 شهر یا کشور",
        "🖐 اعضای بدن",
        "🎬 فیلم یا سریال"
    ]

    text = (
        "🎉 نتیجه اسم و فامیل\n\n"
        f"🔤 حرف انتخاب شده: {letter}\n\n"
    )

    # ======================================
    # نمایش جواب‌ها
    # ======================================

    for category in categories:

        text += f"{category}:\n"

        for player, answers in room.data["answers"].items():

            answer = answers.get(
                category,
                "❌"
            )

            nickname = get_nickname(player)

            if not nickname:
                nickname = "بازیکن"

            text += (
                f"👤 {nickname}: "
                f"{answer}\n"
            )

    # ======================================
    # امتیاز نهایی
    # ======================================

    text += "🏆 امتیاز نهایی:\n\n"

    # مرتب‌سازی از بیشترین امتیاز
    sorted_scores = sorted(
        scores.items(),
        key=lambda item: item[1],
        reverse=True
    )

    for index, (player, score) in enumerate(
        sorted_scores,
        start=1
    ):

        nickname = get_player_name(player)

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

    for player in room.players:

        send_message(
            player,
            text
        )