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


            if text == "/start":


                user = get_user(chat_id)


                if user is None:

                    add_user(chat_id)

                    message = (
                        "🎮 خوش آمدی به Bangame!\n\n"
                        "✅ حساب تو ساخته شد\n"
                        "🪙 1000 سکه هدیه گرفتی\n"
                        "⭐ Level: 1\n\n"
                        "به زودی بازی‌ها فعال می‌شوند 🚀"
                    )


                else:

                    message = (
                        "👋 دوباره خوش آمدی به Bangame!\n\n"
                        "حساب تو آماده است 🎮"
                    )



                result = send_message(
                    chat_id,
                    message
                )


                print("SEND RESULT:")
                print(result)



            else:


                result = send_message(
                    chat_id,
                    "دستور نامعتبر است ❌"
                )


                print(result)



    except Exception as e:

        print("ERROR:")
        print(e)



    return {
        "ok": True
    }