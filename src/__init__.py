import sqlite3

from database.tools import setup_database

DATABASE_PATH = "src/database/database.db"

try:
    with sqlite3.connect(DATABASE_PATH) as conn:
        setup_database(conn)

        #NOTE: Do we enable foreign key constraints?
        #conn.execute("PRAGMA foreign_keys = ON")

        #NOTE: !!!!!! use conn.commit() each time we modify the database !!!!!!

        #TODO: handle erros


except sqlite3.OperationalError as e:
    print("Database error:", e)