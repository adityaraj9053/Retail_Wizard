import sqlite3
import bcrypt


def get_db_connection():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    return conn, cursor


conn, cursor = get_db_connection()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fullname TEXT NOT NULL,
        username TEXT UNIQUE NOT NULL,
        password BLOB NOT NULL  -- Store password as BLOB for bcrypt compatibility
    )
""")
conn.commit()
conn.close()


def store_user(fullname, username, password):
    """Hashes password and stores user credentials in the database."""
    conn, cursor = get_db_connection()
    try:
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        cursor.execute("INSERT INTO users (fullname, username, password) VALUES (?, ?, ?)",
                       (fullname, username, hashed_password))
        conn.commit()
        return "User registered successfully!", "green"
    except sqlite3.IntegrityError:
        return "Username already exists!", "red"
    finally:
        conn.close()


def verify_user(username, password):
    """Verifies a user's credentials by checking the stored hashed password."""
    conn, cursor = get_db_connection()
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()

    if user:
        stored_password = user[0]  
        if bcrypt.checkpw(password.encode('utf-8'), stored_password):
            return True
    return False


def update_password(username, new_password):
    """Updates the user's password after hashing it."""
    conn, cursor = get_db_connection()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    if cursor.fetchone() is None:
        conn.close()
        return False  

    hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
    cursor.execute("UPDATE users SET password = ? WHERE username = ?", (hashed_password, username))
    conn.commit()
    conn.close()
    return True
