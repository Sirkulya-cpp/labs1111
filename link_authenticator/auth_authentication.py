import sqlite3

def check_user_exists(user_login):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT EXISTS(SELECT 1 FROM users WHERE login = ?)", (user_login,))
    result = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return result

def try_user_login(user_login, user_password):
    if check_user_exists(user_login):
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE login = ?", (user_login,))
        right_password = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return user_password == right_password
    return False

def try_user_signup(user_login, user_password):
    if not check_user_exists(user_login):
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (login, password) VALUES (?, ?)", (user_login, user_password))
        cursor.close()
        conn.commit()
        conn.close()
        return True
    return False
