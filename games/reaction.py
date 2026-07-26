import random
import time


games = {}


# ==========================================
# شروع بازی
# ==========================================

def start(chat_id):

    games[chat_id] = {

        "status": "waiting",

        "start_time": None

    }


    return {

        "message":
            "⚡ واکنش سریع\n\n"
            "آماده باش...\n\n"
            "وقتی 🟢 ظاهر شد سریع دکمه را بزن!",

        "wait": random.uniform(2, 5)

    }



# ==========================================
# شروع شمارش
# ==========================================

def begin(chat_id):

    if chat_id not in games:

        return False


    games[chat_id]["status"] = "ready"


    games[chat_id]["start_time"] = time.time()


    return True

# ==========================================
# بررسی واکنش بازیکن
# ==========================================

def play(chat_id):


    if chat_id not in games:

        return {

            "status": "error",

            "message": "❌ بازی‌ای فعال نیست."

        }



    game = games[chat_id]



    # اگر هنوز زمان شروع نشده

    if game["status"] != "ready":

        return {

            "status": "wait",

            "message":
                "⏳ هنوز وقتش نشده!"

        }



    elapsed = round(

        time.time() - game["start_time"],

        3

    )


    game["status"] = "finished"



    return {

        "status": "success",

        "time": elapsed

    }




# ==========================================
# خروج از بازی
# ==========================================

def exit(chat_id):


    games.pop(

        chat_id,

        None

    )



# ==========================================
# گرفتن رکورد
# ==========================================

def get_result(time):


    if time < 0.3:

        return "🔥 فوق العاده سریع!"

    elif time < 0.6:

        return "⚡ خیلی خوب!"

    elif time < 1:

        return "👍 خوبه!"

    else:

        return "🐢 میشه بهترش کرد!"
