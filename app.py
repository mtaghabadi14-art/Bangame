from fastapi import FastAPI, Request
from rubika import send_message, send_keypad
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


            message = update.get(
                "new_message",
                {}
            )


            text = message.get(
                "text",
                ""
            )


            print("Message:", text)



            # ساخت کاربر
            if get_user(chat_id) is None:
                add_user(chat_id)



            if text == "/start":


                send_keypad(
                    chat_id,
                    "🎮 به Bangame خوش آمدی!\n\n"
                    "از منوی زیر انتخاب کن 👇"
                )



            elif text == "/profile" or text == "👤 پروفایل":


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



            elif text == "🎮 بازی‌ها":


                send_message(
                    chat_id,
                    "🎮 بازی‌ها\n\n"
                    "به زودی اضافه می‌شوند 🚀"
                )



            elif text == "🪙 کیف پول":


                user = get_user(chat_id)


                _, coins, _, _ = user


                send_message(
                    chat_id,
                    f"🪙 موجودی شما: {coins}"
                )



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

        print("ERROR:", e)



    return {
        "ok": True
    }