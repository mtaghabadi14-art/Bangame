from fastapi import FastAPI, Request
from rubika import send_message

app = FastAPI()


@app.get("/")
def home():
    return {
        "status": "Bangame Bot is running 🚀"
    }


@app.post("/webhook")
async def webhook(request: Request):

    data = await request.json()

    print(data)

    try:

        if data["type"] == "NewMessage":

            chat_id = data["chat_id"]

            text = data["new_message"].get("text", "")


            if text == "/start":

                send_message(
                    chat_id,
                    "🎮 سلام!\n\n"
                    "به Bangame خوش آمدی 🚀\n\n"
                    "بازی‌ها به زودی آماده می‌شوند 😎"
                )


            else:

                send_message(
                    chat_id,
                    "پیامت دریافت شد ✅"
                )


    except Exception as e:
        print("ERROR:", e)


    return {"ok": True}