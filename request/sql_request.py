import sqlite3


async def create_table():
    try:
        con = sqlite3.connect("User.db")
        cur = con.cursor()

        cur.execute("CREATE TABLE IF NOT EXISTS user_table ("
                    "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                    "user_id INTEGER, "
                    "user_name TEXT, "
                    "count_baseboard INTEGER, "
                    "height_baseboard TEXT, "
                    "zapil_quantity_v TEXT, "
                    "zapil_quantity_k TEXT, "
                    "zapil_quantity_m TEXT, "
                    "sealing_uniq TEXT, "
                    "sealing_up TEXT, "
                    "freight_elevator TEXT, "
                    "material_baseboard TEXT, "
                    "address_baseboard TEXT, "
                    "date TEXT, "
                    "price INTEGER, "
                    "phone_baseboard TEXT)")
        con.commit()
    except sqlite3.Error as e:
        print("SQLite error:", e)


async def insert_into_user_table(user_id, user_name, count_baseboard, height_baseboard, material_baseboard,
                                 address_baseboard, phone_baseboard, date, price,
                                 zapil_quantity_v, zapil_quantity_k, zapil_quantity_m, freight_elevator, sealing_uniq,
                                 sealing_up):
    try:
        con = sqlite3.connect("User.db")
        cur = con.cursor()

        cur.execute("INSERT INTO user_table (user_id, user_name, count_baseboard, height_baseboard, "
                    "material_baseboard, address_baseboard, phone_baseboard, date, price, "
                    "zapil_quantity_v, zapil_quantity_k, zapil_quantity_m, freight_elevator, sealing_uniq, sealing_up) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (user_id, user_name, count_baseboard, height_baseboard, material_baseboard, address_baseboard,
                     phone_baseboard, date, price, zapil_quantity_v, zapil_quantity_k,
                     zapil_quantity_m, freight_elevator, sealing_uniq, sealing_up))
        con.commit()

    except sqlite3.Error as e:
        print("SQLite error:", e)


async def select_all(date):
    try:
        con = sqlite3.connect("User.db")
        cur = con.cursor()

        cur.execute("SELECT user_id, price FROM user_table WHERE date = ?", (date,))
        result = cur.fetchall()

        if result is not None:
            return result
        else:
            return result

    except sqlite3.Error as e:
        print("SQLite error:", e)