import sqlite3


conn = sqlite3.connect('users.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT,
        balance INTEGER DEFAULT 1000
    )
''')
conn.commit()

def set_user_balance(user_id, new_balance=1000):
    cursor.execute('UPDATE users SET balance = ? WHERE id = ?', (new_balance, user_id))
    conn.commit()

def user_exists(user_id):
    cursor.execute('SELECT 1 FROM users WHERE id = ?', (user_id,))
    return cursor.fetchone() is not None

def get_balance(user_id):
    cursor.execute('SELECT balance FROM users WHERE id = ?', (user_id,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        return None

def add_balance(user_id, amount):
    cursor.execute('SELECT balance FROM users WHERE id = ?', (user_id,))
    result = cursor.fetchone()
    if result:
        current_balance = result[0]
        new_balance = current_balance + amount
        cursor.execute('UPDATE users SET balance = ? WHERE id = ?', (new_balance, user_id))
        conn.commit()

def get_players_sorted_by_balance():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute('SELECT id, username, balance FROM users ORDER BY balance ASC')
    players = cursor.fetchall()  # получение всех результатов

    # закрытие соединения
    conn.close()

    return players