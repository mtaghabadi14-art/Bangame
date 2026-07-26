import time
import threading

from rubika import (
    send_keypad,
    send_message
)

from games import reaction

from database import add_coins
from level import give_xp


waiting = {}


# ==========================================
# شروع بازی
# ==========================================

def start(chat_id):

    result = reaction.start(chat_id)


    send_keypad(

        chat_id,

        result["message"],

        [

            [
                "⚡ آماده‌ام"
            ],

            [
                "🚪 خروج از بازی"
            ]

        ]

    )


    # زمان تصادفی انتظار

    def timer():

        time.sleep(
            result["wait"]
        )


        if chat_id in reaction.games:

            reaction.begin(chat_id)


            send_keypad(

                chat_id,

                "🟢 الان!!!\n\n"
                "سریع بزن!",

                [

                    [
                        "⚡ زدم!"
                    ],

                    [
                        "🚪 خروج از بازی"
                    ]

                ]

            )


    threading.Thread(

        target=timer

    ).start()



# ==========================================
# بررسی پیام
# ==========================================

def check(chat_id, text):


    if text == "⚡ آماده‌ام":


        send_message(
            chat_id,
            "⏳ صبر کن..."
        )

        return



    if text == "⚡ زدم!":


        result = reaction.play(chat_id)


        if result["status"] == "wait":

            send_message(

                chat_id,

                "⏳ هنوز علامت سبز نیومده!"

            )

            return



        if result["status"] == "success":


            reaction_time = result["time"]


            coins = 10

            xp = 5


            add_coins(

                chat_id,

                coins

            )


            give_xp(

                chat_id,

                xp

            )


            send_keypad(

                chat_id,

                "⚡ نتیجه:\n\n"

                f"⏱ زمان واکنش: {reaction_time} ثانیه\n\n"

                f"{reaction.get_result(reaction_time)}\n\n"

                f"🪙 +{coins} سکه\n"

                f"⭐ +{xp} XP",

                [

                    [
                        "⚡ دوباره بازی کن"
                    ],

                    [
                        "🚪 خروج از بازی"
                    ]

                ]

            )

            return



    if text == "⚡ دوباره بازی کن":

        start(chat_id)

        return



    if text == "🚪 خروج از بازی":

        reaction.exit(chat_id)


        from handlers.menu import games_menu

        send_message(

            chat_id,

            "🚪 از بازی واکنش سریع خارج شدی."

        )


        games_menu(chat_id)

        return
    # ==========================================
# پاکسازی بازی‌های تمام شده
# ==========================================

def cleanup(chat_id):

    reaction.exit(chat_id)



# ==========================================
# تست وضعیت بازی
# ==========================================

def is_playing(chat_id):

    return chat_id in reaction.games