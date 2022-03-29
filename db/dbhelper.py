import sqlite3

DB_FILES = './db/shopping.db'



def create_tables():
    f_name = 'db/store-schema.sql'
    with open(f_name, 'r', encoding='utf-8') as f:
        sql = f.read()
        conn = sqlite3.connect(DB_FILES)
        try:
            conn.executescript(sql)
            print('Database Initialization success')
        except Exception as e:
            print('Database Initialization Failed')
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
            print('Dataloading success')
        except Exception as e:
            print('Dataloading failed')
            print(e)
        finally:
            conn.close()
