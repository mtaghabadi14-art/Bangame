import random

sentences = [
    "گربه روی دیوار نشست.",
    "امروز هوا خیلی خوب است.",
    "برنامه نویسی با پایتون لذت بخش است.",
    "Bangame بهترین ربات بازی است.",
    "من عاشق ماینکرفت هستم.",
    "هوش مصنوعی آینده را تغییر می‌دهد.",
    "تمرین باعث پیشرفت می‌شود.",
    "کتاب بهترین دوست انسان است.",
    "هرگز تسلیم نشو.",
    "موفقیت نتیجه تلاش است."
]


def create_game():

    sentence = random.choice(sentences)

    return {
        "sentence": sentence
    }


def check(game, text):

    return text.strip() == game["sentence"]