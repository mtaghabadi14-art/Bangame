from fastapi import FastAPI, Request
from rubika import send_message


app = FastAPI()



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


            new_message = update.get(
                "new_message",
                {}
            )


            chat_id = update.get(
                "chat_id"
            )


            text = new_message.get(
                "text",
                ""
            )


            print(
                "Message:",
                text
            )


            if text == "/start":


                send_message(
                    chat_id,
                    "🎮 سلام!\n\n"
                    "به Bangame خوش آمدی 🚀\n\n"
                    "ربات آماده است 😎"
                )


            else:


                send_message(
                    chat_id,
                    "پیامت دریافت شد ✅"
                )



    except Exception as e:

        print(
            "ERROR:",
            e
        )


    return {
        "ok": True
    }