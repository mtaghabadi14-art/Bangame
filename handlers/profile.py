from rubika import send_message
from database import get_user, add_coins
from handlers.profile_buttons import profile_menu
import time


daily_reward = {}


# ==========================================
# XP مورد نیاز هر لول
# ==========================================

def get_next_level_xp(level):

    levels = {
        1: 100,
        2: 250,
        3: 500,
        4: 800,
        5: 1200,
        6: 1700,
        7: 2500,
        8: 3500,
        9: 5000,
    }


    return levels.get(
        level,
        level * 700
    )



# ==========================================
# پروفایل
# ==========================================

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
        nickname,
        title,
        coins,
        level,
        xp,
        typing_games,
        typing_best_time,
        typing_best_wpm

    ) = user



    if typing_best_time == 0:

        best_time = "-"

    else:

        best_time = f"{typing_best_time:.2f} ثانیه"



    if typing_best_wpm == 0:

        best_wpm = "-"

    else:

        best_wpm = f"{round(typing_best_wpm)} WPM"



    next_xp = get_next_level_xp(level)



    if nickname is None:

       nickname = "بدون لقب"

       xp_need = level * 100
       xp_text = f"{xp}/{xp_need}"

    send_message(
        chat_id,

        f"👤 پروفایل\n\n"

        f"✨ لقب: {nickname}\n"
        f"{title}\n\n"

        f"🪙 سکه: {coins}\n"
        f"⭐ لول: {level}\n"
        f"✨ XP: {xp}/{next_xp}\n\n"

        f"🔥 رکوردها:\n"
        f"⌨️ سرعت تایپ: {best_wpm}\n"
        f"🧠 حافظه: ---\n"
        f"⚡ واکنش: ---"

    )

    profile_menu(chat_id)

# ==========================================
# کیف پول
# ==========================================

def show_wallet(chat_id):

    user = get_user(chat_id)


    if not user:

        return



    coins = user[3]


    send_message(
        chat_id,
        f"🪙 موجودی شما:\n{coins} سکه"
    )



# ==========================================
# جایزه روزانه
# ==========================================

def daily(chat_id):

    now = int(time.time())


    if (
        chat_id in daily_reward
        and now - daily_reward[chat_id] < 86400
    ):


        remain = 86400 - (
            now - daily_reward[chat_id]
        )


        h = remain // 3600

        m = (
            remain % 3600
        ) // 60


        send_message(
            chat_id,
            f"⏳ جایزه روزانه را گرفتی.\n"
            f"{h} ساعت و {m} دقیقه دیگر."
        )


        return



    add_coins(
        chat_id,
        50
    )


    daily_reward[chat_id] = now


    send_message(
        chat_id,
        "🎉 جایزه روزانه دریافت شد!\n🪙 +50 سکه"
    )