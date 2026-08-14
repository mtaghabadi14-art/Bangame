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
# ساخت کی‌پد ۳×۴
# ==========================================

def build_categories_keyboard():

    return [
        [
            "👤 اسم",
            "🏠 فامیل",
            "🍎 میوه"
        ],
        [
            "🍔 غذا",
            "🎨 رنگ",
            "📦 اشیا"
        ],
        [
            "🐶 حیوان",
            "🌍 شهر یا کشور",
            "🖐 اعضای بدن"
        ],
        [
            "🎬 فیلم یا سریال",
            "✅ آماده‌ام",
            "🚪 خروج از بازی"
        ]
    ]


# ==========================================
# نمایش دسته‌بندی‌ها
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
# بروزرسانی دسته‌بندی‌ها
# بدون پیام جدید
# ==========================================

def update_categories(chat_id):

    keyboard = build_categories_keyboard()

    return edit_chat_keypad(
        chat_id,
        keyboard
    )

# ==========================================
# نمایش دوباره دسته‌بندی‌ها
# ==========================================

def show_categories_again(chat_id):

    return update_categories(
        chat_id
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
# بعد از ثبت جواب
# ==========================================

def show_after_save(chat_id):

    keyboard = build_categories_keyboard()

    return edit_chat_keypad(
        chat_id,
        keyboard
    )


# ==========================================
# درخواست نوشتن جواب
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

    edit_chat_keypad(
        chat_id,
        keyboard
    )

    send_keypad(
        chat_id,
        (
            f"🔤 حرف: {letter}\n\n"
            f"✍️ جواب بخش {category} را ارسال کن."
        ),
        keyboard
    )


# ==========================================
# وقتی آماده شد
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