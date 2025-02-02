import sqlite3

from database.tools import add_log, add_message, add_user, get_messages_per_log, get_user_id_from_log, get_user_infos_from_username, setup_database

DATABASE_PATH = "src/database/database.db"

try:
    with sqlite3.connect(DATABASE_PATH) as conn:
        setup_database(conn)

        #NOTE: Do we enable foreign key constraints?
        #conn.execute("PRAGMA foreign_keys = ON")

        #NOTE: use conn.commit() each time we modify the database


except sqlite3.OperationalError as e:
    print("Database error:", e)