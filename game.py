import random


def rock_paper_scissors(player):
    print("\n🎮 بازی سنگ، کاغذ، قیچی شروع شد!")

    choices = ["سنگ", "کاغذ", "قیچی"]

    player_score = 0
    bot_score = 0

    rounds = int(input("چند راند بازی کنیم؟ "))

    for round_number in range(1, rounds + 1):

        print(f"\n🎯 راند {round_number} از {rounds}")

        while True:
            player_choice = input("سنگ، کاغذ یا قیچی؟ ").strip()

            if player_choice in choices:
                break

            print("❌ فقط سنگ، کاغذ یا قیچی بنویس.")

        bot_choice = random.choice(choices)

        print(f"🤖 ربات انتخاب کرد: {bot_choice}")
        print(f"👤 تو انتخاب کردی: {player_choice}")

        if player_choice == bot_choice:
            print("🤝 مساوی!")

        elif (
            (player_choice == "سنگ" and bot_choice == "قیچی") or
            (player_choice == "کاغذ" and bot_choice == "سنگ") or
            (player_choice == "قیچی" and bot_choice == "کاغذ")
        ):
            print("🎉 این راند را بردی!")
            player_score += 1

        else:
            print("😢 این راند را ربات برد!")
            bot_score += 1

    print("\n🏁 بازی تمام شد!")

    if player_score > bot_score:
        print("🏆 تو برنده شدی!")
        player.add_win()

    elif bot_score > player_score:
        print("🤖 ربات برنده شد!")
        player.add_loss()

    else:
        print("🤝 مساوی شد!")



def guess_number(player):
    print("\n🎯 بازی حدس عدد شروع شد!")

    number = random.randint(1, 100)
    attempts = 0

    while True:
        try:
            guess = int(input("یک عدد بین 1 تا 100 حدس بزن: "))
            attempts += 1

            if guess < number:
                print("⬆️ عدد من بزرگ‌تره!")

            elif guess > number:
                print("⬇️ عدد من کوچک‌تره!")

            else:
                print(f"🎉 درست حدس زدی! تعداد تلاش‌ها: {attempts}")
                player.add_win()
                break

        except:
            print("❌ فقط عدد وارد کن.")



def dice_game(player):
    print("\n🎲 بازی تاس شروع شد!")

    player_dice = random.randint(1, 6)
    bot_dice = random.randint(1, 6)

    print(f"👤 تاس تو: {player_dice}")
    print(f"🤖 تاس ربات: {bot_dice}")

    if player_dice > bot_dice:
        print("🎉 تو بردی!")
        player.add_win()

    elif bot_dice > player_dice:
        print("😢 ربات برد!")
        player.add_loss()

    else:
        print("🤝 مساوی شد!")