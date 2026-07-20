from rubika import get_updates, send_message
from database.database_sql import get_player, add_player
from models.player import Player
import time

offset_id = None
processed_messages = set()

print("🤖 Bangame Bot Started 🚀")

# خالی کردن پیام‌های قدیمی هنگام روشن شدن ربات
result = get_updates(limit=1)

if result.get("status") == "OK":
    data = result.get("data", {})
    offset_id = data.get("next_offset_id")

while True:

    try:

        result = get_updates(
            offset_id=offset_id,
            limit=10
        )

        if result.get("status") != "OK":
            print(result)
            time.sleep(5)
            continue

        data = result.get("data", {})
        updates = data.get("updates", [])

        # از این به بعد فقط پیام‌های جدید خوانده می‌شوند
        if data.get("next_offset_id"):
            offset_id = data["next_offset_id"]

        for update in updates:

            if update.get("type") != "NewMessage":
                continue

            message = update.get("new_message", {})

            message_id = message.get("message_id")

            if message_id in processed_messages:
                continue

            processed_messages.add(message_id)

            chat_id = update.get("chat_id")
            user_id = message.get("sender_id")
            text = message.get("text", "").strip()

            if not user_id:
                continue

            player_data = get_player(user_id)

            if player_data:

                player = Player(
                    player_data[0],
                    player_data[1],
                    player_data[2],
                    player_data[3],
                    player_data[4],
                    player_data[5],
                    player_data[6],
                    player_data[7]
                )

            else:

                player = Player(
                    user_id=user_id,
                    name=f"Player_{user_id[-6:]}"
                )

                add_player(player)

            print(f"📩 {player.name}: {text}")

            # ---------------- START ----------------

            if text == "/start":

                player.daily_reward()
                add_player(player)

                send_message(
                    chat_id,
                    f"""🎮 Bangame

سلام {player.name} 👋

💰 سکه: {player.coins}
⭐ XP: {player.xp}
🏆 Level: {player.level}

دستورات:

/profile
/daily
/help
"""
                )

            # ---------------- PROFILE ----------------

            elif text == "/profile":

                send_message(
                    chat_id,
                    player.profile_text()
                )

            # ---------------- DAILY ----------------

            elif text == "/daily":

                if player.daily_reward():

                    add_player(player)

                    send_message(
                        chat_id,
                        "🎁 50 سکه جایزه روزانه دریافت کردی!"
                    )

                else:

                    send_message(
                        chat_id,
                        "⏳ جایزه امروز را قبلاً گرفته‌ای."
                    )

            # ---------------- HELP ----------------

            elif text == "/help":

                send_message(
                    chat_id,
                    """📚 دستورات موجود:

/start
/profile
/daily
/help
"""
                )

            # ---------------- UNKNOWN ----------------

            else:

                send_message(
                    chat_id,
                    "❓ دستور ناشناخته است.\nاز /help استفاده کن."
                )

        time.sleep(2)

    except KeyboardInterrupt:

        print("🛑 Bot stopped")
        break

    except Exception as e:

        print("❌ Error:", e)
        time.sleep(5)