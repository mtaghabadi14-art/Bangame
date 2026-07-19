from game import rock_paper_scissors, guess_number, dice_game
from player import Player
from database_sql import add_player, get_player


name = input("🎮 اسم بازیکنت رو وارد کن: ")

data = get_player(name)

if data:
    print(f"\n👋 خوش آمدی دوباره {name}!")

    player = Player(
        data[0],  # name
        data[1],  # coins
        data[2],  # xp
        data[4],  # wins
        data[5],  # losses
        data[3],  # level
        data[6]   # last_reward
    )

else:
    print(f"\n🎉 بازیکن جدید ساخته شد: {name}")

    player = Player(name)

    add_player(player)


# جایزه روزانه
player.daily_reward()

# ذخیره اطلاعات
add_player(player)


while True:
    print("\n========================")
    print("🎮 Bangame")
    print("========================")
    print(f"👤 {player.name}")
    print(f"💰 سکه: {player.coins}")
    print(f"⭐ XP: {player.xp}")
    print(f"📈 Level: {player.level}")
    print("========================")

    print("1️⃣ سنگ، کاغذ، قیچی")
    print("2️⃣ حدس عدد")
    print("3️⃣ تاس")
    print("4️⃣ پروفایل")
    print("5️⃣ خروج")

    choice = input("\nانتخاب کن: ")

    if choice == "1":
        rock_paper_scissors(player)
        add_player(player)

    elif choice == "2":
        guess_number(player)
        add_player(player)

    elif choice == "3":
        dice_game(player)
        add_player(player)

    elif choice == "4":
        player.show_profile()

    elif choice == "5":
        add_player(player)
        print("\n👋 خداحافظ!")
        break

    else:
        print("\n❌ انتخاب نامعتبر است.")