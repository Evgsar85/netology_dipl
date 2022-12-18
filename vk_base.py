import psycopg2
from my_config import *

conn = psycopg2.connect(
    host=host,
    user=user,
    password=password,
    database=db_name
)

conn.autocommit = True

def create_table_units_serch(): 
    
    with conn.cursor() as cursor:
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS units_serch(
                id serial,
                name varchar(50) NOT NULL,
                surname varchar(25) NOT NULL,
                vk_id varchar(20) NOT NULL PRIMARY KEY,
                vk_link varchar(50));"""
        )
    print("Table UNITS was created.")


def create_table_units_seen():  # references users(vk_id)
    
    with conn.cursor() as cursor:
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS units_seen(
            id serial,
            vk_id varchar(50) PRIMARY KEY);"""
        )
    print("Table UNITS_SEEN was created.")


def insert_data_units_serch(name, surname, vk_id, vk_link):
    
    with conn.cursor() as cursor:
        cursor.execute(
            f"""INSERT INTO units_serch (name, surname, vk_id, vk_link) 
            VALUES ('{name}', '{surname}', '{vk_id}', '{vk_link}');"""
        )


def insert_data_units_seen(vk_id): # offset has been delited as nonfunctional parameter
    
    with conn.cursor() as cursor:
        cursor.execute(
            f"""INSERT INTO units_seen (vk_id) 
            VALUES ('{vk_id}');"""
        )


def select(offset):
    with conn.cursor() as cursor:
        cursor.execute(
            f"""SELECT u.name,
                        u.surname,
                        u.vk_id,
                        u.vk_link,
                        us.vk_id
                        FROM units_serch AS u
                        LEFT JOIN units_seen AS us 
                        ON u.vk_id = us.vk_id
                        WHERE us.vk_id IS NULL
                        OFFSET '{offset}';"""
        )
        return cursor.fetchone()


def drop_units_serch():
    with conn.cursor() as cursor:
        cursor.execute(
            """DROP TABLE IF EXISTS units_serch CASCADE;"""
        )
        print('Table UNITS_SERCH was deleted.')


def drop_units_seen():
    with conn.cursor() as cursor:
        cursor.execute(
            """DROP TABLE  IF EXISTS units_seen CASCADE;"""
        )
        print('Table UNITS_SEEN was deleted.')


def creating_database():
    drop_units_serch()
    drop_units_seen()
    create_table_units_serch()
    create_table_units_seen()

# with psycopg2.connect(database=db_name, user=user, password=password) as conn:
#     creating_database(conn)
