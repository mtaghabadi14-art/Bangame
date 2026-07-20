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

            new_message = update.get(
                "new_message",
                {}
            )

            text = new_message.get(
                "text",
                ""
            )


            print("Message:", text)



            # ثبت کاربر
            if get_user(chat_id) is None:
                add_user(chat_id)



            # شروع
            if text == "/start":

                send_message(
                    chat_id,
                    "🎮 خوش آمدی به Bangame!\n\n"
                    "🪙 1000 سکه اولیه گرفتی\n"
                    "⭐ Level: 1\n\n"
                    "برای دیدن پروفایل بزن:\n"
                    "/profile"
                )



            # پروفایل
            elif text == "/profile":

                user = get_user(chat_id)


                if user:

                    user_id, coins, level, xp = user


                    send_message(
                        chat_id,
                        "👤 پروفایل Bangame\n\n"
                        f"🪙 سکه: {coins}\n"
                        f"⭐ Level: {level}\n"
                        f"✨ XP: {xp}\n\n"
                        "🎮 بازی‌ها به زودی فعال می‌شوند"
                    )


            else:

                send_message(
                    chat_id,
                    "❌ دستور پیدا نشد\n\n"
                    "دستورات:\n"
                    "/start\n"
                    "/profile"
                )



    except Exception as e:

        print("ERROR:")
        print(e)



    return {
        "ok": True
    }