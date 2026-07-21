from fastapi import FastAPI, Request
from rubika import send_message, send_keypad, remove_keypad

from database import (
    create_tables,
    add_user,
    get_user,
    add_coins
)

from games import rps, guess, dice
from level import give_xp

import time

app = FastAPI()

create_tables()

# -----------------------------
# حافظه موقت
# -----------------------------

states = {}

# -----------------------------
# منوی اصلی
# -----------------------------

def main_menu(chat_id):

    send_keypad(
        chat_id,
        "👋 دوباره خوش آمدی به Bangame!\n\nاز منوی زیر انتخاب کن 👇",
        [
            ["🎮 بازی‌ها", "👤 پروفایل"],
            ["🪙 کیف پول", "🎁 جایزه روزانه"]
        ]
    )

# -----------------------------
# منوی بازی‌ها
# -----------------------------

def games_menu(chat_id):

    send_keypad(
        chat_id,
        "🎮 یکی از بازی‌ها را انتخاب کن:",
        [
            ["✂️ سنگ کاغذ قیچی"],
            ["🔢 حدس عدد"],
            ["🎲 تاس"],
            ["🚪 خروج"]
        ]
    )

# -----------------------------
# صفحه اصلی
# -----------------------------

@app.get("/")
def home():

    return {
        "status": "Bangame Bot Online 🚀"
    }

# -----------------------------
# دریافت پیام
# -----------------------------

@app.post("/receiveUpdate")
async def receive_update(request: Request):

    data = await request.json()

    print(data)

    try:

        update = data.get("update", {})

        if update.get("type") != "NewMessage":
            return {"ok": True}

        chat_id = update["chat_id"]

        msg = update["new_message"]

        text = (
            msg.get("aux_data", {}).get("button_id")
            or msg.get("text", "")
        ).strip()

        if not get_user(chat_id):
            add_user(chat_id)

        user = get_user(chat_id)

        # -----------------------------
        # شروع
        # -----------------------------

        if text == "/start":

            states.pop(chat_id, None)

            main_menu(chat_id)

        # -----------------------------
        # منوی اصلی
        # -----------------------------

        elif text == "🎮 بازی‌ها":

            games_menu(chat_id)

        elif text == "👤 پروفایل":

            _, coins, level, xp = user

            send_message(
                chat_id,
                f"👤 پروفایل\n\n"
                f"🪙 سکه: {coins}\n"
                f"⭐ لول: {level}\n"
                f"✨ XP: {xp}"
            )

        elif text == "🪙 کیف پول":

            _, coins, _, _ = user

            send_message(
                chat_id,
                f"🪙 موجودی شما:\n{coins} سکه"
            )

        elif text == "🎁 جایزه روزانه":

            now = int(time.time())

            if (
                chat_id in states
                and states[chat_id].get("daily")
                and now - states[chat_id]["daily"] < 86400
            ):

                remain = 86400 - (
                    now - states[chat_id]["daily"]
                )

                h = remain // 3600
                m = (remain % 3600) // 60

                send_message(
                    chat_id,
                    f"⏳ جایزه روزانه را گرفتی.\n"
                    f"{h} ساعت و {m} دقیقه دیگر."
                )

            else:

                add_coins(chat_id, 50)

                states.setdefault(chat_id, {})

                states[chat_id]["daily"] = now

                send_message(
                    chat_id,
                    "🎉 جایزه روزانه دریافت شد!\n"
                    "🪙 +50 سکه"
                )

        elif text == "🚪 خروج":

            states.pop(chat_id, None)

            remove_keypad(
                chat_id,
                "✅ از بازی خارج شدی."
            )

            main_menu(chat_id)
                    # -----------------------------
        # سنگ کاغذ قیچی
        # -----------------------------

        elif text == "✂️ سنگ کاغذ قیچی":

            states[chat_id] = {
                "game": "rps"
            }

            send_keypad(
                chat_id,
                "✂️ یکی را انتخاب کن 👇",
                [
                    ["🪨 سنگ", "📄 کاغذ", "✂️ قیچی"],
                    ["🚪 خروج"]
                ]
            )

        elif (
            isinstance(states.get(chat_id), dict)
            and states[chat_id].get("game") == "rps"
            and text in ["🪨 سنگ", "📄 کاغذ", "✂️ قیچی"]
        ):

            player = text

            result = rps.play(player)

            message = (
                f"👤 تو: {result['player']}\n"
                f"🤖 ربات: {result['bot']}\n\n"
            )

            if result["result"] == "win":

                add_coins(chat_id, 5)

                level = give_xp(chat_id, 2)

                message += "🏆 برنده شدی!\n🪙 +5 سکه\n⭐ +2 XP"

                if level["level_up"]:

                    message += (
                        f"\n\n🎉 LEVEL UP!"
                        f"\n⭐ Level {level['level']}"
                        f"\n🪙 +{level['reward']} سکه"
                    )

            elif result["result"] == "lose":

                give_xp(chat_id, 1)

                message += "😢 ربات برنده شد.\n⭐ +1 XP"

            else:

                give_xp(chat_id, 1)

                message += "🤝 مساوی شد.\n⭐ +1 XP"

            send_keypad(
                chat_id,
                message,
                [
                    ["🪨 سنگ", "📄 کاغذ", "✂️ قیچی"],
                    ["🚪 خروج"]
                ]
            )
                    # -----------------------------
        # حدس عدد
        # -----------------------------

        elif text == "🔢 حدس عدد":

            number = guess.create_game()

            states[chat_id] = {
                "game": "guess",
                "number": number,
                "tries": 0
            }

            remove_keypad(
                chat_id,
                "🔢 یک عدد بین 1 تا 100 حدس بزن."
            )

        elif (
            isinstance(states.get(chat_id), dict)
            and states[chat_id].get("game") == "guess"
        ):

            if not text.isdigit():

                send_message(
                    chat_id,
                    "❌ فقط عدد وارد کن."
                )

            else:

                states[chat_id]["tries"] += 1

                value = int(text)

                result = guess.check(
                    states[chat_id]["number"],
                    value
                )

                if result == "higher":

                    send_message(
                        chat_id,
                        "⬆️ عدد من بزرگ‌تره."
                    )

                elif result == "lower":

                    send_message(
                        chat_id,
                        "⬇️ عدد من کوچک‌تره."
                    )

                else:

                    tries = states[chat_id]["tries"]

                    if tries == 1:
                        coins = 100
                        xp = 20
                    elif tries == 2:
                        coins = 80
                        xp = 18
                    elif tries == 3:
                        coins = 60
                        xp = 15
                    elif tries <= 5:
                        coins = 40
                        xp = 10
                    elif tries <= 8:
                        coins = 25
                        xp = 6
                    else:
                        coins = 10
                        xp = 3

                    add_coins(chat_id, coins)

                    level = give_xp(chat_id, xp)

                    states.pop(chat_id)

                    message = (
                        f"🎉 درست حدس زدی!\n"
                        f"🪙 +{coins} سکه\n"
                        f"⭐ +{xp} XP"
                    )

                    if level["level_up"]:

                        message += (
                            f"\n\n🎉 LEVEL UP!"
                            f"\n⭐ Level {level['level']}"
                            f"\n🪙 +{level['reward']} سکه"
                        )

                    send_message(chat_id, message)

                    games_menu(chat_id)

        # -----------------------------
        # تاس
        # -----------------------------

        elif text == "🎲 تاس":

            states[chat_id] = {
                "game": "dice"
            }

            send_keypad(
                chat_id,
                "🎲 برای انداختن تاس روی دکمه زیر بزن.",
                [
                    ["🎲 ریختن تاس"],
                    ["🚪 خروج"]
                ]
            )

        elif (
            isinstance(states.get(chat_id), dict)
            and states[chat_id].get("game") == "dice"
            and text == "🎲 ریختن تاس"
        ):

            player = dice.roll()
            bot = dice.roll()

            message = (
                f"🎲 تاس تو: {player}\n"
                f"🤖 تاس ربات: {bot}\n\n"
            )

            if player > bot:

                add_coins(chat_id, 10)

                level = give_xp(chat_id, 3)

                message += "🏆 برنده شدی!\n🪙 +10 سکه\n⭐ +3 XP"

                if level["level_up"]:

                    message += (
                        f"\n\n🎉 LEVEL UP!"
                        f"\n⭐ Level {level['level']}"
                        f"\n🪙 +{level['reward']} سکه"
                    )

            elif player < bot:

                give_xp(chat_id, 1)

                message += "😢 ربات برنده شد.\n⭐ +1 XP"

            else:

                give_xp(chat_id, 1)

                message += "🤝 مساوی شد.\n⭐ +1 XP"

            send_keypad(
                chat_id,
                message,
                [
                    ["🎲 ریختن تاس"],
                    ["🚪 خروج"]
                ]
            )
                    # -----------------------------
        # پیام ناشناخته
        # -----------------------------

        else:

            send_message(
                chat_id,
                "❓ دستور را متوجه نشدم.\nاز دکمه‌های منو استفاده کن."
            )

    except Exception as e:

        print("ERROR:", e)

        try:

            send_message(
                chat_id,
                "❌ خطایی در ربات رخ داد."
            )

        except:
            pass

    return {
        "ok": True
    }


# -----------------------------
# اجرای محلی
# -----------------------------

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )


# ==========================================
# پایان فایل app.py
# Bangame v2.0
# ==========================================