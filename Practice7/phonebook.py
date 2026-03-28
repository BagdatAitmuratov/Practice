import psycopg2
import csv
from config import parametrs
#1.1
def crate_table():
    conn_str = f"host='{parametrs['host']}' dbname='{parametrs['database']}' user='{parametrs['user']}' password='{parametrs['password']}'"
    with psycopg2.connect(**parametrs) as conn:
        with conn.cursor() as f:
            f.execute('''
                CREATE TABLE IF NOT EXISTS phonebook (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(250),
                    phone VARCHAR(25)
                );
            ''')
        conn.commit()
#1.2
def insetr_csv(file):
    with psycopg2.connect(**parametrs) as conn:
        with conn.cursor() as c:
            with open(file, 'r', encoding='utf-8') as f:
                r = csv.reader(f)
                for row in r:
                    c.execute("INSERT INTO phonebook (name, phone) VALUES (%s, %s)", row)
        conn.commit()
#1.3
def add_contact(name, phone):
    with psycopg2.connect(**parametrs) as conn:
        with conn.cursor() as throw:
            throw.execute("INSERT INTO phonebook (name, phone) VALUES (%s, %s)", (name, phone))
        conn.commit()
#1.4
def update_contact(name, new_phone):
    with psycopg2.connect(**parametrs) as conn:
        with conn.cursor() as update:
            update.execute("UPDATE phonebook SET phone=%s WHERE name=%s", (new_phone, name))
        conn.commit()
#1.5
def contact_find(soz):
    with psycopg2.connect(**parametrs) as conn:
        with conn.cursor() as throw:
            throw.execute("SELECT * FROM phonebook WHERE name LIKE %s OR phone LIKE %s", (f'%{soz}%', f'{soz}%'))
            res = throw.fetchall()
            if res:
                for row in res: print(row)
            else:
                pass
#1.6
def contact_del(name):
    with psycopg2.connect(**parametrs) as conn:
        with conn.cursor() as throw:
            throw.execute("DELETE FROM phonebook WHERE name = %s", (name,))
        conn.commit()
def menu():
    crate_table();
    while True:
        print("\n--- PhoneBook menu ---")
        print("1: CSV\n2: Қосу \n3: Жаңарту \n4: Іздеу \n5: Өшіру \n0: Шығу")
        sol = input("Tangdau: ")

        if sol == '1':
            insetr_csv('contacts.csv')
        elif sol == '2':
            add_contact(input("Аты: "), input("Телефон: "))
        elif sol == '3':
            update_contact(input("Кімді өзгертеміз (аты): "), input("Жаңа нөмір: "))
        elif sol == '4':
            contact_find(input("Іздеу үшін ат немесе нөмір жазыңыз: "))
        elif sol == '5':
            contact_del(input("Кімді өшіреміз: "))
        elif sol == '0':
            print("Сау болыңыз!")
            break
        else:
            print("Қате таңдау, қайта көріңіз.")

    menu()