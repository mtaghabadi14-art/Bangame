from rubika import (
    send_message,
    send_keypad
)

from database import get_nickname

from handlers.esm_buttons import CATEGORIES

from rooms.manager import delete_room

from handlers.menu import room_menu


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
# بررسی جواب
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
    category,
    invalid_answers=None
):

    results = {}

    answers = {}

    if invalid_answers is None:

        invalid_answers = {}

    # ======================================
    # بررسی جواب تمام بازیکنان
    # ======================================

    for player, data in players_answers.items():

        # ----------------------------------
        # اگر جواب قبلاً با اعتراض باطل شده
        # ----------------------------------

        player_invalid = invalid_answers.get(
            player,
            []
        )

        if category in player_invalid:

            answers[player] = None
            continue

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
        "letter",
        ""
    )

    players_answers = room.data.get(
        "answers",
        {}
    )

    invalid_answers = room.data.get(
        "invalid_answers",
        {}
    )

    scores = {}

    # ======================================
    # مقداردهی اولیه
    # ======================================

    for player in players_answers:

        scores[player] = 0

    # ======================================
    # بررسی دسته‌ها
    # ======================================

    for category in CATEGORIES:

        result = calculate_category_score(
            letter,
            players_answers,
            category,
            invalid_answers
        )

        for player, score in result.items():

            scores[player] += score

    return scores

# ==========================================
# آماده‌سازی سیستم اعتراض
# ==========================================

def init_protest(room):

    room.data.setdefault(
        "protest",
        None
    )

    room.data.setdefault(
        "protest_votes",
        {}
    )


# ==========================================
# شروع اعتراض
# ==========================================

def start_protest(
    room,
    player
):

    init_protest(
        room
    )

    if room.data.get("protest"):

        send_message(
            player,
            "⚠️ در حال حاضر یک اعتراض در حال بررسی است."
        )

        return True

    send_keypad(
        player,
        (
            "⚖️ اعتراض به نتیجه\n\n"
            "📚 دسته‌ای که فکر می‌کنی امتیازش اشتباه است را انتخاب کن:"
        ),
        [
            [
                {
                    "id": f"esm_protest_category_{index}",
                    "text": category
                }
            ]
            for index, category in enumerate(CATEGORIES)
        ] + [
            [
                {
                    "id": "esm_protest_cancel",
                    "text": "❌ لغو"
                }
            ]
        ]
    )

    room.data["protest_selector"] = player

    return True


# ==========================================
# انتخاب دسته اعتراض
# ==========================================

def select_protest_category(
    room,
    player,
    category
):

    if category not in CATEGORIES:

        return False

    if room.data.get("protest_selector") != player:

        return False

    opponents = [
        p
        for p in room.players
        if p != player
    ]

    if not opponents:

        send_message(
            player,
            "❌ بازیکن دیگری برای اعتراض وجود ندارد."
        )

        return True

    room.data["protest_category"] = category

    buttons = []

    for opponent in opponents:

        nickname = get_player_name(
            opponent
        )

        buttons.append([
            {
                "id": f"esm_protest_player_{opponent}",
                "text": f"👤 {nickname}"
            }
        ])

    buttons.append([
        {
            "id": "esm_protest_cancel",
            "text": "❌ لغو"
        }
    ])

    send_keypad(
        player,
        (
            "⚖️ اعتراض به نتیجه\n\n"
            f"📚 دسته: {category}\n\n"
            "👤 به جواب کدام بازیکن اعتراض داری؟"
        ),
        buttons
    )

    return True


# ==========================================
# ثبت اعتراض به بازیکن
# ==========================================

def select_protest_player(
    room,
    player,
    target
):

    category = room.data.get(
        "protest_category"
    )

    if not category:

        return False

    if target not in room.players:

        return False

    if target == player:

        return False

    answer = room.data.get(
        "answers",
        {}
    ).get(
        target,
        {}
    ).get(
        category,
        ""
    )

    room.data["protest"] = {
        "protester": player,
        "category": category,
        "target": target,
        "answer": answer
    }

    room.data["protest_votes"] = {}

    voters = [
        p
        for p in room.players
        if p != player
    ]

    for voter in voters:

        send_keypad(
            voter,
            (
                "⚖️ اعتراض به نتیجه\n\n"
                f"👤 معترض: {get_player_name(player)}\n"
                f"📚 دسته: {category}\n"
                f"👤 بازیکن: {get_player_name(target)}\n"
                f"📝 جواب: {answer or '❌ بدون جواب'}\n\n"
                "آیا با اعتراض موافقی؟"
            ),
            [
                [
                    {
                        "id": "esm_protest_approve",
                        "text": "✅ تأیید اعتراض"
                    }
                ],
                [
                    {
                        "id": "esm_protest_reject",
                        "text": "❌ رد اعتراض"
                    }
                ]
            ]
        )

    send_message(
        player,
        (
            "⚖️ اعتراض ثبت شد.\n\n"
            f"📚 دسته: {category}\n"
            f"👤 بازیکن: {get_player_name(target)}\n"
            f"📝 جواب: {answer or '❌ بدون جواب'}\n\n"
            "⏳ منتظر رأی بازیکن دیگر باش..."
        )
    )

    return True


# ==========================================
# ثبت رأی اعتراض
# ==========================================

def vote_protest(
    room,
    voter,
    approve
):

    protest = room.data.get(
        "protest"
    )

    if not protest:

        send_message(
            voter,
            "❌ اعتراض فعالی وجود ندارد."
        )

        return True

    # معترض نمی‌تواند به اعتراض خودش رأی بدهد
    if voter == protest["protester"]:

        return True

    votes = room.data.setdefault(
        "protest_votes",
        {}
    )

    # جلوگیری از رأی دوباره
    if voter in votes:

        send_message(
            voter,
            "⚠️ رأی تو قبلاً ثبت شده است."
        )

        return True

    # ثبت رأی
    votes[voter] = (
        "approve"
        if approve
        else "reject"
    )

    # ==========================================
    # بازیکنانی که باید رأی بدهند
    # ==========================================

    required_voters = [
        p
        for p in room.players
        if p != protest["protester"]
    ]

    # هنوز همه رأی نداده‌اند
    if len(votes) < len(required_voters):

        send_message(
            voter,
            "✅ رأی تو ثبت شد."
        )

        return True

    # ==========================================
    # بررسی نتیجه رأی
    # ==========================================

    rejected = any(
        vote == "reject"
        for vote in votes.values()
    )

    # ==========================================
    # اعتراض رد شد
    # ==========================================

    if rejected:

        result_text = (
            "❌ اعتراض رد شد.\n\n"
            f"📚 دسته: {protest['category']}\n"
            f"👤 بازیکن: {get_player_name(protest['target'])}\n"
            f"📝 جواب: "
            f"{protest['answer'] or '❌ بدون جواب'}\n\n"
            "📊 نتیجه قبلی همچنان معتبر است."
        )

        for player in room.players:

            send_message(
                player,
                result_text
            )

    # ==========================================
    # اعتراض تأیید شد
    # ==========================================

    else:

        category = protest["category"]
        target = protest["target"]

        # --------------------------------------
        # ثبت اعتراض تأییدشده
        # --------------------------------------

        invalid_answers = room.data.setdefault(
            "invalid_answers",
            {}
        )

        invalid_categories = invalid_answers.setdefault(
            target,
            []
        )

        if category not in invalid_categories:

            invalid_categories.append(
                category
            )

        result_text = (
            "✅ اعتراض تأیید شد.\n\n"
            f"📚 دسته: {category}\n"
            f"👤 بازیکن: {get_player_name(target)}\n"
            f"📝 جواب: "
            f"{protest['answer'] or '❌ بدون جواب'}\n\n"
            "⚠️ این جواب نامعتبر شد.\n"
            "📊 امتیاز این دسته اصلاح شد."
        )

        for player in room.players:

            send_message(
                player,
                result_text
            )

    # ==========================================
    # پاک کردن اعتراض فعلی
    # ==========================================

    room.data["protest"] = None

    room.data["protest_votes"] = {}

    room.data.pop(
        "protest_selector",
        None
    )

    room.data.pop(
        "protest_category",
        None
    )

    # ==========================================
    # نمایش نتیجه جدید
    # ==========================================

    show_result(
        room
    )

    return True


# ==========================================
# بازگشت به کافه بازی
# ==========================================

def return_to_cafe(
    room,
    player
):

    returned_players = room.data.setdefault(
        "returned_players",
        []
    )

    # --------------------------------------
    # قبلاً برگشته
    # --------------------------------------

    if player in returned_players:

        room_menu(
            player
        )

        return True

    # --------------------------------------
    # ثبت بازگشت
    # --------------------------------------

    returned_players.append(
        player
    )

    room_menu(
        player
    )

    # --------------------------------------
    # بررسی بازگشت همه
    # --------------------------------------

    total_players = len(
        room.players
    )

    returned_count = len(
        returned_players
    )

    if returned_count >= total_players:

        delete_room(
            room.room_id
        )

        return True

    # --------------------------------------
    # هنوز بازیکن دیگری مانده
    # --------------------------------------

    send_message(
        player,
        (
            "🏠 به کافه بازی برگشتی.\n\n"
            f"⏳ منتظر بقیه بازیکنان...\n"
            f"👥 {returned_count}/{total_players} برگشته‌اند."
        )
    )

    return True


# ==========================================
# تأیید پایان بازی
# ==========================================

def vote_exit_result(
    room,
    player
):

    if player not in room.players:
        return True

    votes = room.data.setdefault(
        "exit_votes",
        set()
    )

    # قبلاً رأی داده
    if player in votes:

        send_message(
            player,
            "✅ قبلاً اعلام کردی که نتیجه قانونیه."
        )

        return True

    # ثبت رأی
    votes.add(player)

    remaining = len(room.players) - len(votes)

    if remaining > 0:

        send_message(
            player,
            (
                "✅ رأی تو ثبت شد.\n\n"
                f"⏳ منتظر {remaining} بازیکن دیگر..."
            )
        )

        return True

    # ======================================
    # همه تأیید کردند
    # ======================================

    players = room.players.copy()

    for p in players:

        send_message(
            p,
            "✅ همه بازیکنان نتیجه را تأیید کردند!\n\n"
            "🎮 اتاق بسته شد.\n"
            "☕ برگشت به کافه بازی..."
        )

    # حذف کامل اتاق
    delete_room(
        room.room_id
    )

    # برگشت همه به کافه
    for p in players:

        room_menu(
            p
        )

    return True


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

    init_protest(
        room
    )

    room.data["returned_players"] = []

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

    # ======================================
    # ارسال نتیجه
    # ======================================

    for player in room.players:

        send_keypad(
            player,
            text,
            [
                [
                    {
                        "id": "esm_protest",
                        "text": "⚖️ اعتراض به نتیجه"
                    }
                ],
                [
                    {
                        "id": "esm_exit_result",
                        "text": "✅ قانونیه"
                    }
                ]
            ]
        )

    return scores