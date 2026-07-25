from rubika import send_message

from database import get_typing_leaderboard


def typing(chat_id):

    players = get_typing_leaderboard()

    if not players:

        send_message(
            chat_id,
            "هنوز کسی سرعت تایپ بازی نکرده است."
        )

        return

    text = "🏆 لیدربورد سرعت تایپ\n\n"

    medals = [
        "🥇",
        "🥈",
        "🥉"
    ]

    for i, player in enumerate(players):

        uid, wpm, best_time = player

        if i < 3:
            icon = medals[i]
        else:
            icon = f"{i+1}."

        text += (
            f"{icon} "
            f"{uid[:8]}..."
            f"\n"
            f"⚡ {round(wpm)} WPM"
            f" | "
            f"⏱ {best_time:.2f}s\n\n"
        )

    send_message(
        chat_id,
        text
    )