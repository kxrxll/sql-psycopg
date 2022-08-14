import psycopg2


def create_tables():
    with psycopg2.connect(database="postgres", user="postgres", password="3132146") as conn:
        with conn.cursor() as cur:
            cur.execute("""
            CREATE TABLE IF NOT EXISTS phonenumbers(
                id SERIAL PRIMARY KEY,
                number VARCHAR(40) NOT NULL
            );
            """)
            cur.execute("""
            CREATE TABLE IF NOT EXISTS users(
                id SERIAL PRIMARY KEY,
                name VARCHAR(40) NOT NULL,
                surname VARCHAR(40) NOT NULL,
                email VARCHAR(40) NOT NULL,
                number_id INTEGER REFERENCES phonenumbers(id)
            );
            """)
            conn.commit()


def delete_tables():
    with psycopg2.connect(database="postgres", user="postgres", password="3132146") as conn:
        with conn.cursor() as cur:
            cur.execute("""
            DROP TABLE users;
            DROP TABLE phonenumbers;
            """)
            conn.commit()


def create_new_user(name, surname, email):
    with psycopg2.connect(database="postgres", user="postgres", password="3132146") as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO users (name, surname, email) VALUES (%s, %s, %s);", (name, surname, email))
            conn.commit()


def update_phone_number(user_id, number):
    with psycopg2.connect(database="postgres", user="postgres", password="3132146") as conn:
        with conn.cursor() as cur:
            cur.execute("""
                   INSERT INTO phonenumbers (number) VALUES (%s) RETURNING id;
                   """, (number,))
            phone_id = cur.fetchone()[0]
            cur.execute("""
                   UPDATE users SET number_id=%s WHERE id=%s;
                   """, (phone_id, user_id))
            conn.commit()


def update_existing_user(user_id, name, surname, email):
    with psycopg2.connect(database="postgres", user="postgres", password="3132146") as conn:
        with conn.cursor() as cur:
            cur.execute("""
                   UPDATE users SET name=%s, surname=%s, email=%s WHERE id=%s;
                   """, (name, surname, email, user_id))
            conn.commit()


def unlink_phones(user_id):
    with psycopg2.connect(database="postgres", user="postgres", password="3132146") as conn:
        with conn.cursor() as cur:
            cur.execute("""
                   UPDATE users SET number_id=NULL WHERE id=%s;
                   """, (user_id,))
            conn.commit()


def delete_phone_number(phone_id):
    with psycopg2.connect(database="postgres", user="postgres", password="3132146") as conn:
        with conn.cursor() as cur:
            cur.execute("""
                    DELETE FROM phonenumbers WHERE id=%s;
                    """, (phone_id,))
            conn.commit()


def delete_user(user_id):
    with psycopg2.connect(database="postgres", user="postgres", password="3132146") as conn:
        with conn.cursor() as cur:
            cur.execute("""
                    SELECT * FROM users WHERE id=%s;
                    """, (user_id,))
            phone = cur.fetchone()[4]
            unlink_phones(user_id)
            delete_phone_number(phone)
            cur.execute("""
                    DELETE FROM users WHERE id=%s;
                    """, (user_id,))
            conn.commit()


def find_user_by_name(name):
    with psycopg2.connect(database="postgres", user="postgres", password="3132146") as conn:
        with conn.cursor() as cur:
            cur.execute("""
                    SELECT * FROM users WHERE name=%s;
                    """, (name,))
            print(cur.fetchone())
            conn.commit()


def find_user_by_phone(phone_number):
    with psycopg2.connect(database="postgres", user="postgres", password="3132146") as conn:
        with conn.cursor() as cur:
            cur.execute("""
                    SELECT * FROM phonenumbers WHERE number=%s;
                    """, (phone_number,))
            phone_id = cur.fetchone()[0]
            cur.execute("""
                    SELECT * FROM users WHERE number_id=%s;
                    """, (phone_id,))
            print(cur.fetchone())
            conn.commit()


delete_tables()
create_tables()
create_new_user('Kirill', 'Kovalyov', 'kovalyovkirill@gmail.com')
update_phone_number(1, '89262759282')
update_existing_user(1, 'Vasya', 'Ivanov', 'test@test.ru')
find_user_by_name('Vasya')
find_user_by_phone('89262759282')
delete_user(1)
