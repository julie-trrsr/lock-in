import sqlite3

from database.tools import add_log, add_message, add_user, get_messages_per_log, get_user_id_from_log, get_user_infos_from_user_id, get_user_infos_from_username, setup_database

DATABASE_PATH = "src/database/database.db"

try:
    with sqlite3.connect(DATABASE_PATH) as conn:
        setup_database(conn)

        #NOTE: Do we enable foreign key constraints?
        #conn.execute("PRAGMA foreign_keys = ON")

        #NOTE: !!!!!! use conn.commit() each time we modify the database !!!!!!

        #TODO: handle erros
        cur = conn.cursor()
        user1 = add_user("aaa", "bbb", cur)
        user2 = add_user("ccc", "ddd", cur)

        log1 = add_log(user1, cur)
        log2 = add_log(user1, cur)
        log3 = add_log(user2, cur)

        mess1 = add_message(log1, "aaaA", "bbbA", cur)
        mess2 = add_message(log1, "cccA", "dddA", cur)
        mess3 = add_message(log3, "eeeA", "fffA", cur)

        conn.commit()

        print(get_user_infos_from_username("aaa", cur))
        print(get_user_infos_from_username("ccc", cur))
        print(get_user_infos_from_user_id(user2, cur))
        print(get_user_id_from_log(log2, cur))
        print(get_messages_per_log(log1, cur))


except sqlite3.OperationalError as e:
    print("Database error:", e)