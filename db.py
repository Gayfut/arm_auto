import sqlite3


class Database:
    def __init__(self, db_name='автосалон.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_users_table()
        self.create_tables()

    def create_users_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                password TEXT,
                is_admin BOOLEAN
            )
        ''')
        self.conn.commit()

    def check_user_credentials(self, username, password):
        self.cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        return self.cursor.fetchone()

    def close_connection(self):
        self.conn.close()

    def create_tables(self):
        # Таблица для хранения информации об автомобилях
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS cars (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                brand TEXT,
                color TEXT,
                year INTEGER,
                engine_volume REAL,
                horsepower INTEGER,
                transmission_type TEXT,
                photo BLOB
            )
        ''')

        # Таблица для хранения информации о клиентах
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS clients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT,
                birth_year DATE,
                gender TEXT,
                registration_date DATE
            )
        ''')

        # Таблица для хранения информации о заявках на просмотр
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                car_id INTEGER,
                client_id INTEGER,
                viewing_date DATE,
                is_shown BOOLEAN NOT NULL DEFAULT FALSE,
                FOREIGN KEY (car_id) REFERENCES cars (id),
                FOREIGN KEY (client_id) REFERENCES clients (id)
            )
        ''')

        self.conn.commit()

    def add_car(self, brand, color, year, engine_volume, horsepower, transmission_type, photo):
        self.cursor.execute('''
            INSERT INTO cars (brand, color, year, engine_volume, horsepower, transmission_type, photo)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (brand, color, year, engine_volume, horsepower, transmission_type, photo))
        self.conn.commit()

    def add_client(self, full_name, birth_year, gender, registration_date):
        self.cursor.execute('''
            INSERT INTO clients (full_name, birth_year, gender, registration_date)
            VALUES (?, ?, ?, ?)
        ''', (full_name, birth_year, gender, registration_date))
        self.conn.commit()

    def add_application(self, car_id, client_id, viewing_date):
        self.cursor.execute('''
            INSERT INTO applications (car_id, client_id, viewing_date, is_shown)
            VALUES (?, ?, ?, ?)
        ''', (car_id, client_id, viewing_date, False))
        self.conn.commit()

    def get_cars(self):
        self.cursor.execute('SELECT * FROM cars')
        return self.cursor.fetchall()

    def get_clients(self):
        self.cursor.execute('SELECT * FROM clients')
        return self.cursor.fetchall()

    def get_applications(self, all_applications=False):
        if all_applications:
            self.cursor.execute('SELECT * FROM applications')
        else:
            self.cursor.execute('SELECT * FROM applications WHERE is_shown=?', (False,))
        return self.cursor.fetchall()

    def delete_car(self, car_id):
        self.cursor.execute("DELETE FROM cars WHERE id=?", (car_id,))
        self.conn.commit()

    def delete_client(self, client_id):
        self.cursor.execute("DELETE FROM clients WHERE id=?", (client_id,))
        self.conn.commit()

    def delete_application(self, application_id):
        self.cursor.execute("DELETE FROM applications WHERE id=?", (application_id,))
        self.conn.commit()

    def edit_car(self, car_id, brand, color, year, engine_volume, horsepower, transmission_type, photo):
        self.cursor.execute('''
            UPDATE cars
            SET brand=?, color=?, year=?, engine_volume=?, horsepower=?, transmission_type=?, photo=?
            WHERE id=?
        ''', (brand, color, year, engine_volume, horsepower, transmission_type, photo, car_id))
        self.conn.commit()

    def edit_client(self, client_id, full_name, birth_year, gender, registration_date):
        self.cursor.execute('''
            UPDATE clients
            SET full_name=?, birth_year=?, gender=?, registration_date=?
            WHERE id=?
        ''', (full_name, birth_year, gender, registration_date, client_id))
        self.conn.commit()

    def edit_application(self, application_id, car_id, client_id, viewing_date):
        self.cursor.execute('''
            UPDATE applications
            SET car_id=?, client_id=?, viewing_date=?
            WHERE id=?
        ''', (car_id, client_id, viewing_date, application_id))
        self.conn.commit()

    def get_car(self, car_id):
        self.cursor.execute("SELECT * FROM cars WHERE id=?", (car_id,))
        return self.cursor.fetchone()

    def get_client(self, client_id):
        self.cursor.execute("SELECT * FROM clients WHERE id=?", (client_id,))
        return self.cursor.fetchone()

    def get_application(self, application_id):
        self.cursor.execute("SELECT * FROM applications WHERE id=?", (application_id,))
        return self.cursor.fetchone()

    def get_username_by_id(self, user_id):
        self.cursor.execute("SELECT username FROM users WHERE id=?", (user_id,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def get_car_name_by_id(self, car_id):
        self.cursor.execute("SELECT brand FROM cars WHERE id=?", (car_id,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def get_client_name_by_id(self, client_id):
        self.cursor.execute("SELECT full_name FROM clients WHERE id=?", (client_id,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def mark_application_as_shown(self, application_id):
        self.cursor.execute("""
            UPDATE applications
            SET is_shown = ?
            WHERE id = ?
        """, (True, application_id,))
        self.conn.commit()

    def user_is_admin(self, user_id):
        self.cursor.execute("SELECT is_admin FROM users WHERE id=?", (user_id,))
        result = self.cursor.fetchone()
        return result[0] if result else False

    def add_user(self, username, password, is_admin):
        self.cursor.execute('''
            INSERT INTO users (username, password, is_admin)
            VALUES (?, ?, ?)
        ''', (username, password, is_admin))
        self.conn.commit()

    def delete_user(self, user_id):
        self.cursor.execute("DELETE FROM users WHERE id=?", (user_id,))
        self.conn.commit()

    def get_user(self, user_id):
        self.cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
        return self.cursor.fetchone()

    def edit_user(self, user_id, username, password, is_admin):
        self.cursor.execute('''
            UPDATE users
            SET username=?, password=?, is_admin=?
            WHERE id=?
        ''', (username, password, is_admin, user_id))
        self.conn.commit()

    def get_users(self, current_user_id):
        self.cursor.execute('SELECT * FROM users WHERE id<>?', (current_user_id,))
        return self.cursor.fetchall()

    def check_car(self, car_id):
        self.cursor.execute("SELECT id FROM applications WHERE car_id=?", (car_id,))
        result = self.cursor.fetchone()

        if result:
            car_used = True
        else:
            car_used = False

        return car_used

    def check_client(self, client_id):
        self.cursor.execute("SELECT id FROM applications WHERE client_id=?", (client_id,))
        result = self.cursor.fetchone()

        if result:
            client_used = True
        else:
            client_used = False

        return client_used