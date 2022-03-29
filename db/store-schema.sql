--
-- File generated with SQLiteStudio v3.3.3 on Mon Mar 28 18:40:59 2022
--
-- Text encoding used: System
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: item
DROP TABLE IF EXISTS item;
CREATE TABLE item (item_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, item_group_id INTEGER NOT NULL, name TEXT NOT NULL, description TEXT, price REAL NOT NULL);


-- Table: item_group
DROP TABLE IF EXISTS item_group;
CREATE TABLE item_group (item_group_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, item_group_name TEXT NOT NULL, description TEXT);


-- Table: order
DROP TABLE IF EXISTS orders;
CREATE TABLE orders (order_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, user_id INTEGER NOT NULL, item_id INTEGER NOT NULL, order_date TEXT NOT NULL, final_price REAL NOT NULL);

-- Table: shopping_cart
DROP TABLE IF EXISTS shopping_cart;
CREATE TABLE shopping_cart (cart_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, user_id INTEGER NOT NULL, item_id INTEGER NOT NULL, item_quantity INTEGER NOT NULL);

-- Table: user
DROP TABLE IF EXISTS user;
create table user
(
   user_id              varchar(20) primary key,
   name                 varchar(100) not null,
   password             varchar(100) not null,
   address              varchar(100),
   phone_number         varchar(20),
   email                varchar(100)
);

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
