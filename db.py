import sqlite3


conn = sqlite3.connect("data_base6.db", check_same_thread=False)
cursor = conn.cursor()


cursor.execute("""CREATE TABLE IF NOT EXISTS customers(
                id INTEGER PRIMARY KEY,
                customer_name TEXT,
                wallet_name TEXT DEFAULT 'Не указано',
                wallet_token TEXT DEFAULT 'Не указано',
                credit INTEGER DEFAULT 0
                )""")


cursor.execute("""CREATE TABLE IF NOT EXISTS executors(
                id INTEGER PRIMARY KEY,
                executor_name TEXT,
                wallet_name TEXT DEFAULT 'Не указано',
                wallet_address TEXT DEFAULT 'Не указано',
                balance INTEGER DEFAULT 0,
                score INTEGER DEFAULT 0,
                cnt_orders INTEGER DEFAULT 0
                )""")


cursor.execute("""CREATE TABLE IF NOT EXISTS orders(
                id INTEGER PRIMARY KEY NOT NULL,
                customer_id INTEGER,
                lvl_key TEXT,
                cnt_executors INTEGER,
                cnt_fact_executors INTEGER DEFAULT 0,
                fraction TEXT,
                key_name TEXT DEFAULT 'Без ключа',
                roles TEXT,
                cnt_roles INTEGER DEFAULT 0,
                link TEXT DEFAULT 'Ссылка не указана',
                price INTEGER,
                executors_id TEXT,
                step INTEGER DEFAULT 0,
                message_order INTEGER,
                comission INTEGER DEFAULT 0,
                room INTEGER,
                comment TEXT,
                waiting room TEXT
                )""")


### Создание записей ###
def cerate_customer(customer_id: int, customer_name: str): # Создание заказчика в customers
    try:
        cursor.execute(
            "INSERT INTO customers (id, customer_name) VALUES (?, ?)", 
        (customer_id, customer_name))
        conn.commit()
    except:
        print('уже создан')


def create_order(cusromer_id: int, lvl_key: str, cnt_executors: int): # Создание заказа в orders
    cursor.execute(
        "INSERT INTO orders (customer_id, lvl_key, cnt_executors) VALUES (?, ?, ?)", 
    (cusromer_id, lvl_key, cnt_executors))
    conn.commit()


def cerate_executor(executor_id: int, executor_name: str): # Создание исполнителя в executors
    try:
        cursor.execute(
            "INSERT INTO executors (id, executor_name) VALUES (?, ?)", 
        (executor_id, executor_name))
        conn.commit()
    except:
        print('уже создан')


def update(table, column: str, value, primary_id: int): # Обновление для executors и customers
    cursor.execute(
        f"UPDATE {table} SET {column}=? WHERE id={primary_id}", 
        (value,))
    conn.commit()


def ended(table, column: str, value, primary_id: int, user_id: int): # Закрытие заказа
    cursor.execute(
        f"UPDATE {table} SET {column}=? WHERE id={primary_id} AND customer_id={user_id}", 
        (value,))
    conn.commit()


def update9(column: str, value, primary_id: int): # Обновление orders, где step<9
    cursor.execute(
        f"UPDATE orders SET {column}=? WHERE customer_id={primary_id} AND step<9", 
        (value,))
    conn.commit()


def update8(column: str, value, primary_id: int): # Обновление orders, где step>8
    cursor.execute(
        f"UPDATE orders SET {column}=? WHERE id={primary_id} AND step>8", 
        (value,))
    conn.commit()


def get_customer(primary_id: int): # Достатет данные заказчика
    cursor.execute(
        f"SELECT * FROM customers WHERE id={primary_id}")
    rows = cursor.fetchall()
    columns = ['id', 'customer_name', 'wallet_name', 'wallet_token', 'credit']
    dict_row = {}
    for row in rows:
        for index, column in enumerate(columns):
            dict_row[column] = row[index]
    return dict_row


def get_executor(primary_id: int): # Достатет данные исполнителя
    cursor.execute(
        f"SELECT * FROM executors WHERE id={primary_id}")
    rows = cursor.fetchall()
    columns = ['id', 'executor_name', 'wallet_name', 'wallet_address', 'balance', 'score', 'cnt_orders']
    dict_row = {}
    for row in rows:
        for index, column in enumerate(columns):
            dict_row[column] = row[index]
    return dict_row


def get_order(customer_id: int): # Достатет данные заказа по customer_id
    cursor.execute(
        f"SELECT * FROM orders WHERE customer_id={customer_id} AND step<9")
    rows = cursor.fetchall()
    columns = ['id', 'customer_id', 'lvl_key', 'cnt_executors', 'cnt_fact_executors', 'fraction', 'key_name', 'roles', 
    'cnt_roles', 'link', 'price', 'executors_id', 'step', 'message_order', 'comission', 'room', 'comment', 'waiting room']
    dict_row = {}
    for row in rows:
        for index, column in enumerate(columns):
            dict_row[column] = row[index]
    return dict_row


def get_order_id(order_id: int): # Достает заказ по id заказа
    cursor.execute(
        f"SELECT * FROM orders WHERE id={order_id}")
    rows = cursor.fetchall()
    columns = ['id', 'customer_id', 'lvl_key', 'cnt_executors', 'cnt_fact_executors', 'fraction', 'key_name', 'roles', 
    'cnt_roles', 'link', 'price', 'executors_id', 'step', 'message_order', 'comission', 'room', 'comment', 'waiting room']
    dict_row = {}
    for row in rows:
        for index, column in enumerate(columns):
            dict_row[column] = row[index]
    return dict_row


def active_orders_customer(customer_id: int): # Достает активные заказы по customer_id
    cursor.execute(
        f"SELECT * FROM orders WHERE customer_id={customer_id} AND step IN (9, 10)")
    rows = cursor.fetchall()
    if rows != []:
        orders = []
        for row in rows:
            order_id = str(row[0])
            key_name = row[6]
            price = str(row[10])
            if row[12] == 9:
                step = 'в поиске исполнителя'
            elif row[12] == 10:
                step = 'выполняется'
            order = f"№{order_id} - {key_name} | {price}₽ | {step}"
            orders.append(order)
        orders_history = '\n'.join(orders)
        return orders_history
    else:
        orders = 'Нет активных заказов'
        return orders


def active_orders_executor(executors_id: int): # Достает активные заказы по executor_id
    cursor.execute(
        f"SELECT * FROM orders WHERE step in (9, 10)")
    rows = cursor.fetchall()
    orders = []
    if rows != []:
        try:
            for row in rows:
                executors_id_list = eval(row[11])
                if executors_id in executors_id_list:
                    order_id = str(row[0])
                    key_name = row[6]
                    price = str(row[10])
                    if row[12] == 9:
                        step = 'в поиске исполнитей'
                    elif row[12] == 10:
                        step = 'выполняется'
                    order = f"№{order_id} - {key_name} | {price}₽ | {step}"
                    orders.append(order)
                else:
                    pass
            orders_history = '\n'.join(orders)
            return orders_history
        except:
            orders = 'Нет активных заказов'
            return orders
    else:
        orders = 'Нет активных заказов'
        return orders


def not_conf(customer_id: int): # Пометка недооформленных заказов заказов
    cursor.execute(f"SELECT id, step FROM orders WHERE customer_id={customer_id}")
    rows = cursor.fetchall()
    for row in rows:
        if row[1] not in (9, 10, 12, 13):
            cursor.execute(
                f"UPDATE orders SET step=? WHERE customer_id={customer_id} AND id={row[0]}",
                (11,))
            conn.commit()


def history_customer(column, primary_id: int): # Возвращает строку с историей заказов
    cursor.execute(
        f"SELECT * FROM orders WHERE {column}={primary_id} AND step IN (9, 10, 12, 13)")
    rows = cursor.fetchall()
    orders = []
    for row in rows:
        order_id = str(row[0])
        key_name = row[6]
        price = str(row[10])
        if row[12] == 9:
            step = 'в поиске исполнителя'
        elif row[12] == 10:
            step = 'выполняется'
        elif row[12] == 12:
            step = 'закончен, неоплачен'
        elif row[12] == 13:
            step = 'закончен, оплачен'
        order = f"№{order_id} - {key_name} | {price}₽ | {step}"
        orders.append(order)
    orders_history = '\n'.join(orders)
    return orders_history


def history_executor(primary_id: int): # Возвращает строку с историей заказов
    cursor.execute(
        f"SELECT * FROM orders WHERE step IN (9, 10, 12, 13)")
    rows = cursor.fetchall()
    orders = []
    for row in rows:
        print(row)
        executors_id_list = eval(row[11])
        if primary_id in executors_id_list:
            order_id = str(row[0])
            key_name = row[6]
            price = str(row[10])
            if row[12] == 9:
                step = 'в поиске исполнителя'
            elif row[12] == 10:
                step = 'выполняется'
            elif row[12] == 12:
                step = 'закончен, неоплачен'
            elif row[12] == 13:
                step = 'закончен, оплачен'
            order = f"№{order_id} - {key_name} | {price}₽ | {step}"
            orders.append(order)
    orders_history = '\n'.join(orders)
    return orders_history


cursor.execute(f"SELECT * FROM orders")
rows = cursor.fetchall()
print(rows)