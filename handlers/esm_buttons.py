from rubika import (
    send_keypad,
    edit_chat_keypad
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
# ساخت کی‌پد دسته‌بندی‌ها
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
# نمایش اولیه دسته‌ها
# فقط یک بار پیام جدید می‌سازد
# ==========================================

def show_categories(chat_id):

    keyboard = build_categories_keyboard()

    return send_keypad(
        chat_id,
        "📚 یکی از دسته‌ها را انتخاب کن:",
        keyboard
    )


# ==========================================
# بازگرداندن کی‌پد دسته‌ها
# بدون پیام جدید
# ==========================================

def update_categories(chat_id):

    keyboard = build_categories_keyboard()

    return edit_chat_keypad(
        chat_id,
        keyboard
    )


# ==========================================
# بعد از ثبت جواب
# بدون ارسال پیام جدید
# ==========================================

def show_after_save(chat_id):

    keyboard = build_categories_keyboard()

    return edit_chat_keypad(
        chat_id,
        keyboard
    )


# ==========================================
# حالت نوشتن جواب
# ==========================================

def show_answer_mode(chat_id):

    return edit_chat_keypad(
        chat_id,
        [
            [
                "⬅️ انصراف"
            ]
        ]
    )


# ==========================================
# بعد از آماده شدن
# ==========================================

def show_waiting(chat_id):

    return edit_chat_keypad(
        chat_id,
        [
            [
                "🚪 خروج از بازی"
            ]
        ]
    )


# ==========================================
# بازگشت از حالت نوشتن جواب
# ==========================================

def show_categories_again(chat_id):

    return update_categories(
        chat_id
    )