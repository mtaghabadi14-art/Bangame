from rubika import send_message

from handlers.esm_buttons import (
    show_after_save,
    show_waiting,
    ask_for_answer
)


# ==========================================
# بازیکن در حال نوشتن جواب
# ==========================================

def set_waiting(
    room,
    player,
    category
):

    if "waiting" not in room.data:

        room.data["waiting"] = {}

    room.data["waiting"][player] = category


# ==========================================
# انتخاب دسته
# ==========================================

def choose_category(
    room,
    player,
    category
):

    if "answers" not in room.data:

        room.data["answers"] = {}

    if player not in room.data["answers"]:

        room.data["answers"][player] = {}

    old_answer = room.data["answers"][player].get(
        category
    )

    set_waiting(
        room,
        player,
        category
    )

    letter = room.data.get(
        "letter",
        "؟"
    )

    # اگر جواب قبلی وجود داشته باشد
    if old_answer:

        send_message(
            player,
            (
                f"✏️ جواب قبلی {category}:\n\n"
                f"«{old_answer}»\n\n"
                "🔄 جواب جدید را ارسال کن تا جایگزین شود."
            )
        )

    else:

        send_message(
            player,
            (
                f"✍️ دسته: {category}\n\n"
                f"🔤 حرف: {letter}\n\n"
                "جوابت را ارسال کن."
            )
        )

    # کی‌پد را فقط به حالت انصراف تغییر می‌دهیم

    ask_for_answer(
        player,
        category,
        letter
    )


# ==========================================
# ذخیره جواب
# ==========================================

def save_answer(
    room,
    player,
    text
):

    waiting = room.data.get(
        "waiting",
        {}
    ).get(player)

    if waiting is None:

        return False

    text = text.strip()

    if not text:

        send_message(
            player,
            "❌ جواب نمی‌تواند خالی باشد."
        )

        return False

    letter = room.data.get(
        "letter"
    )

    # ==========================================
    # بررسی حرف
    # ==========================================

    if letter:

        if not text.startswith(letter):

            send_message(
                player,
                (
                    f"❌ جواب باید با حرف «{letter}» شروع شود.\n\n"
                    f"دسته: {waiting}"
                )
            )

            return False

    # ==========================================
    # ذخیره
    # ==========================================

    if "answers" not in room.data:

        room.data["answers"] = {}

    if player not in room.data["answers"]:

        room.data["answers"][player] = {}

    room.data["answers"][player][waiting] = text

    # حذف حالت انتظار
    room.data["waiting"].pop(
        player,
        None
    )

    send_message(
        player,
        (
            f"✅ جواب {waiting} ذخیره شد.\n\n"
            f"📝 جواب: {text}"
        )
    )

    # برگرداندن همان Chat Keypad دسته‌ها
    show_after_save(
        player
    )

    return True


# ==========================================
# آماده شدن
# ==========================================

def ready(
    room,
    player
):

    if player in room.data.get(
        "ready",
        []
    ):

        send_message(
            player,
            (
                "✅ تو قبلاً آماده شدی.\n"
                "⏳ منتظر بقیه بازیکنان باش..."
            )
        )

        show_waiting(
            player
        )

        return

    # اگر هنوز جوابی در حال نوشتن است
    if player in room.data.get(
        "waiting",
        {}
    ):

        send_message(
            player,
            "❌ اول جواب دسته انتخاب‌شده را ارسال کن."
        )

        return

    room.data.setdefault(
        "ready",
        []
    )

    room.data["ready"].append(
        player
    )

    show_waiting(
        player
    )

    send_message(
        player,
        (
            "✅ آماده شدی!\n\n"
            "⏳ منتظر بقیه بازیکنان باش..."
        )
    )

    # ==========================================
    # آیا همه آماده‌اند؟
    # ==========================================

    if len(room.data["ready"]) == len(room.players):

        finish_waiting(
            room
        )


# ==========================================
# پایان انتظار
# ==========================================

def finish_waiting(
    room
):

    from handlers.esm_check import show_result

    show_result(
        room
    )