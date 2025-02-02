import sqlite3

def setup_database(conn):
    try:
        cur = conn.cursor()

        cur.execute('''
        CREATE TABLE IF NOT EXISTS user_table (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT
        )
        ''')

        cur.execute('''
        CREATE TABLE IF NOT EXISTS log_table (
            log_id INTEGER PRIMARY KEY,
            user_id INTEGER
        )
        ''')

        cur.execute('''
        CREATE TABLE IF NOT EXISTS message_table (
            message_id INTEGER PRIMARY KEY,
            log_id INTEGER,
            time TEXT NOT NULL,
            content TEXT NOT NULL
        )
        ''')

        conn.commit()

    except sqlite3.OperationalError as e:
        print(f"OperationalError during setup: {e}")
        conn.rollback()
        raise

    except sqlite3.DatabaseError as e:
        print(f"DatabaseError during setup: {e}")
        conn.rollback()
        raise


#NOTE: We assume that we always know that the log_id has been given to the log_table 
#      before adding a message

#NOTE: Don't forget to commit (connector.commit()) any modification to the database

def add_user(username, password, cursor):
    """
    Add a new user to the `user_table`.

    Args:
    - username (str)
    - password (str)
    - cursor (sqlite3.Cursor)

    Returns:
    - user_id (int)
    """
    try:
        cursor.execute("INSERT INTO user_table (username, password) VALUES (?, ?)", (username, password))
        user_id = cursor.lastrowid
        return user_id

    except sqlite3.IntegrityError as e:
        print(f"IntegrityError when adding user {username}: {e}")
        raise

    except sqlite3.DatabaseError as e:
        print(f"DatabaseError when adding user {username}: {e}")
        raise


def does_username_already_exist(username, cursor):
    """
    Check if a username already exists in the user_table.

    Args:
    - username (str)
    - cursor (sqlite3.Cursor)

    Returns:
    - bool
    """
    try:
        cursor.execute("SELECT 1 FROM user_table WHERE username = ? LIMIT 1", (username,))
        count = cursor.fetchone()[0]
        return count > 0
    
    except sqlite3.DatabaseError as e:
        print(f"DatabaseError when checking username existence: {e}")
        raise


def add_log(log_id, user_id, cursor):
    """
    Add a new log entry to the `log_table`.

    Args:
    - log_id (int)
    - user_id (int)
    - cursor (sqlite3.Cursor)
    """
    try:
        cursor.execute("INSERT INTO log_table VALUES (?, ?)", (log_id, user_id))

    except sqlite3.IntegrityError as e:
        print(f"IntegrityError when adding log {log_id} for user {user_id}: {e}")
        raise

    except sqlite3.DatabaseError as e:
        print(f"DatabaseError when adding log {log_id} for user {user_id}: {e}")
        raise


def add_message(message_id, log_id, time, content, cursor):
    """
    Add a new message entry to the `message_table`.

    Args:
    - message_id (int)
    - log_id (int)
    - time (str): The timestamp of when the message was created.
    - content (str): The content of the message.
    - cursor (sqlite3.Cursor)
    """
    try:
        cursor.execute("INSERT INTO message_table (message_id, log_id, time, content) VALUES (?, ?, ?, ?)",
                    (message_id, log_id, time, content))
        
    except sqlite3.IntegrityError as e:
        print(f"IntegrityError when adding message {message_id} for log {log_id}: {e}")
        raise

    except sqlite3.DatabaseError as e:
        print(f"DatabaseError when adding message {message_id} for log {log_id}: {e}")
        raise


def get_user_infos_from_username(username, cursor):
    """
    Retrieve user information based on the username.

    Args:
    - username (str).
    - cursor (sqlite3.Cursor)

    Returns:
    - tuple: A tuple containing (user_id, password) if the user exists, or None if the user does not exist.
    """
    try:
        cursor.execute("SELECT user_id, password FROM user_table WHERE username = ?", (username,))
        user_info = cursor.fetchone()
        return user_info
    
    except sqlite3.DatabaseError as e:
        print(f"DatabaseError when retrieving user info for {username}: {e}")
        raise


def get_user_id_from_log(log_id, cursor):
    """
    Retrieve the user_id associated with a specific log entry.

    Args:
    - log_id (int)
    - cursor (sqlite3.Cursor)

    Returns:
    - int: The user_id associated with the log_id, or None if not found.
    """
    try:
        result = cursor.execute("SELECT user_id FROM log_table WHERE log_id = ?", (log_id,))
        user_id = result.fetchone()

        if user_id:
            return user_id[0]
        
    except sqlite3.DatabaseError as e:
        print(f"DatabaseError when retrieving user ID from log {log_id}: {e}")
        raise
    

def get_specific_message(message_id, cursor):
    """
    Retrieve details of a message (its log_id, time, and content).

    Args:
    - message_id (int)
    - cursor (sqlite3.Cursor)

    Returns:
    - tuple: (log_id, time, content of the message), or None if not found.
    """
    try:
        result = cursor.execute("SELECT log_id, time, content FROM message_table WHERE message_id = ?", (message_id,))
        row = result.fetchone()
        return row
    
    except sqlite3.DatabaseError as e:
        print(f"DatabaseError when retrieving message {message_id}: {e}")
        raise


def get_messages_per_log(log_id, cursor):
    """
    Retrieve all messages for a specific log_id.

    Args:
    - log_id (int)
    - cursor (sqlite3.Cursor)

    Returns:
    - list: A list of tuples (message_id, time, content), or an empty list if no messages are found.
    """
    try:
        result = cursor.execute("SELECT message_id, time, content FROM message_table WHERE log_id = ?", (log_id,))
        rows = result.fetchall()
        
        if rows:
            return rows
        return []
    
    except sqlite3.DatabaseError as e:
        print(f"DatabaseError when retrieving messages for log {log_id}: {e}")
        raise


def get_all_messages_per_user(user_id, cursor):
    """
    Retrieve all messages for a specific user from all logs.

    Args:
    - user_id (int)
    - cursor (sqlite3.Cursor)

    Returns:
    - list: A list of tuples (message_id, log_id, time, content) for each message the user is associated with,
            or an empty list if no messages are found.
    """
    try:
        result = cursor.execute('''
            SELECT m.message_id, m.log_id, m.time, m.content
            FROM message_table m
            JOIN log_table l ON l.log_id = m.log_id
            WHERE l.user_id = ?
        ''', (user_id,))
        
        rows = result.fetchall()
        
        if rows:
            return rows
        return []
    
    except sqlite3.DatabaseError as e:
        print(f"DatabaseError when retrieving all messages for user {user_id}: {e}")
        raise

