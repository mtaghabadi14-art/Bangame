from fastapi import FastAPI, Request
from rubika import send_message, send_keypad
from database import create_tables, add_user, get_user, add_coins
import random


app = FastAPI()

create_tables()


# ذخیره وضعیت بازی‌ها
games = {}



@app.get("/")
def home():

    return {
        "status": "Bangame Bot is running 🚀"
    }



def main_menu(chat_id):

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



def games_menu(chat_id):

    send_keypad(
        chat_id,
        "🎮 بازی‌ها:",
        [
            [
                "✂️ سنگ کاغذ قیچی",
                "🔢 حدس عدد"
            ],
            [
                "🎲 تاس",
                "🚪 خروج"
            ]
        ]
    )



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

            main_menu(chat_id)



        # منوی بازی‌ها
        elif text == "🎮 بازی‌ها":

            games_menu(chat_id)



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



        # کیف پول
        elif text == "🪙 کیف پول":


            _, coins, _, _ = user


            send_message(
                chat_id,
                f"🪙 موجودی شما: {coins}"
            )



        # جایزه روزانه
        elif text == "🎁 جایزه روزانه":


            add_coins(
                chat_id,
                50
            )


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


            main_menu(chat_id)



        # شروع سنگ کاغذ قیچی
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



        # شروع حدس عدد
        elif text == "🔢 حدس عدد":


            games[chat_id] = {
                "type": "guess",
                "number": random.randint(1,100)
            }


            send_message(
                chat_id,
                "🔢 حدس عدد شروع شد!\n\n"
                "یک عدد بین 1 تا 100 بفرست.\n"
                "من می‌گویم بزرگتر است یا کوچکتر 😉"
            )



        # شروع تاس
        elif text == "🎲 تاس":


            games[chat_id] = "dice"


            send_keypad(
                chat_id,
                "🎲 آماده‌ای؟\n"
                "برای ریختن تاس دکمه را بزن:",
                [
                    [
                        "🎲 ریختن تاس"
                    ],
                    [
                        "🚪 خروج"
                    ]
                ]
            )