import psycopg2
from requests_functions import delete_tables, create_tables, create_new_user, update_phone_number, update_existing_user, find_user_by_something, find_user_by_phone, delete_user


if __name__ == '__main__':
    with psycopg2.connect(database="postgres", user="postgres", password="3132146") as conn:
        with conn.cursor() as cur:
            delete_tables(conn, cur)
            create_tables(conn, cur)
            create_new_user(conn, cur, 'Kirill', 'Kovalyov', 'kovalyovkirill@gmail.com')
            update_phone_number(conn, cur, 1, '89262759282')
            update_existing_user(conn, cur, 1, name='Vasya', surname='Ivanov', email='test@test.ru')
            find_user_by_something(conn, cur, 'Vasya')
            find_user_by_phone(conn, cur, '89262759282')
            delete_user(conn, cur, 1)

