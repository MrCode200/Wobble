import sqlite3
import logging
from functools import lru_cache
from pathlib import Path
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('wobble.bot')

# Get the absolute path of the current file
current_path = os.path.abspath(__file__)
# Get the directory of the current file
current_dir = os.path.dirname(current_path)


@lru_cache(maxsize=None)
def read_sql_query(sql_path: str) -> str:
    """Read the SQL query from a specified file.

    This function reads the content of a SQL file and returns it as a string.

    :param sql_path: The path to the SQL file to be read.
    :return: The content of the SQL file as a string.
    """
    return Path(current_dir + sql_path).read_text()


# Establishing a connection to the SQLite database
conn = sqlite3.connect(current_dir + '/user_level.db')
cursor = conn.cursor()

# Execute the setup SQL script
try:
    cursor.execute(read_sql_query("/sql/setup.sql"))
    conn.commit()
    logger.info("Database setup script executed successfully.")
except sqlite3.Error as e:
    logger.error(f"An error occurred while executing the setup script: {e}")


def add_or_update_user_xp_and_lvl(username: str, xp: int, lvl: int) -> None:
    """Add or update a user's experience points and level in the database.

    This function inserts a new user or updates the XP and level for an existing user
    in the database.

    :param username: The username of the user whose XP and level are being updated.
    :param xp: The amount of experience points to set for the user.
    :param lvl: The level to set for the user.
    """
    try:
        cursor.execute(read_sql_query("/sql/add_or_update.sql"),
                       {"username": username, "xp": xp, "lvl": lvl})
        conn.commit()
        logger.debug(f"User '{username}' XP updated to {xp} and level to {lvl}.")
    except sqlite3.Error as e:
        logger.error(f"An error occurred while adding or updating user '{username}': {e}")


def fetch_user_xp_and_lvl(username: str) -> tuple[int, int] | None:
    """Fetch the experience points and level of a user from the database.

    This function retrieves the XP and level of the specified user from the database.

    :param username: The username of the user whose data is to be fetched.
    :return: A tuple containing the user's XP and level if found; otherwise, None.
    """
    try:
        cursor.execute(read_sql_query("/sql/read.sql"), {"username": username})
        result = cursor.fetchone()
        if result:
            logger.debug(f"User '{username}' found with {result[0]} XP and {result[1]} Level.")
            return result
        else:
            logger.warning(f"User '{username}' not found.")
            return None
    except sqlite3.Error as e:
        logger.error(f"An error occurred while fetching XP for user '{username}': {e}")
        return None


def close() -> None:
    """Close the connection to the SQLite database.

    This function closes the connection to the database to free up resources.
    """
    conn.close()
    logger.info("Database connection closed.")
