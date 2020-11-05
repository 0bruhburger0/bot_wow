import sqlite3


conn = sqlite3.connect("data_base6.db", check_same_thread=False)
cursor = conn.cursor()


cursor.execute("""CREATE TABLE IF NOT EXISTS orders(
                order_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                user_id INTEGER,
                user_name TEXT,
                keyy TEXT,
                key_name TEXT,
                value_particiant TEXT,
                fraction TEXT,
                role TEXT,
                type_of_armor TEXT,
                need_key TEXT,
                step INTEGER DEFAULT 0, 
                cnt_role INTEGER DEFAULT 0
                )""")


# Создание юзера
def cerate_user(user_id: int, user_name: str):
    cursor.execute("INSERT INTO orders (user_id, user_name) VALUES (?, ?)", (user_id, user_name))
    conn.commit()


# Обновляет запись в oredrs
def update(column: str, value, user_id: int):
    cursor.execute(
        f"UPDATE orders SET {column}=? WHERE user_id={user_id} AND step<9", 
        (value,))
    conn.commit()


# Достает step
def get_step(user_id: int):
    cursor.execute(f"SELECT step FROM orders WHERE user_id={user_id} AND step<9")
    rows = cursor.fetchall()
    return(rows)


# Пометка незаконченных заказов
def not_conf(user_id: int):
    cursor.execute(f"SELECT step FROM orders WHERE user_id={user_id}")
    rows = cursor.fetchall()
    if rows[0][0] != 8:
        cursor.execute(f"UPDATE orders SET step=? WHERE user_id={user_id} and step!=0", (11,))
        conn.commit()


# Достает заказ
def get_order(user_id: int):
    cursor.execute(
        f"SELECT * FROM orders WHERE user_id={user_id} AND step<9")
    rows = cursor.fetchall()
    columns = ['order_id', 'user_id', 'user_name', 'keyy', 'key_name', 'value_particiant', 'fraction', 'role', 'type_of_armor', 'need_key', 'step', 'cnt_role']
    dict_row = {}
    for row in rows:
        for index, column in enumerate(columns):
            dict_row[column] = row[index]
    return dict_row


def get_other(user_id: int, column):
    cursor.execute(f"SELECT {column} FROM orders WHERE user_id={user_id} AND step<9")
    rows = cursor.fetchall()
    return rows


def get_cnt_role(user_id):
    cursor.execute(f"SELECT cnt_role FROM orders WHERE user_id={user_id} AND step<9")
    rows = cursor.fetchall()
    return rows


def active_orders(user_id):
    cursor.execute(
        f"SELECT * FROM orders WHERE user_id={user_id} AND step==9")
    rows = cursor.fetchall()
    columns = ['order_id', 'user_id', 'user_name', 'keyy', 'key_name', 'value_particiant', 'fraction', 'role', 'type_of_armor', 'need_key', 'step', 'cnt_role']
    dict_row = {}
    for row in rows:
        for index, column in enumerate(columns):
            dict_row[column] = row[index]
    return dict_row


def all_valid_orders(user_id):
    cursor.execute(
        f"SELECT * FROM orders WHERE user_id={user_id} AND step>8 AND step<11")
    rows = cursor.fetchall()
    return rows

# cursor.execute(f"SELECT * FROM orders")
# rows = cursor.fetchall()
# print(rows)