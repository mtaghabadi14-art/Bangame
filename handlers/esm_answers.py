from rubika import send_message

from handlers.esm_buttons import (
    show_categories,
    show_after_save,
    show_waiting
)


# ==========================================
# بازیکن در حال نوشتن جواب
# ==========================================

def set_waiting(room, player, category):

    room.data["waiting"][player] = category


# ==========================================
# گرفتن دسته انتخاب شده
# ==========================================

def choose_category(room, player, category):

    if player not in room.data["answers"]:

        room.data["answers"][player] = {}

    old_answer = room.data["answers"][player].get(category)

    set_waiting(
        room,
        player,
        category
    )

    if old_answer:

        send_message(
            player,
            f"✏️ جواب قبلی {category}:\n"
            f"{old_answer}\n\n"
            f"جواب جدید را بفرست تا ویرایش شود."
        )

    else:

        send_message(
            player,
            f"✍️ جواب {category} را بنویس."
        )


# ==========================================
# ذخیره جواب
# ==========================================

def save_answer(room, player, text):

    waiting = room.data["waiting"].get(player)

    if waiting is None:

        return False

    room.data["answers"][player][waiting] = text

    room.data["waiting"].pop(
        player,
        None
    )

    show_after_save(player)

    return True


# ==========================================
# آماده شدن بازیکن
# ==========================================

def ready(room, player):

    # اگر قبلاً آماده شده
    if player in room.data["ready"]:

        send_message(
            player,
            "✅ تو قبلاً آماده شدی.\n"
            "منتظر بقیه بازیکنان باش."
        )

        return

    room.data["ready"].append(player)

    send_message(
        player,
        "✅ آماده شدی.\n"
        "منتظر بقیه بازیکنان باش."
    )

    # اگر همه آماده بودند
    if len(room.data["ready"]) == len(room.players):

        finish_waiting(room)


# ==========================================
# پایان انتظار
# ==========================================

def finish_waiting(room):

    from handlers.esm_check import show_result

    # نمایش مستقیم نتیجه
    # از ارسال پیام اضافه به تمام بازیکنان جلوگیری می‌کنیم

    show_result(room)