def create_tables(conn, cur):
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


def delete_tables(conn, cur):
    cur.execute("""
            DROP TABLE users;
            DROP TABLE phonenumbers;
            """)
    conn.commit()


def create_new_user(conn, cur, name, surname, email):
    cur.execute("INSERT INTO users (name, surname, email) VALUES (%s, %s, %s);", (name, surname, email))
    conn.commit()


def update_phone_number(conn, cur, user_id, number):
    cur.execute("""
                   INSERT INTO phonenumbers (number) VALUES (%s) RETURNING id;
                   """, (number,))
    phone_id = cur.fetchone()[0]
    cur.execute("""
                   UPDATE users SET number_id=%s WHERE id=%s;
                   """, (phone_id, user_id))
    conn.commit()


def update_existing_user(conn, cur, user_id, name='', surname='', email=''):
    if name and surname and email:
        cur.execute("UPDATE users SET name=%s, surname=%s, email=%s WHERE id=%s;", (name, surname, email, user_id))
    elif not email:
        cur.execute("UPDATE users SET name=%s, surname=%s WHERE id=%s;", (name, surname, user_id))
    elif not surname:
        cur.execute("UPDATE users SET name=%s, email=%s WHERE id=%s;", (name, email, user_id))
    elif not name:
        cur.execute("UPDATE users SET surname=%s, email=%s WHERE id=%s;", (surname, email, user_id))
    elif not email and not surname:
        cur.execute("UPDATE users SET name=%s WHERE id=%s;", (name, user_id))
    elif not name and not surname:
        cur.execute("UPDATE users SET email=%s WHERE id=%s;", (email, user_id))
    elif not name and not email:
        cur.execute("UPDATE users SET surname=%s WHERE id=%s;", (surname, user_id))
    conn.commit()


def unlink_phones(conn, cur, user_id):
    cur.execute("""
                   UPDATE users SET number_id=NULL WHERE id=%s;
                   """, (user_id,))
    conn.commit()


def delete_phone_number(conn, cur, phone_id):
    cur.execute("""
                    DELETE FROM phonenumbers WHERE id=%s;
                    """, (phone_id,))
    conn.commit()


def delete_user(conn, cur, user_id):
    cur.execute("""
                    SELECT * FROM users WHERE id=%s;
                    """, (user_id,))
    phone = cur.fetchone()[4]
    unlink_phones(conn, cur, user_id)
    delete_phone_number(conn, cur, phone)
    cur.execute("""
                    DELETE FROM users WHERE id=%s;
                    """, (user_id,))
    conn.commit()


def find_user_by_something(conn, cur, something):
    cur.execute("""
                    SELECT * FROM users WHERE %s=%s;
                    """, (something, something))
    print(cur.fetchone())
    conn.commit()


def find_user_by_phone(conn, cur, phone_number):
    cur.execute("""
                    SELECT * FROM phonenumbers WHERE number=%s;
                    """, (phone_number,))
    phone_id = cur.fetchone()[0]
    cur.execute("""
                    SELECT * FROM users WHERE number_id=%s;
                    """, (phone_id,))
    print(cur.fetchone())
    conn.commit()
