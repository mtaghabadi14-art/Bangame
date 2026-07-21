from database import get_user, add_xp, set_xp, set_level, add_coins

# XP مورد نیاز برای هر لول
LEVELS = {
    1: 10,
    2: 100,
    3: 250,
    4: 500,
    5: 800,
    6: 1200
}

# جایزه هر لول
REWARDS = {
    2: 50,
    3: 150,
    4: 300,
    5: 500,
    6: 800,
    7: 1200
}


def give_xp(user_id, amount):

    add_xp(user_id, amount)

    user = get_user(user_id)

    coins = user[1]
    level = user[2]
    xp = user[3]

    while level in LEVELS and xp >= LEVELS[level]:

        xp -= LEVELS[level]
        level += 1

        set_level(user_id, level)
        set_xp(user_id, xp)

        reward = REWARDS.get(level, level * 300)

        add_coins(user_id, reward)

        return {
            "level_up": True,
            "level": level,
            "reward": reward
        }

    return {
        "level_up": False,
        "level": level,
        "reward": 0
    }