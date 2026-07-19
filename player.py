import datetime


class Player:
    def __init__(self, name, coins=100, xp=0, wins=0, losses=0, level=1, last_reward=""):
        self.name = name
        self.coins = coins
        self.xp = xp
        self.wins = wins
        self.losses = losses
        self.level = level
        self.last_reward = last_reward

    def show_profile(self):
        print("\n👤 پروفایل بازیکن")
        print("----------------")
        print(f"نام: {self.name}")
        print(f"💰 سکه: {self.coins}")
        print(f"⭐ XP: {self.xp}")
        print(f"📈 Level: {self.level}")
        print(f"🏆 برد: {self.wins}")
        print(f"😢 باخت: {self.losses}")

    def add_win(self):
        self.wins += 1
        self.xp += 10
        self.coins += 20

        if self.xp >= self.level * 50:
            self.level += 1
            print(f"🎉 Level Up! رسیدی به Level {self.level}")

    def add_loss(self):
        self.losses += 1
        self.xp += 2

    def daily_reward(self):
        today = str(datetime.date.today())

        if self.last_reward != today:
            self.coins += 50
            self.xp += 5
            self.last_reward = today

            print("\n🎁 جایزه روزانه گرفتی!")
            print("💰 +50 سکه")
            print("⭐ +5 XP")

        else:
            print("\n⏳ جایزه روزانه امروز رو گرفتی.")