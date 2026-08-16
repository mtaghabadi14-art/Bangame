import re


def normalize_answer(text):
    if not text:
        return ""

    text = str(text).strip()

    # یکسان‌سازی حروف عربی و فارسی
    text = text.replace("ي", "ی")
    text = text.replace("ى", "ی")
    text = text.replace("ك", "ک")

    # تبدیل اعداد فارسی و عربی به انگلیسی
    digit_map = str.maketrans(
        "۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩",
        "01234567890123456789"
    )
    text = text.translate(digit_map)

    # حذف نیم‌فاصله
    text = text.replace("\u200c", "")

    # حروف انگلیسی بدون حساسیت به بزرگ/کوچک
    text = text.casefold()

    # حذف فاصله‌ها و علائم غیرضروری
    text = re.sub(
        r"[\s\-_.,،؛;:!?؟]+",
        "",
        text
    )

    return text