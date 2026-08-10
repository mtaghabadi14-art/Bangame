from fastapi import FastAPI, Request
import time

from handlers import leaderboard
from handlers import typing as typing_handler
from handlers import memory
from handlers import word as word_handler
from handlers import math_game
from handlers import reaction
from handlers import reaction as reaction_handler
from handlers import nickname

from handlers.menu import (
    main_menu,
    games_menu
)

from games import reaction as reaction_game

from rubika import send_message

from database import (
    create_tables,
    add_typing_columns,
    add_user,
    get_user,
    set_nickname
)

from handlers.profile import (
    show_profile,
    show_wallet,
    daily
)

from handlers.guess import (
    start as guess_start,
    check as guess_check,
    exit as guess_exit
)

from handlers.dice import (
    start as dice_start,
    roll as dice_roll,
    exit as dice_exit
)

from handlers.rooms import (
    open_room_menu,
    open_create_room,
    create_rps_room,
    create_tictactoe_room,
    create_esm_famil_room,
    request_join,
    receive_room_code,
    exit_room
)

from handlers import (
    tictactoe as ttt_handler,
    rps as rps_handler,
    esm_famil as esm_handler
)

from rooms.manager import get_player_room


print("########## APP.PY LOADED ##########")


app = FastAPI()


# ==========================================
# ساخت جدول‌ها
# ==========================================

create_tables()
add_typing_columns()


# ==========================================
# State ها
# ==========================================

states = {}

waiting_for_nickname = set()


# ==========================================
# Home
# ==========================================

@app.get("/")
def home():

    return {
        "status": "Vexon Online 🚀"
    }


# ==========================================
# دریافت Update
# ==========================================

@app.post("/receiveUpdate")
async def receive_update(request: Request):

    start_time = time.time()

    chat_id = None

    try:

        # ==========================================
        # دریافت اطلاعات
        # ==========================================

        data = await request.json()

        print("\n========== UPDATE ==========")
        print(data)
        print("============================\n")

        update = data.get(
            "update",
            {}
        )

        if update.get("type") != "NewMessage":

            return {
                "ok": True
            }

        chat_id = update["chat_id"]

        msg = update["new_message"]

        text = msg.get(
            "text",
            ""
        ).strip()

        button_id = (
            msg.get("aux_data", {})
            .get("button_id")
        )

        print("TEXT:", text)
        print("BUTTON_ID:", button_id)

        print("TEXT repr:", repr(text))
        print("BUTTON repr:", repr(button_id))


        # ==========================================
        # گرفتن User فقط یک بار
        # ==========================================

        user = get_user(chat_id)

        if not user:

            add_user(chat_id)

            user = get_user(chat_id)


        print("========== DEBUG ==========")
        print("USER FROM DB:", user)
        print("NICK WAITING:", nickname.waiting)
        print("===========================")


        # ==========================================
        # سیستم Nickname
        # ==========================================

        if (
            chat_id not in nickname.waiting
            and not user[1]
        ):

            print("➡️ START NICKNAME FLOW")

            nickname.start(chat_id)

            return {
                "ok": True
            }


        elif chat_id in nickname.waiting:

            nickname.save(
                chat_id,
                text
            )

            return {
                "ok": True
            }


        # ==========================================
        # ورود به اتاق
        # ==========================================

        if receive_room_code(
            chat_id,
            text
        ):

            return {
                "ok": True
            }


        # ==========================================
        # بازی‌های آنلاین
        # ==========================================

        room = get_player_room(chat_id)

        if room:

            print(
                "ROOM GAME:",
                room.game
            )


            # ==========================================
            # دوز
            # ==========================================

            if room.game == "tictactoe":

                ttt_handler.handle(
                    room,
                    chat_id,
                    {
                        "button_id": button_id
                    }
                )

                return {
                    "ok": True
                }


            # ==========================================
            # سنگ کاغذ قیچی
            # ==========================================

            if room.game == "rps":

                rps_handler.handle(
                    room,
                    chat_id,
                    {
                        "button_id": button_id
                    }
                )

                return {
                    "ok": True
                }


            # ==========================================
            # اسم و فامیل
            # ==========================================

            if room.game == "esm_famil":

                esm_handler.handle(
                    room,
                    chat_id,
                    text
                )

                return {
                    "ok": True
                }


        # ==========================================
        # /start
        # ==========================================

        if (
            text == "/start"
            or text.endswith("/start")
        ):

            print(
                "➡️ START MAIN MENU FLOW"
            )

            states.pop(
                chat_id,
                None
            )

            main_menu(chat_id)

            return {
                "ok": True
            }


        # ==========================================
        # منوی اصلی
        # ==========================================

        elif text == "🎮 بازی‌ها":

            games_menu(chat_id)

            return {
                "ok": True
            }


        elif text == "👤 پروفایل":

            show_profile(chat_id)

            return {
                "ok": True
            }


        elif text == "✏️ تغییر لقب":

            nickname.change_start(
                chat_id
            )

            return {
                "ok": True
            }


        elif text == "🧪 تست XP":

            from database import add_xp

            add_xp(
                chat_id,
                110
            )

            show_profile(chat_id)

            return {
                "ok": True
            }


        elif text == "🪙 کیف پول":

            show_wallet(chat_id)

            return {
                "ok": True
            }


        elif text == "🎁 جایزه روزانه":

            daily(chat_id)

            return {
                "ok": True
            }


        # ==========================================
        # اتاق بازی
        # ==========================================

        elif text == "🏠 اتاق بازی":

            open_room_menu(
                chat_id
            )

            return {
                "ok": True
            }


        elif text == "➕ ساخت اتاق":

            open_create_room(
                chat_id
            )

            return {
                "ok": True
            }


        elif text == "🚪 ورود به اتاق":

            request_join(
                chat_id
            )

            return {
                "ok": True
            }


        elif text == "🚪 خروج از اتاق":

            exit_room(
                chat_id
            )

            return {
                "ok": True
            }


        # ==========================================
        # برگشت
        # ==========================================

        elif text == "برگشت":

            main_menu(
                chat_id
            )

            return {
                "ok": True
            }


        elif text == "برگشت به منوی اصلی":

            main_menu(
                chat_id
            )

            return {
                "ok": True
            }


        elif text == "برگشت به اتاق بازی":

            open_room_menu(
                chat_id
            )

            return {
                "ok": True
            }


        # ==========================================
        # ساخت اتاق
        # ==========================================

        elif text == "✂️ سنگ کاغذ قیچی":

            create_rps_room(
                chat_id
            )

            return {
                "ok": True
            }


        elif text == "⭕ دوز":

            create_tictactoe_room(
                chat_id
            )

            return {
                "ok": True
            }


        elif text == "✍️ اسم و فامیل":

            create_esm_famil_room(
                chat_id
            )

            return {
                "ok": True
            }


        # ==========================================
        # سرعت تایپ
        # ==========================================

        elif text == "⌨️ سرعت تایپ":

            typing_handler.start(
                chat_id
            )

            return {
                "ok": True
            }


        elif (
            chat_id in typing_handler.games
            or chat_id in typing_handler.waiting_level
        ):

            typing_handler.check(
                chat_id,
                text
            )

            return {
                "ok": True
            }


        # ==========================================
        # لیدربورد سرعت تایپ
        # ==========================================

        elif text == "🏆 لیدربورد سرعت تایپ":

            leaderboard.typing(
                chat_id
            )

            return {
                "ok": True
            }


        # ==========================================
        # محاسبات سریع
        # ==========================================

        elif text == "⚡ محاسبات سریع":

            math_game.start(
                chat_id
            )

            return {
                "ok": True
            }


        elif (
            chat_id in math_game.games
            or chat_id in math_game.waiting_level
        ):

            math_game.check(
                chat_id,
                text
            )

            return {
                "ok": True
            }


        # ==========================================
        # بازی حافظه
        # ==========================================

        elif text == "🧠 بازی حافظه":

            memory.start(
                chat_id
            )

            return {
                "ok": True
            }


        elif (
            chat_id in memory.games
            or chat_id in memory.waiting_level
        ):

            memory.check(
                chat_id,
                text
            )

            return {
                "ok": True
            }


        # ==========================================
        # کامل کردن کلمه
        # ==========================================

        elif text == "📝 کامل کردن کلمه":

            word_handler.start(
                chat_id
            )

            return {
                "ok": True
            }


        elif (
            chat_id in word_handler.games
            or chat_id in word_handler.waiting_level
            or text == "🔁 بازی مجدد"
        ):

            word_handler.check(
                chat_id,
                text
            )

            return {
                "ok": True
            }


        # ==========================================
        # واکنش سریع
        # ==========================================

        elif text == "⚡ واکنش سریع":

            reaction_handler.start(
                chat_id
            )

            return {
                "ok": True
            }


        elif chat_id in reaction_game.games:

            reaction_handler.check(
                chat_id,
                text
            )

            return {
                "ok": True
            }


        # ==========================================
        # حدس عدد
        # ==========================================

        elif text == "🔢 حدس عدد":

            guess_start(
                states,
                chat_id
            )

            return {
                "ok": True
            }


        elif (
            chat_id in states
            and states[chat_id].get("game") == "guess"
        ):

            if text == "🚪 خروج از بازی":

                guess_exit(
                    states,
                    chat_id
                )

                return {
                    "ok": True
                }

            guess_check(
                states,
                chat_id,
                text
            )

            return {
                "ok": True
            }


        # ==========================================
        # تاس
        # ==========================================

        elif text == "🎲 تاس":

            dice_start(
                chat_id
            )

            return {
                "ok": True
            }


        elif text == "🎲 ریختن تاس":

            dice_roll(
                chat_id
            )

            return {
                "ok": True
            }


        elif text == "🚪 خروج از بازی":

            dice_exit(
                chat_id
            )

            return {
                "ok": True
            }


        # ==========================================
        # خروج
        # ==========================================

        elif text == "🚪 خروج":

            main_menu(
                chat_id
            )

            return {
                "ok": True
            }


        # ==========================================
        # پیام ناشناخته
        # ==========================================

        else:

            send_message(
                chat_id,
                "❓ دستور را متوجه نشدم."
            )


    except Exception as e:

        print(
            "================================"
        )

        print(
            "ERROR:",
            e
        )

        print(
            "================================"
        )


        try:

            send_message(
                chat_id,
                "❌ خطایی در ربات رخ داد."
            )

        except Exception:

            pass


    # ==========================================
    # زمان پردازش
    # ==========================================

    end_time = time.time()

    print(
        f"⚡ Process Time: "
        f"{round(end_time - start_time, 3)} sec"
    )


    return {
        "ok": True
    }


# ==========================================
# Run Server
# ==========================================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )