from data import add_or_update_user_xp_and_lvl, fetch_user_xp_and_lvl
import logging

logger = logging.getLogger('wobble.bot')

def reset_profile(username: str):
    try:
        add_or_update_user_xp_and_lvl(username, 0, 1)
        return f"Wobble was surprised to know you want to reset your profile `w(ﾟДﾟ)w`, but he did reset them!"
    except Exception as e:
        logger.error(f"An error occurred while resetting user '{username}': {e}")
        return f"Wobble had some problems resetting your profile `(￣﹏￣；)`"


def check_level(username:str, xp: int):
    try:
        user_data = fetch_user_xp_and_lvl(username)

        if user_data is None:
            add_or_update_user_xp_and_lvl(username, xp, 1)
            logger.info(f"New User '{username}' added with {xp} XP and level 1.")
            return f"Welcome `{username}`! You are **reborn** in this new World (〃￣︶￣)/`\(￣︶￣〃)`"

        updated_level = calculate_lvl(user_data[1], user_data[0] + xp)

        add_or_update_user_xp_and_lvl(username, user_data[0] + xp, updated_level)

        if updated_level > user_data[1]:
            logger.info(f"User '{username}' leveled up to {updated_level}.")
            return f"**CONGRATS🎉**, Wobble is happy to announce that you **LEVELD UP** to `Level {updated_level}`! `o(*^＠^*)o!`"
    except Exception as e:
        print(e)


def calculate_lvl(level: int, xp: int) -> int:
    """Calculate the level based on experience points.

    This method calculates the XP required for the next level based
    on the current level and returns the new level if the user has
    enough XP to level up.

    :param level: The current level of the user.
    :param xp: The current experience points of the user.
    :return: The new level after considering the current XP.
    """
    base_xp = 100
    growth_factor = 1.5

    xp_for_next_level = int(base_xp * (level ** growth_factor))

    if xp >= xp_for_next_level:
        return level + 1
    return level