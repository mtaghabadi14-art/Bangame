import random

from .questions import QUESTIONS


class PuzzleGame:

    # ==========================================
    # تنظیمات بازی
    # ==========================================

    TOTAL_ROUNDS = 10

    # ==========================================
    # ساخت بازی
    # ==========================================

    def __init__(self, players):

        self.players = players.copy()

        self.started = False
        self.finished = False

        self.current_round = 0

        # سؤال‌های این بازی
        self.questions = []

        # سؤال فعلی
        self.current_question = None

        # بازیکنانی که در دور فعلی جواب داده‌اند
        self.answers = set()

        # امتیاز
        self.scores = {
            player: 0
            for player in self.players
        }

        # تعداد جواب صحیح
        self.correct_answers = {
            player: 0
            for player in self.players
        }

        # تعداد جواب داده‌شده
        self.total_answers = {
            player: 0
            for player in self.players
        }

        # پاسخ‌های دور فعلی
        self.round_answers = {}


    # ==========================================
    # شروع بازی
    # ==========================================

    def start(self):

        if self.started:
            return False

        if len(self.players) < 2:
            return False

        # برای هر بازی یک ترتیب تصادفی جدید
        self.questions = QUESTIONS.copy()

        random.shuffle(
            self.questions
        )

        # اگر تعداد سؤال‌ها کمتر از تعداد دورها بود
        if len(self.questions) < self.TOTAL_ROUNDS:
            return False

        self.started = True
        self.finished = False

        self.current_round = 0

        self.answers.clear()
        self.round_answers.clear()

        self.current_question = None

        return self.next_question()


    # ==========================================
    # سؤال بعدی
    # ==========================================

    def next_question(self):

        if self.finished:
            return False

        if self.current_round >= self.TOTAL_ROUNDS:

            self.finish()

            return False

        # پاک کردن جواب‌های دور قبلی
        self.answers.clear()
        self.round_answers.clear()

        # انتخاب سؤال جدید
        self.current_question = (
            self.questions[
                self.current_round
            ]
        )

        self.current_round += 1

        return True


    # ==========================================
    # سؤال فعلی
    # ==========================================

    def get_question(self):

        return self.current_question


    # ==========================================
    # شماره دور
    # ==========================================

    def round_number(self):

        return self.current_round


    # ==========================================
    # ثبت جواب
    # ==========================================

    def answer(
        self,
        player,
        answer
    ):

        # بازی تمام شده
        if self.finished:

            return {
                "success": False,
                "message": "🏁 بازی تمام شده است."
            }

        # بازیکن داخل بازی نیست
        if player not in self.players:

            return {
                "success": False,
                "message": "❌ تو داخل این بازی نیستی."
            }

        # قبلاً جواب داده
        if player in self.answers:

            return {
                "success": False,
                "message": "⚠️ جواب این دور را قبلاً فرستادی."
            }

        if self.current_question is None:

            return {
                "success": False,
                "message": "❌ سؤال فعالی وجود ندارد."
            }

        # ذخیره جواب
        self.answers.add(
            player
        )

        self.total_answers[player] += 1

        self.round_answers[player] = answer

        correct_answer = (
            self.current_question["answer"]
        )

        # مقایسه پاسخ
        is_correct = self.normalize(
            answer
        ) == self.normalize(
            correct_answer
        )

        # --------------------------------------
        # جواب صحیح
        # --------------------------------------

        if is_correct:

            self.correct_answers[player] += 1

            self.scores[player] += 1

            return {
                "success": True,
                "correct": True,
                "points": 1,
                "message": "✅ جواب درست بود! +1 امتیاز"
            }

        # --------------------------------------
        # جواب غلط
        # --------------------------------------

        return {
            "success": True,
            "correct": False,
            "points": 0,
            "message": "❌ جواب اشتباه بود."
        }


    # ==========================================
    # نرمال‌سازی جواب
    # ==========================================

    @staticmethod
    def normalize(text):

        if text is None:
            return ""

        text = str(text).strip().lower()

        # --------------------------------------
        # یکسان‌سازی حروف فارسی و عربی
        # --------------------------------------

        text = text.replace("ي", "ی")
        text = text.replace("ى", "ی")

        text = text.replace("ك", "ک")

        # --------------------------------------
        # تبدیل اعداد فارسی به انگلیسی
        # --------------------------------------

        persian_digits = "۰۱۲۳۴۵۶۷۸۹"
        english_digits = "0123456789"

        for persian, english in zip(
            persian_digits,
            english_digits
        ):
            text = text.replace(
                persian,
                english
            )

        # --------------------------------------
        # تبدیل اعداد عربی به انگلیسی
        # --------------------------------------

        arabic_digits = "٠١٢٣٤٥٦٧٨٩"

        for arabic, english in zip(
            arabic_digits,
            english_digits
        ):
            text = text.replace(
                arabic,
                english
            )

        # --------------------------------------
        # حذف تمام فاصله‌ها
        # --------------------------------------

        text = "".join(
            text.split()
        )

        return text


    # ==========================================
    # آیا همه جواب داده‌اند؟
    # ==========================================

    def everyone_answered(self):

        return len(
            self.answers
        ) >= len(
            self.players
        )


    # ==========================================
    # آیا بازیکن جواب داده؟
    # ==========================================

    def has_answered(
        self,
        player
    ):

        return player in self.answers


    # ==========================================
    # پایان دور و رفتن به سؤال بعدی
    # ==========================================

    def finish_round(self):

        if self.finished:
            return False

        if self.current_round >= self.TOTAL_ROUNDS:

            self.finish()

            return False

        return self.next_question()


    # ==========================================
    # پایان بازی
    # ==========================================

    def finish(self):

        self.finished = True
        self.started = False

        self.current_question = None


    # ==========================================
    # برنده
    # ==========================================

    def winner(self):

        if not self.scores:
            return None

        return max(
            self.scores,
            key=self.scores.get
        )


    # ==========================================
    # رتبه‌بندی
    # ==========================================

    def leaderboard(self):

        return sorted(
            self.scores.items(),
            key=lambda item: item[1],
            reverse=True
        )


    # ==========================================
    # امتیاز بازیکن
    # ==========================================

    def get_score(
        self,
        player
    ):

        return self.scores.get(
            player,
            0
        )


    # ==========================================
    # وضعیت بازی
    # ==========================================

    def status(self):

        return {
            "started": self.started,
            "finished": self.finished,
            "round": self.current_round,
            "total_rounds": self.TOTAL_ROUNDS,
            "players": self.players.copy(),
            "scores": self.scores.copy(),
            "answered": list(
                self.answers
            ),
            "current_question": self.current_question
        }