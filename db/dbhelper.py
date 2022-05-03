import sqlite3

DB_FILES = './db/database.db'


def create_tables():
    f_name = 'db/store-schema.sql'
    with open(f_name, 'r', encoding='utf-8') as f:
        sql = f.read()
        conn = sqlite3.connect(DB_FILES)
        try:
            conn.executescript(sql)
            print('Database Initialization Success')
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
            print('Data Successfully Loaded')
        except Exception as e:
            print('Data Loading Failed')
            print(e)
        finally:
            conn.close()
