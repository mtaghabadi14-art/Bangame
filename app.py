from fastapi import FastAPI, Request
import time

from rubika import (
    send_message,
    remove_keypad
)

from database import (
    create_tables,
    add_user,
    get_user
)

from handlers.menu import (
    main_menu,
    games_menu,
    room_menu,
    create_room_menu
)

from handlers.profile import (
    show_profile,
    show_wallet,
    daily
)

from handlers.guess import (
    start as guess_start,
    check as guess_check
)

from handlers.dice import (
    start as dice_start,
    roll as dice_roll
)

from handlers.rooms import (
    open_room_menu,
    open_create_room,
    create_rps_room,
    create_tictactoe_room,
    request_join,
    receive_room_code,
    exit_room
)


# ==========================================
# Bangame
# ==========================================

app = FastAPI()

create_tables()

# وضعیت بازیکنان
states = {}


# ==========================================
# Home
# ==========================================

@app.get("/")
def home():

    return {
        "status": "Bangame Online 🚀"
    }


# ==========================================
# Webhook
# ==========================================

@app.post("/receiveUpdate")
async def receive_update(request: Request):

    start_time = time.time()

    data = await request.json()

    print("\n==============================")
    print("📩 New Update")
    print(data)
    print("==============================\n")

    try:

        update = data.get("update", {})

        if update.get("type") != "NewMessage":

            return {
                "ok": True
            }

        chat_id = update["chat_id"]

        msg = update["new_message"]

        text = (
            msg.get("aux_data", {}).get("button_id")
            or msg.get("text", "")
        ).strip()

        # ثبت کاربر
        if not get_user(chat_id):

            add_user(chat_id)

        # اگر کاربر در حال وارد کردن کد اتاق باشد
        if receive_room_code(chat_id, text):

            return {
                "ok": True
            }
                # ==========================================
        # Start
        # ==========================================

        if text == "/start":

            states.pop(chat_id, None)

            main_menu(chat_id)


        # ==========================================
        # Main Menu
        # ==========================================

        elif text == "🎮 بازی‌ها":

            games_menu(chat_id)


        elif text == "🏠 اتاق بازی":

            open_room_menu(chat_id)


        elif text == "👤 پروفایل":

            show_profile(chat_id)


        elif text == "🪙 کیف پول":

            show_wallet(chat_id)


        elif text == "🎁 جایزه روزانه":

            daily(chat_id)


        # ==========================================
        # Room Menu
        # ==========================================

        elif text == "➕ ساخت اتاق":

            open_create_room(chat_id)


        elif text == "🚪 ورود به اتاق":

            request_join(chat_id)


        elif text == "🚪 خروج":

            exit_room(chat_id)


        # ==========================================
        # Create Games
        # ==========================================

        elif text == "✂️ سنگ کاغذ قیچی":

            create_rps_room(chat_id)


        elif text == "⭕ دوز":

            create_tictactoe_room(chat_id)
                    # ==========================================
        # Guess Number
        # ==========================================

        elif text == "🔢 حدس عدد":

            guess_start(
                states,
                chat_id
            )


        elif (
            chat_id in states
            and states[chat_id].get("game") == "guess"
        ):

            guess_check(
                states,
                chat_id,
                text
            )


        # ==========================================
        # Dice
        # ==========================================

        elif text == "🎲 تاس":

            dice_start(chat_id)


        elif text == "🎲 ریختن تاس":

            dice_roll(chat_id)


        # ==========================================
        # Unknown Command
        # ==========================================

        else:

            send_message(
                chat_id,
                "❓ دستور را متوجه نشدم."
            )
    except Exception as e:

        print("\n========== ERROR ==========")
        print(e)
        print("===========================\n")

        try:

            send_message(
                chat_id,
                "❌ خطایی در ربات رخ داد."
            )

        except Exception as err:

            print("Send Error:", err)

    end_time = time.time()

    print(
        f"⏱ Process Time: {end_time - start_time:.2f}s"
    )

    return {
        "ok": True
    }
# ==========================================
# Run
# ==========================================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )