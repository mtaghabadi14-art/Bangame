from datetime import datetime, timedelta


class Player:

    def __init__(
        self,
        user_id,
        name,
        coins=100,
        xp=0,
        level=1,
        wins=0,
        losses=0,
        last_reward=None
    ):
        self.user_id = user_id
        self.name = name
        self.coins = coins
        self.xp = xp
        self.level = level
        self.wins = wins
        self.losses = losses
        self.last_reward = last_reward

    def add_coins(self, amount):
        self.coins += amount

    def remove_coins(self, amount):
        self.coins = max(0, self.coins - amount)

    def add_xp(self, amount):
        self.xp += amount

        while self.xp >= self.level * 100:
            self.xp -= self.level * 100
            self.level += 1

    def win(self):
        self.wins += 1
        self.add_coins(20)
        self.add_xp(10)

    def lose(self):
        self.losses += 1
        self.add_xp(3)

    # برای سازگاری با game.py
    def add_win(self):
        self.win()

    def add_loss(self):
        self.lose()

    def daily_reward(self):

        now = datetime.now()

        if self.last_reward:
            try:
                last = datetime.fromisoformat(self.last_reward)

                if now - last < timedelta(days=1):
                    return False

            except Exception:
                pass

        self.coins += 50
        self.last_reward = now.isoformat()

        return True

    def profile_text(self):

        return (
            f"👤 نام: {self.name}\n"
            f"💰 سکه: {self.coins}\n"
            f"⭐ XP: {self.xp}\n"
            f"🏆 Level: {self.level}\n"
            f"✅ برد: {self.wins}\n"
            f"❌ باخت: {self.losses}"
        )

    def show_profile(self):
        print(self.profile_text())