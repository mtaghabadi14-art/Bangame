from fastapi import FastAPI, Request
from rubika import send_message, send_keypad
from database import create_tables, add_user, get_user
import random


app = FastAPI()


create_tables()



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



        # فقط یک بار گرفتن کاربر
        user = get_user(chat_id)



        if user is None:

            add_user(chat_id)

            user = get_user(chat_id)



        # START
        if text == "/start":


            send_keypad(
                chat_id,
                "🎮 به Bangame خوش آمدی!\n\n"
                "از منوی زیر انتخاب کن 👇"
            )



        # PROFILE
        elif text == "/profile" or text == "👤 پروفایل":


            _, coins, level, xp = user


            send_message(
                chat_id,
                "👤 پروفایل Bangame\n\n"
                f"🪙 سکه: {coins}\n"
                f"⭐ Level: {level}\n"
                f"✨ XP: {xp}"
            )



        # GAMES
        elif text == "🎮 بازی‌ها":


            send_message(
                chat_id,
                "🎮 بازی‌ها:\n\n"
                "✂️ سنگ کاغذ قیچی\n\n"
                "برای شروع بزن:\n"
                "/rps"
            )



        # RPS START
        elif text == "/rps":


            send_message(
                chat_id,
                "✂️ سنگ کاغذ قیچی\n\n"
                "انتخاب کن:\n\n"
                "🪨 سنگ\n"
                "📄 کاغذ\n"
                "✂️ قیچی"
            )



        # RPS GAME
        elif text in [
            "🪨 سنگ",
            "📄 کاغذ",
            "✂️ قیچی"
        ]:


            choices = [
                "🪨 سنگ",
                "📄 کاغذ",
                "✂️ قیچی"
            ]


            bot_choice = random.choice(
                choices
            )


            if text == bot_choice:

                result = "🤝 مساوی شد!"


            elif (
                (text == "🪨 سنگ" and bot_choice == "✂️ قیچی")
                or
                (text == "📄 کاغذ" and bot_choice == "🪨 سنگ")
                or
                (text == "✂️ قیچی" and bot_choice == "📄 کاغذ")
            ):

                result = "🎉 بردی!\n🪙 جایزه بعداً اضافه می‌شود"


            else:

                result = "😢 باختی!"



            send_message(
                chat_id,
                f"انتخاب تو: {text}\n"
                f"انتخاب من: {bot_choice}\n\n"
                f"{result}"
            )



        # WALLET
        elif text == "🪙 کیف پول":


            _, coins, level, xp = user


            send_message(
                chat_id,
                f"🪙 موجودی شما: {coins}"
            )



        # DAILY
        elif text == "🎁 جایزه روزانه":


            send_message(
                chat_id,
                "🎁 جایزه روزانه به زودی فعال می‌شود"
            )



        else:


            send_message(
                chat_id,
                "❌ دستور پیدا نشد"
            )



    except Exception as e:

        print("ERROR:")
        print(e)



    return {
        "ok": True
    }