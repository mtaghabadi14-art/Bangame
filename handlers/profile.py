from rubika import send_message
from database import get_user, add_coins
import time

daily_reward = {}


def show_profile(chat_id):

    user = get_user(chat_id)

    if not user:

        send_message(
            chat_id,
            "❌ اطلاعات کاربر پیدا نشد."
        )
        return

    (
    _,
    coins,
    level,
    xp,
    typing_games,
    typing_best_time,
    typing_best_wpm,
    nickname,
    title
) = user

    if typing_best_time == 0:
        best_time = "-"
    else:
        best_time = f"{typing_best_time:.2f} ثانیه"

    if typing_best_wpm == 0:
        best_wpm = "-"
    else:
        best_wpm = f"{round(typing_best_wpm)} WPM"

    send_message(
        chat_id,
        f"👤 پروفایل\n\n"
        f"🪙 سکه: {coins}\n"
        f"⭐ لول: {level}\n"
        f"✨ XP: {xp}\n\n"
        f"⌨️ سرعت تایپ\n"
        f"🎮 تعداد بازی: {typing_games}\n"
        f"🏆 بهترین زمان: {best_time}\n"
        f"⚡ بهترین سرعت: {best_wpm}"
        f"👤 لقب: {nickname}"
        f"🏷 عنوان: {title}"

    )


def show_wallet(chat_id):

    user = get_user(chat_id)

    _, coins, _, _, _, _, _ = user

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