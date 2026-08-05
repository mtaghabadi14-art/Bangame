from database import (
    set_nickname,
    get_nickname
)

from handlers.menu import main_menu
from rubika import send_message


waiting = set()


# ==========================================
# شروع گرفتن لقب
# ==========================================

def start(chat_id):

    waiting.add(chat_id)

    send_message(
        chat_id,
        "👋 به Bangame خوش اومدی!\n\n"
        "🏷 لطفاً لقب خودت رو وارد کن."
    )


# ==========================================
# ذخیره لقب
# ==========================================

def check(chat_id, text):

    nickname = text.strip()

    if len(nickname) < 3:

        send_message(
            chat_id,
            "❌ لقب باید حداقل ۳ حرف باشد."
        )

        return


    if len(nickname) > 20:

        send_message(
            chat_id,
            "❌ لقب نباید بیشتر از ۲۰ حرف باشد."
        )

        return


    set_nickname(
        chat_id,
        nickname
    )

    waiting.discard(chat_id)

    send_message(
        chat_id,
        f"✅ لقب شما روی «{nickname}» ذخیره شد."
    )

    main_menu(chat_id)