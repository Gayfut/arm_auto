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
                password TEXT
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
                transmission_type TEXT
            )
        ''')

        # Таблица для хранения информации о клиентах
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS clients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT,
                birth_year INTEGER,
                gender TEXT,
                registration_date TEXT
            )
        ''')

        # Таблица для хранения информации о заявках на просмотр
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                car_id INTEGER,
                client_id INTEGER,
                viewing_date TEXT,
                FOREIGN KEY (car_id) REFERENCES cars (id),
                FOREIGN KEY (client_id) REFERENCES clients (id)
            )
        ''')

        self.conn.commit()

    def add_car(self, brand, color, year, engine_volume, horsepower, transmission_type):
        self.cursor.execute('''
            INSERT INTO cars (brand, color, year, engine_volume, horsepower, transmission_type)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (brand, color, year, engine_volume, horsepower, transmission_type))
        self.conn.commit()

    def add_client(self, full_name, birth_year, gender, registration_date):
        self.cursor.execute('''
            INSERT INTO clients (full_name, birth_year, gender, registration_date)
            VALUES (?, ?, ?, ?)
        ''', (full_name, birth_year, gender, registration_date))
        self.conn.commit()

    def add_application(self, car_id, client_id, viewing_date):
        self.cursor.execute('''
            INSERT INTO applications (car_id, client_id, viewing_date)
            VALUES (?, ?, ?)
        ''', (car_id, client_id, viewing_date))
        self.conn.commit()

    def get_cars(self):
        self.cursor.execute('SELECT * FROM cars')
        return self.cursor.fetchall()

    def get_clients(self):
        self.cursor.execute('SELECT * FROM clients')
        return self.cursor.fetchall()

    def get_applications(self):
        self.cursor.execute('SELECT * FROM applications')
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

    def edit_car(self, car_id, brand, color, year, engine_volume, horsepower, transmission_type):
        self.cursor.execute('''
            UPDATE cars
            SET brand=?, color=?, year=?, engine_volume=?, horsepower=?, transmission_type=?
            WHERE id=?
        ''', (brand, color, year, engine_volume, horsepower, transmission_type, car_id))
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
