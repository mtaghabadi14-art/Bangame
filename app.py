from fastapi import FastAPI, Request
from rubika import send_message, send_keypad, remove_keypad
from database import create_tables, add_user, get_user, add_coins
import random


app = FastAPI()

create_tables()


# وضعیت بازی کاربران
games = {}



@app.get("/")
def home():

    return {
        "status": "Bangame Bot is running 🚀"
    }



@app.post("/receiveUpdate")
async def receive_update(request: Request):

    data = await request.json()

    print("NEW UPDATE:")
    print(data)


    try:

        update = data.get("update", {})


        if update.get("type") != "NewMessage":
            return {"ok": True}



        chat_id = update.get("chat_id")


        message = update.get(
            "new_message",
            {}
        )


        text = message.get(
            "text",
            ""
        )


        print("Message:", text)



        user = get_user(chat_id)


        if user is None:

            add_user(chat_id)

            user = get_user(chat_id)



        # شروع
        if text == "/start":


            send_keypad(
                chat_id,
                "🎮 به Bangame خوش آمدی!\n\n"
                "یک گزینه انتخاب کن 👇",
                [
                    [
                        "🎮 بازی‌ها",
                        "👤 پروفایل"
                    ],
                    [
                        "🪙 کیف پول",
                        "🎁 جایزه روزانه"
                    ]
                ]
            )



        # پروفایل
        elif text == "👤 پروفایل":


            _, coins, level, xp = user


            send_message(
                chat_id,
                "👤 پروفایل Bangame\n\n"
                f"🪙 سکه: {coins}\n"
                f"⭐ Level: {level}\n"
                f"✨ XP: {xp}"
            )



        # بازی ها
        elif text == "🎮 بازی‌ها":


            send_keypad(
                chat_id,
                "🎮 بازی‌ها را انتخاب کن:",
                [
                    [
                        "✂️ سنگ کاغذ قیچی",
                        "🔢 حدس عدد"
                    ],
                    [
                        "🚪 خروج"
                    ]
                ]
            )



        # شروع RPS
        elif text == "✂️ سنگ کاغذ قیچی":


            games[chat_id] = "rps"


            send_keypad(
                chat_id,
                "✂️ سنگ کاغذ قیچی\n\n"
                "انتخاب کن:",
                [
                    [
                        "🪨 سنگ",
                        "📄 کاغذ"
                    ],
                    [
                        "✂️ قیچی",
                        "🚪 خروج"
                    ]
                ]
            )



        # بازی RPS
        elif games.get(chat_id) == "rps" and text in [
            "🪨 سنگ",
            "📄 کاغذ",
            "✂️ قیچی"
        ]:


            bot = random.choice(
                [
                    "🪨 سنگ",
                    "📄 کاغذ",
                    "✂️ قیچی"
                ]
            )


            if text == bot:

                result = "🤝 مساوی شد!"



            elif (
                (text == "🪨 سنگ" and bot == "✂️ قیچی")
                or
                (text == "📄 کاغذ" and bot == "🪨 سنگ")
                or
                (text == "✂️ قیچی" and bot == "📄 کاغذ")
            ):

                add_coins(chat_id, 100)

                result = "🎉 بردی!\n🪙 +100 سکه"



            else:

                result = "😢 باختی!"



            send_message(
                chat_id,
                f"انتخاب تو: {text}\n"
                f"انتخاب من: {bot}\n\n"
                f"{result}"
            )



        # شروع حدس عدد
        elif text == "🔢 حدس عدد":


            games[chat_id] = {
                "game": "guess",
                "number": random.randint(1,10)
            }


            send_keypad(
                chat_id,
                "🔢 یک عدد بین 1 تا 10 حدس بزن:",
                [
                    [
                        "1",
                        "2",
                        "3"
                    ],
                    [
                        "4",
                        "5",
                        "6"
                    ],
                    [
                        "7",
                        "8",
                        "9"
                    ],
                    [
                        "10",
                        "🚪 خروج"
                    ]
                ]
            )



        # حدس عدد
        elif isinstance(games.get(chat_id), dict) and games[chat_id].get("game") == "guess":


            if text.isdigit():


                guess = int(text)

                answer = games[chat_id]["number"]



                if guess == answer:

                    add_coins(chat_id, 200)

                    send_message(
                        chat_id,
                        "🎉 درست حدس زدی!\n"
                        "🪙 +200 سکه"
                    )


                    games.pop(chat_id)



                else:

                    send_message(
                        chat_id,
                        "❌ اشتباه بود!\n"
                        "دوباره تلاش کن"
                    )



        # کیف پول
        elif text == "🪙 کیف پول":


            _, coins, _, _ = user


            send_message(
                chat_id,
                f"🪙 موجودی شما: {coins}"
            )



        # جایزه
        elif text == "🎁 جایزه روزانه":


            add_coins(chat_id, 50)


            send_message(
                chat_id,
                "🎁 جایزه گرفتی!\n"
                "🪙 +50 سکه"
            )



        # خروج
        elif text == "🚪 خروج":


            games.pop(
                chat_id,
                None
            )


            send_keypad(
                chat_id,
                "🏠 برگشتی به منوی اصلی",
                [
                    [
                        "🎮 بازی‌ها",
                        "👤 پروفایل"
                    ],
                    [
                        "🪙 کیف پول",
                        "🎁 جایزه روزانه"
                    ]
                ]
            )



        else:

            send_message(
                chat_id,
                "❌ دستور پیدا نشد"
            )



    except Exception as e:

        print("ERROR:", e)



    return {
        "ok": True
    }