def get_title(level):
    if level >= 100:
        return "🏆 اسطوره Bangame"

    elif level >= 50:
        return "💎 افسانه"

    elif level >= 30:
        return "👑 استاد"

    elif level >= 20:
        return "🔥 حرفه‌ای"

    elif level >= 10:
        return "⚔️ مبارز"

    elif level >= 5:
        return "🎮 بازیکن"

    else:
        return "🥉 تازه‌کار"