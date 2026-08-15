from fastapi import FastAPI, Request
import time
import socket

from handlers import leaderboard
from handlers import typing as typing_handler
from handlers import memory
from handlers import word as word_handler
from handlers import math_game
from handlers import reaction
from handlers import reaction as reaction_handler
from handlers import nickname

from handlers import minesweeper as minesweeper_handler

from handlers.menu import (
    main_menu,
    games_menu
)

from games import reaction as reaction_game

from rubika import (
    send_message,
    send_keypad,
    edit_chat_keypad
)

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
    create_memory_online_room,
    create_uno_room,
    request_join,
    receive_room_code,
    exit_room
)

from handlers import (
    tictactoe as ttt_handler,
    rps as rps_handler,
    esm_famil as esm_handler,
    memory_online as memory_online_handler,
    uno as uno_handler
)

from rooms.manager import get_player_room


# ==========================================
# APP
# ==========================================

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
# Cache کاربران
# ==========================================

user_cache = set()

nickname_cache = set()


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

        aux_data = msg.get("aux_data") or {}

        button_id = aux_data.get("button_id")

        if button_id:

            print(
                f"🔘 {button_id}"
            )


        # ==========================================
        # بررسی کاربر
        # ==========================================

        if chat_id not in user_cache:

            user = get_user(chat_id)

            if not user:

                add_user(chat_id)

                user = get_user(chat_id)

            user_cache.add(chat_id)

            if user and user[1]:

                nickname_cache.add(chat_id)


        # ==========================================
        # سیستم Nickname
        # ==========================================

        if (
            chat_id not in nickname.waiting
            and chat_id not in nickname_cache
        ):

            nickname.start(chat_id)

            return {
                "ok": True
            }


        if chat_id in nickname.waiting:

            nickname.save(
                chat_id,
                text
            )

            nickname_cache.add(chat_id)

            return {
                "ok": True
            }


        # ==========================================
        # ماین‌یاب
        # ==========================================

        if chat_id in minesweeper_handler.active_games:

            # --------------------------------------
            # کنترل‌های ماین‌یاب
            # --------------------------------------

            if (
                button_id
                and button_id.startswith(
                    "minesweeper_"
                )
            ):

                minesweeper_handler.handle_control(
                    chat_id,
                    button_id
                )

                return {
                    "ok": True
                }


            # --------------------------------------
            # خانه‌های زمین
            # --------------------------------------

            if (
                button_id
                and button_id.startswith(
                    "mine_"
                )
            ):

                parts = button_id.split("_")

                if len(parts) == 3:

                    try:

                        row = int(
                            parts[1]
                        )

                        col = int(
                            parts[2]
                        )

                        minesweeper_handler.handle_cell(
                            chat_id,
                            row,
                            col
                        )

                    except ValueError:

                        pass

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

        room = get_player_room(
            chat_id
        )

        if room:

            # ==========================================
            # دوز
            # ==========================================

            if (
                room.game == "tictactoe"
                and room.started
            ):

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

            if (
                room.game == "rps"
                and room.started
            ):

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
            # حافظه آنلاین
            # ==========================================

            if room.game == "memory_online":

                if text == "▶️ شروع بازی":

                    memory_online_handler.start_by_host(
                        room,
                        chat_id
                    )

                    return {
                        "ok": True
                    }


                if text == "🚪 خروج از بازی":

                    memory_online_handler.exit_game(
                        room,
                        chat_id
                    )

                    return {
                        "ok": True
                    }


                if room.started:

                    memory_online_handler.handle_answer(
                        room,
                        chat_id,
                        text
                    )

                    return {
                        "ok": True
                    }


            # ==========================================
            # UNO
            # ==========================================

            if room.game == "uno":

                if button_id and (
                    button_id.startswith("uno_")
                ):

                    uno_handler.handle(
                        room,
                        chat_id,
                        button_id
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

            states.pop(
                chat_id,
                None
            )

            main_menu(
                chat_id
            )

            return {
                "ok": True
            }


        # ==========================================
        # منوی اصلی
        # ==========================================

        elif text == "🎮 بازی‌ها":

            games_menu(
                chat_id
            )

            return {
                "ok": True
            }


        # ==========================================
        # پروفایل
        # ==========================================

        elif text == "👤 پروفایل":

            show_profile(
                chat_id
            )

            return {
                "ok": True
            }


        # ==========================================
        # تغییر لقب
        # ==========================================

        elif text == "✏️ تغییر لقب":

            nickname.change_start(
                chat_id
            )

            return {
                "ok": True
            }


        # ==========================================
        # تست XP
        # ==========================================

        elif text == "🧪 تست XP":

            from database import add_xp

            add_xp(
                chat_id,
                110
            )

            show_profile(
                chat_id
            )

            return {
                "ok": True
            }


        # ==========================================
        # کیف پول
        # ==========================================

        elif text == "🪙 کیف پول":

            show_wallet(
                chat_id
            )

            return {
                "ok": True
            }


        # ==========================================
        # جایزه روزانه
        # ==========================================

        elif text == "🎁 جایزه روزانه":

            daily(
                chat_id
            )

            return {
                "ok": True
            }


        # ==========================================
        # کافه بازی
        # ==========================================

        elif text == "🎮☕ کافه بازی 🎉":

            open_room_menu(
                chat_id
            )

            return {
                "ok": True
            }


        # ==========================================
        # ساخت اتاق
        # ==========================================

        elif text == "➕ ساخت اتاق":

            open_create_room(
                chat_id
            )

            return {
                "ok": True
            }


        # ==========================================
        # ورود به اتاق
        # ==========================================

        elif text == "🚪 ورود به اتاق":

            request_join(
                chat_id
            )

            return {
                "ok": True
            }


        # ==========================================
        # خروج از اتاق
        # ==========================================

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
        # ساخت اتاق سنگ کاغذ قیچی
        # ==========================================

        elif text == "✂️ سنگ کاغذ قیچی":

            create_rps_room(
                chat_id
            )

            return {
                "ok": True
            }


        # ==========================================
        # ساخت اتاق دوز
        # ==========================================

        elif text == "⭕ دوز":

            create_tictactoe_room(
                chat_id
            )

            return {
                "ok": True
            }


        # ==========================================
        # ساخت اتاق اسم و فامیل
        # ==========================================

        elif text == "✍️ اسم و فامیل":

            create_esm_famil_room(
                chat_id
            )

            return {
                "ok": True
            }


        # ==========================================
        # ساخت اتاق حافظه آنلاین
        # ==========================================

        elif text == "🧠 حافظه آنلاین":

            create_memory_online_room(
                chat_id
            )

            return {
                "ok": True
            }


        # ==========================================
        # ساخت اتاق UNO
        # ==========================================

        elif text == "🃏 UNO":

            create_uno_room(
                chat_id
            )

            return {
                "ok": True
            }


        # ==========================================
        # مین‌روب
        # ==========================================

        elif text == "💣 مین‌روب":

            minesweeper_handler.show_difficulty_menu(
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
        # انتخاب سطح ماین‌یاب
        # ==========================================

        elif text in (
            "🟢 آسان",
            "🟡 متوسط",
            "🔴 سخت"
        ):

            difficulty_map = {
                "🟢 آسان": "easy",
                "🟡 متوسط": "medium",
                "🔴 سخت": "hard"
            }

            minesweeper_handler.start(
                chat_id,
                difficulty_map[text]
            )

            return {
                "ok": True
            }


        # ==========================================
        # تست Edit Chat Keypad
        # ==========================================

        elif text == "🧪 تست ویرایش کیپد":

            buttons = [
                [
                    {
                        "id": "test_1",
                        "text": "🟦 دکمه اول"
                    },
                    {
                        "id": "test_2",
                        "text": "🟥 دکمه دوم"
                    }
                ]
            ]

            send_keypad(
                chat_id,
                "🧪 تست Chat Keypad\n\nاین کیپد باید قابل ویرایش باشد.",
                buttons
            )

            edit_chat_keypad(
                chat_id,
                [
                    [
                        {
                            "id": "test_1_new",
                            "text": "✅ دکمه تغییر کرد"
                        },
                        {
                            "id": "test_2_new",
                            "text": "🔵 دکمه دوم"
                        }
                    ]
                ]
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



def test_rubika_connection():

    host = "botapi.rubika.ir"

    try:
        ip = socket.gethostbyname(host)

        print(f"🌐 Rubika DNS → {ip}")

        sock = socket.create_connection(
            (host, 443),
            timeout=10
        )

        sock.close()

        print("🔗 Rubika HTTPS → CONNECTED")

        return True

    except socket.gaierror:

        print("❌ Rubika DNS → FAILED")

        return False

    except socket.timeout:

        print("⏱️ Rubika HTTPS → TIMEOUT")

        return False

    except Exception:

        print("❌ Rubika HTTPS → FAILED")

        return False


if __name__ == "__main__":

    test_rubika_connection()

    import uvicorn

    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=False
    )


# ==========================================
# Run Server
# ==========================================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=False
    )