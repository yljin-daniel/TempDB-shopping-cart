import sqlite3

DB_FILES = './db/database.db'


def create_tables():
    f_name = 'db/store-schema.sql'
    with open(f_name, 'r', encoding='utf-8') as f:
        sql = f.read()
        conn = sqlite3.connect(DB_FILES)
        try:
            conn.executescript(sql)
            print('数据库初始化成功')
        except Exception as e:
            print('数据库初始化失败')
            print(e)
        finally:
            conn.close()


def load_data():
    f_name = './db/store-dataload.sql'
    with open(f_name, 'r', encoding='utf-8') as f:
        sql = f.read()
        conn = sqlite3.connect(DB_FILES)
        try:
            conn.executescript(sql)
            print('数据库插入成功')
        except Exception as e:
            print('数据库插入失败')
            print(e)
        finally:
            conn.close()
