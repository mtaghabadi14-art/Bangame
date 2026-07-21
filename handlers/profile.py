from rubika import send_message
from database import get_user, add_coins
import time

daily_reward = {}


def show_profile(chat_id):

    user = get_user(chat_id)

    _, coins, level, xp = user

    send_message(
        chat_id,
        f"👤 پروفایل\n\n"
        f"🪙 سکه: {coins}\n"
        f"⭐ لول: {level}\n"
        f"✨ XP: {xp}"
    )


def show_wallet(chat_id):

    user = get_user(chat_id)

    _, coins, _, _ = user

    send_message(
        chat_id,
        f"🪙 موجودی شما:\n{coins} سکه"
    )


def daily(chat_id):

    now = int(time.time())

    if (
        chat_id in daily_reward
        and now - daily_reward[chat_id] < 86400
    ):

        remain = 86400 - (now - daily_reward[chat_id])

        h = remain // 3600
        m = (remain % 3600) // 60

        send_message(
            chat_id,
            f"⏳ جایزه روزانه را گرفتی.\n"
            f"{h} ساعت و {m} دقیقه دیگر."
        )

        return

    add_coins(chat_id, 50)

    daily_reward[chat_id] = now

    send_message(
        chat_id,
        "🎉 جایزه روزانه دریافت شد!\n🪙 +50 سکه"
    )