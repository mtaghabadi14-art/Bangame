from fastapi import FastAPI, Request
from rubika import send_message
from database import create_tables, add_user, get_user


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


        if update.get("type") == "NewMessage":


            chat_id = update.get("chat_id")


            text = update.get(
                "new_message",
                {}
            ).get(
                "text",
                ""
            )


            print("Message:", text)



            if text == "/start":


                user = get_user(chat_id)


                if user is None:

                    add_user(chat_id)


                    send_message(
                        chat_id,
                        "🎮 خوش آمدی به Bangame!\n\n"
                        "✅ حساب تو ساخته شد\n"
                        "🪙 1000 سکه هدیه گرفتی\n"
                        "⭐ Level: 1\n"
                        "✨ XP: 0\n\n"
                        "/profile"
                    )


                else:

                    send_message(
                        chat_id,
                        "👋 دوباره خوش آمدی به Bangame!\n\n"
                        "🎮 حساب تو آماده است\n\n"
                        "/profile"
                    )



            elif text == "/profile":


                user = get_user(chat_id)


                if user:

                    _, coins, level, xp = user


                    send_message(
                        chat_id,
                        "👤 پروفایل Bangame\n\n"
                        f"🪙 سکه: {coins}\n"
                        f"⭐ Level: {level}\n"
                        f"✨ XP: {xp}"
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