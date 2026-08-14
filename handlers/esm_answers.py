from rubika import (
    send_message,
    edit_message_text
)

from handlers.esm_buttons import (
    show_categories_again,
    show_after_save,
    show_waiting
)


# ==========================================
# پیام وضعیت بازی
# ==========================================

def update_status(
    room,
    player,
    text
):

    message_ids = room.data.get(
        "status_messages",
        {}
    )

    message_id = message_ids.get(
        player
    )

    if not message_id:
        return False

    result = edit_message_text(
        player,
        message_id,
        text
    )

    return result


# ==========================================
# تنظیم حالت انتظار جواب
# ==========================================

def set_waiting(
    room,
    player,
    category
):

    room.data.setdefault(
        "waiting",
        {}
    )

    room.data["waiting"][player] = category


# ==========================================
# انتخاب دسته
# ==========================================

def choose_category(
    room,
    player,
    category
):

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

    # --------------------------------------
    # تغییر کی‌پد بدون پیام جدید
    # --------------------------------------

    from handlers.esm_buttons import show_answer_mode

    show_answer_mode(
        player
    )

    # --------------------------------------
    # متن وضعیت را ویرایش می‌کنیم
    # --------------------------------------

    if old_answer:

        text = (
            "✏️ ویرایش جواب\n\n"
            f"🔤 حرف: {letter}\n"
            f"📚 دسته: {category}\n\n"
            f"📝 جواب قبلی: {old_answer}\n\n"
            "جواب جدیدت را ارسال کن."
        )

    else:

        text = (
            "✍️ نوشتن جواب\n\n"
            f"🔤 حرف: {letter}\n"
            f"📚 دسته: {category}\n\n"
            "جوابت را ارسال کن."
        )

    if not update_status(
        room,
        player,
        text
    ):

        # فقط اگر پیام وضعیت وجود نداشت
        # یک پیام ساخته می‌شود
        result = send_message(
            player,
            text
        )

        message_id = (
            result
            .get("data", {})
            .get("message_id")
        )

        room.data.setdefault(
            "status_messages",
            {}
        )

        room.data["status_messages"][player] = message_id

    return True


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
    ).get(
        player
    )

    if waiting is None:

        return False

    text = text.strip()

    if not text:

        return False

    room.data["answers"][player][waiting] = text

    room.data["waiting"].pop(
        player,
        None
    )

    category = waiting

    letter = room.data.get(
        "letter",
        "؟"
    )

    # --------------------------------------
    # بازگشت کی‌پد دسته‌ها
    # --------------------------------------

    show_after_save(
        player
    )

    # --------------------------------------
    # ویرایش همان پیام
    # --------------------------------------

    update_status(
        room,
        player,
        (
            "✅ جواب ذخیره شد!\n\n"
            f"🔤 حرف: {letter}\n"
            f"📚 دسته: {category}\n"
            f"📝 جواب: {text}\n\n"
            "می‌توانی دسته دیگری را انتخاب کنی "
            "یا وقتی تمام کردی «✅ آماده‌ام» را بزن."
        )
    )

    return True


# ==========================================
# لغو نوشتن جواب
# ==========================================

def cancel_answer(
    room,
    player
):

    waiting = room.data.get(
        "waiting",
        {}
    )

    if player not in waiting:

        return False

    waiting.pop(
        player,
        None
    )

    show_categories_again(
        player
    )

    letter = room.data.get(
        "letter",
        "؟"
    )

    update_status(
        room,
        player,
        (
            "↩️ انتخاب دسته\n\n"
            f"🔤 حرف انتخاب شده: {letter}\n\n"
            "📚 دسته موردنظرت را انتخاب کن."
        )
    )

    return True


# ==========================================
# آماده شدن بازیکن
# ==========================================

def ready(
    room,
    player
):

    ready_players = room.data.setdefault(
        "ready",
        []
    )

    if player in ready_players:

        update_status(
            room,
            player,
            (
                "✅ تو قبلاً آماده شدی.\n\n"
                "⏳ منتظر بقیه بازیکنان باش..."
            )
        )

        show_waiting(
            player
        )

        return

    ready_players.append(
        player
    )

    show_waiting(
        player
    )

    update_status(
        room,
        player,
        (
            "✅ آماده شدی!\n\n"
            "⏳ منتظر بقیه بازیکنان باش..."
        )
    )

    if len(ready_players) == len(room.players):

        finish_waiting(
            room
        )


# ==========================================
# پایان انتظار
# ==========================================

def finish_waiting(room):

    from handlers.esm_check import show_result

    show_result(
        room
    )