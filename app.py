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
            print("Chat ID:", chat_id)


            if text == "/start":

                result = send_message(
                    chat_id,
                    "🎮 سلام!\n\n"
                    "به Bangame خوش آمدی 🚀\n\n"
                    "ربات آماده است 😎"
                )

                print("SEND RESULT:")
                print(result)


            else:

                result = send_message(
                    chat_id,
                    "پیامت دریافت شد ✅"
                )

                print("SEND RESULT:")
                print(result)


    except Exception as e:

        print("ERROR:")
        print(e)


    return {
        "ok": True
    }