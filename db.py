import sqlite3


conn = sqlite3.connect("data_base3.db", check_same_thread=False)
cursor = conn.cursor()


cursor.execute("""CREATE TABLE IF NOT EXISTS orders(
                order_id INT PRIMARY KEY,
                user_id INT,
                user_name TEXT,
                keyy TEXT,
                value_particiant TEXT,
                fraction TEXT,
                role TEXT,
                type_of_armor TEXT,
                need_key BOOLEAN,
                step INTEGER
                )""")


# Создание юзера
def cerate_user(user_id: int, user_name: str):
    try:
        cursor.execute(
            f"INSERT INTO orders (user_id, user_name) VALUES ({user_id}, {user_name})")
        conn.commit()
    except:
        print('Такой юзер уже есть')


# Обновляет запись в oredrs
def update(column: str, value, user_id: int):
    cursor.execute(
        f"UPDATE orders SET {column}=? WHERE user_id={user_id}", 
        (value,))
    conn.commit()


# Достает step
def get_step(user_id: int):
        cursor.execute(
        f"SELECT step FROM orders WHERE tg_id={tg_id} AND step<9")
    rows = cursor.fetchall()