import os
import requests

from rubika import send_message, send_keypad


# ==========================================
# تنظیمات PGame
# ==========================================

VEXON_API_KEY = os.getenv(
    "VEXON_RUBIKA_API_KEY"
)

VEXON_STATUS_URL = (
    "https://s.vexongame.workers.dev/api/rubika/status-bot"
)

VEXON_UNLINK_URL = (
    "https://s.vexongame.workers.dev/api/rubika/unlink-bot"
)


# ==========================================
# بررسی وضعیت اتصال
# ==========================================

def get_pgame_connection_status(chat_id):

    if not VEXON_API_KEY:
        return None

    try:

        response = requests.get(

            VEXON_STATUS_URL,

            params={
                "rubika_user_id":
                    str(chat_id)
            },

            headers={
                "X-VEXON-API-KEY":
                    VEXON_API_KEY
            },

            timeout=10
        )

        try:

            result = response.json()

        except ValueError:

            return None

        if (
            response.ok
            and result.get("success")
        ):

            return bool(
                result.get("connected")
            )

        return None

    except requests.exceptions.RequestException as error:

        print(
            "🔌 PGame STATUS ERROR:",
            error
        )

        return None

    except Exception as error:

        print(
            "❌ PGame STATUS ERROR:",
            error
        )

        return None


# ==========================================
# مدیریت اتصال PGame
# ==========================================

def show_pgame_connection(chat_id):

    connected = get_pgame_connection_status(
        chat_id
    )

    if connected is True:

        send_keypad(

            chat_id,

            "🔗 مدیریت اتصال PGame\n\n"
            "🟢 وضعیت اتصال: متصل\n\n"
            "حساب روبیکای تو در حال حاضر "
            "به PGame متصل است.",

            [
                ["🔴 قطع ارتباط با PGame"],
                ["برگشت"]
            ]

        )

        return


    if connected is False:

        send_keypad(

            chat_id,

            "🔗 مدیریت اتصال PGame\n\n"
            "🔴 وضعیت اتصال: متصل نیست\n\n"
            "این حساب روبیکا در حال حاضر "
            "به PGame متصل نیست.",

            [
                ["برگشت"]
            ]

        )

        return


    send_keypad(

        chat_id,

        "🔗 مدیریت اتصال PGame\n\n"
        "⚠️ بررسی وضعیت اتصال با PGame "
        "انجام نشد.\n\n"
        "لطفاً دوباره تلاش کن.",

        [
            ["برگشت"]
        ]

    )


# ==========================================
# تأیید قطع اتصال
# ==========================================

def confirm_pgame_disconnect(chat_id):

    connected = get_pgame_connection_status(
        chat_id
    )

    if connected is False:

        send_message(

            chat_id,

            "🔴 این حساب در حال حاضر "
            "به PGame متصل نیست."

        )

        return


    if connected is None:

        send_message(

            chat_id,

            "⚠️ نتونستم وضعیت اتصال "
            "PGame رو بررسی کنم."

        )

        return


    send_keypad(

        chat_id,

        "⚠️ قطع اتصال PGame\n\n"
        "با قطع اتصال، اطلاعات Bangame "
        "مثل سکه، XP، سطح و اطلاعات مشابه "
        "دیگر از طریق این حساب روبیکا "
        "با PGame هماهنگ نخواهد شد.\n\n"
        "حساب Bangame و اطلاعاتش حذف نمی‌شود.\n\n"
        "مطمئنی که می‌خواهی اتصال را قطع کنی؟",

        [
            ["✅ بله، قطع کن"],
            ["❌ لغو"]
        ]

    )


# ==========================================
# قطع واقعی اتصال
# ==========================================

def disconnect_pgame(chat_id):

    if not VEXON_API_KEY:

        send_message(

            chat_id,

            "❌ کلید اتصال PGame "
            "روی سرور بات تنظیم نشده است."

        )

        return


    try:

        response = requests.post(

            VEXON_UNLINK_URL,

            json={
                "rubika_user_id":
                    str(chat_id)
            },

            headers={
                "X-VEXON-API-KEY":
                    VEXON_API_KEY
            },

            timeout=10
        )


        try:

            result = response.json()

        except ValueError:

            result = {

                "success": False,

                "message":
                    "پاسخ نامعتبر از PGame دریافت شد."

            }


        if (
            response.ok
            and result.get("success")
        ):

            send_keypad(

                chat_id,

                "✅ اتصال PGame با موفقیت قطع شد.\n\n"
                "از این به بعد اطلاعات Bangame "
                "به حساب PGame تو متصل نیست.\n\n"
                "نگران نباش؛ حساب Bangame و اطلاعاتش "
                "حذف نشده و فقط اتصال با PGame قطع شده است. 💚",

                [
                    ["👤 پروفایل"],
                    ["🎮 بازی‌ها"],
                    ["🪙 کیف پول"],
                    ["🎁 جایزه روزانه"]
                ]

            )

        else:

            send_message(

                chat_id,

                "❌ "
                + result.get(
                    "message",
                    "قطع اتصال انجام نشد."
                )

            )


    except requests.exceptions.Timeout:

        send_message(

            chat_id,

            "⏱️ ارتباط با PGame "
            "به پایان رسید. دوباره تلاش کن."

        )


    except requests.exceptions.RequestException as error:

        print(

            "🔌 PGame UNLINK ERROR:",
            error

        )

        send_message(

            chat_id,

            "❌ ارتباط با سرور PGame برقرار نشد."

        )


    except Exception as error:

        print(

            "❌ PGame UNLINK ERROR:",
            error

        )

        send_message(

            chat_id,

            "❌ خطایی هنگام قطع اتصال رخ داد."

        )