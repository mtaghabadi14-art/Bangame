from rubika import (
    send_keypad,
    edit_chat_keypad,
    send_message
)


# ==========================================
# دسته‌بندی‌ها
# ==========================================

CATEGORIES = [
    "👤 اسم",
    "🏠 فامیل",
    "🍎 میوه",
    "🍔 غذا",
    "🎨 رنگ",
    "📦 اشیا",
    "🐶 حیوان",
    "🌍 شهر یا کشور",
    "🖐 اعضای بدن",
    "🎬 فیلم یا سریال"
]


# ==========================================
# ساخت کی‌پد دسته‌ها
# ==========================================

def build_categories_keyboard():

    keyboard = []

    for category in CATEGORIES:

        keyboard.append([
            category
        ])

    keyboard.append([
        "✅ آماده‌ام"
    ])

    keyboard.append([
        "🚪 خروج از بازی"
    ])

    return keyboard


# ==========================================
# نمایش دسته‌ها
# فقط هنگام شروع بازی
# ==========================================

def show_categories(chat_id):

    keyboard = build_categories_keyboard()

    send_keypad(
        chat_id,
        "📚 یکی از دسته‌ها را انتخاب کن:",
        keyboard
    )


# ==========================================
# بروزرسانی همان Chat Keypad
# ==========================================

def update_categories(chat_id):

    keyboard = build_categories_keyboard()

    edit_chat_keypad(
        chat_id,
        keyboard
    )


# ==========================================
# بعد از ثبت جواب
# ==========================================

def show_after_save(chat_id):

    keyboard = build_categories_keyboard()

    edit_chat_keypad(
        chat_id,
        keyboard
    )


# ==========================================
# درخواست جواب
# ==========================================

def ask_for_answer(
    chat_id,
    category,
    letter
):

    keyboard = [
        [
            "⬅️ انصراف"
        ]
    ]

    # همان کی‌پد را تغییر می‌دهیم
    edit_chat_keypad(
        chat_id,
        keyboard
    )

    send_message(
        chat_id,
        (
            f"🔤 حرف: {letter}\n\n"
            f"✍️ جواب بخش {category} را ارسال کن."
        )
    )


# ==========================================
# حالت انتظار
# ==========================================

def show_waiting(chat_id):

    keyboard = [
        [
            "🚪 خروج از بازی"
        ]
    ]

    edit_chat_keypad(
        chat_id,
        keyboard
    )