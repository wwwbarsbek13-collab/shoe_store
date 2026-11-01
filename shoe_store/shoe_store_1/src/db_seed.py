import sqlite3
from pathlib import Path

DB = Path(__file__).parent.parent / "db" / "shoe_store.sqlite"

def get_connection():
    conn = sqlite3.connect(DB)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def seed_all():
    conn = get_connection()
    c = conn.cursor()
    for t in ["order_items","orders","stock_items","products","users","sizes","roles"]:
        c.execute(f"DELETE FROM {t}")

    c.executemany("INSERT INTO roles (role_name) VALUES (?)",
        [("администратор",), ("менеджер",), ("авторизованный пользователь",)])

    c.executemany("INSERT INTO users (last_name,first_name,middle_name,login,role_id) VALUES (?,?,?,?,?)",
        [("Иванов","Иван","Иванович","admin",1),
         ("Петров","Пётр","Петрович","manager",2),
         ("Сидоров","Сидор",None,"user",3)])

    c.executemany("INSERT INTO sizes (size_value) VALUES (?)",
        [(36.0,),(37.0,),(38.0,),(39.0,),(40.0,)])

    c.executemany("""INSERT INTO products
        (category,subcategory,manufacturer,product_name,image_path,composition,description,price)
        VALUES (?,?,?,?,?,?,?,?)""",
        [("Спортивная","Кроссовки","Nike","Кроссовки RunFast","img/nike.jpg","Текстиль","Лёгкие",8999.00),
         ("Зимняя","Ботинки","Ecco","Ботинки WinterPro","img/ecco.jpg","Кожа","Тёплые",12999.50),
         ("Классическая","Туфли","Clarks","Туфли Classic","img/clarks.jpg","Кожа","Строгие",7499.00),
         ("Летняя","Сандалии","Adidas","Сандалии Summer","img/adidas.jpg","Синтетика","Открытые",3499.99),
         ("Повседневная","Кеды","Puma","Кеды Street","img/puma.jpg","Текстиль","Универсальные",5999.00)])

    c.executemany("INSERT INTO stock_items (product_id,size_id,quantity_available) VALUES (?,?,?)",
        [(1,1,10),(1,2,15),(1,3,20),(2,3,5),(2,4,8),
         (3,2,12),(3,3,7),(4,1,25),(4,2,30),(5,4,18)])

    c.executemany("INSERT INTO orders (user_id,order_date) VALUES (?,?)",
        [(3,"2024-01-15"),(2,"2024-01-16"),(3,"2024-01-17")])

    c.executemany("INSERT INTO order_items (order_id,stock_item_id,quantity,price) VALUES (?,?,?,?)",
        [(1,1,1,8999.00),(1,8,2,3499.99),(2,4,1,12999.50),
         (2,6,1,7499.00),(3,2,1,8999.00),(3,10,1,5999.00)])

    conn.commit()
    conn.close()
    print("Данные вставлены.")

if __name__ == "__main__":
    seed_all()