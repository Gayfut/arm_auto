import tkinter as tk
from tkinter import ttk


class MainWindow:
    def __init__(self, root, database):
        self.root = root
        self.root.title("Главная страница")
        self.database = database

        # Определение стилей
        self.root.configure(bg='white')

        # Создаем табличный ноутбук для вкладок
        self.notebook = ttk.Notebook(self.root)

        # Вкладка "Автомобили"
        self.tab_cars = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_cars, text="Автомобили")
        self.create_cars_tab()

        # Вкладка "Клиенты"
        self.tab_clients = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_clients, text="Клиенты")
        self.create_clients_tab()

        # Вкладка "Заявки на просмотр"
        self.tab_applications = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_applications, text="Заявки на просмотр")
        self.create_applications_tab()

        self.notebook.pack(fill="both", expand=True)

        # Заполнение вкладок при открытии приложения
        self.refresh_cars_table()
        self.refresh_clients_table()
        self.refresh_applications_table()

    def create_cars_tab(self):
        self.tree_cars = ttk.Treeview(self.tab_cars, columns=("ID", "Brand", "Color", "Year", "Engine Volume", "Horsepower", "Transmission Type"), show="headings")
        self.tree_cars.heading("ID", text="id")
        self.tree_cars.heading("Brand", text="Марка")
        self.tree_cars.heading("Color", text="Цвет")
        self.tree_cars.heading("Year", text="Год")
        self.tree_cars.heading("Engine Volume", text="Объем двигателя")
        self.tree_cars.heading("Horsepower", text="Лошадиные силы")
        self.tree_cars.heading("Transmission Type", text="Тип коробки")

        self.tree_cars.pack()

        btn_add_car = ttk.Button(self.tab_cars, text="Добавить", command=self.add_car_window)
        btn_add_car.pack()

    def create_clients_tab(self):
        self.tree_clients = ttk.Treeview(self.tab_clients, columns=("ID", "Full Name", "Birth Year", "Gender", "Registration Date"), show="headings")
        self.tree_clients.heading("ID", text="id")
        self.tree_clients.heading("Full Name", text="ФИО")
        self.tree_clients.heading("Birth Year", text="Год рождения")
        self.tree_clients.heading("Gender", text="Пол")
        self.tree_clients.heading("Registration Date", text="Дата регистрации")

        self.tree_clients.pack()

        btn_add_client = ttk.Button(self.tab_clients, text="Добавить", command=self.add_client_window)
        btn_add_client.pack()

    def create_applications_tab(self):
        self.tree_applications = ttk.Treeview(self.tab_applications, columns=("ID", "Car", "Client", "Viewing Date"), show="headings")
        self.tree_applications.heading("ID", text="id")
        self.tree_applications.heading("Car", text="Автомобиль")
        self.tree_applications.heading("Client", text="Клиент")
        self.tree_applications.heading("Viewing Date", text="Дата просмотра")

        self.tree_applications.pack()

        btn_add_application = ttk.Button(self.tab_applications, text="Добавить", command=self.add_application_window)
        btn_add_application.pack()

    def add_car_window(self):
        add_car_window = tk.Toplevel(self.root)
        add_car_window.title("Добавить автомобиль")

        # Создаем и размещаем элементы интерфейса для добавления автомобиля
        label_brand = ttk.Label(add_car_window, text="Марка:")
        label_brand.pack()

        brand_entry = ttk.Entry(add_car_window)
        brand_entry.pack()

        label_color = ttk.Label(add_car_window, text="Цвет:")
        label_color.pack()

        color_entry = ttk.Entry(add_car_window)
        color_entry.pack()

        label_year = ttk.Label(add_car_window, text="Год:")
        label_year.pack()

        year_entry = ttk.Entry(add_car_window)
        year_entry.pack()

        label_engine_volume = ttk.Label(add_car_window, text="Объем двигателя:")
        label_engine_volume.pack()

        engine_volume_entry = ttk.Entry(add_car_window)
        engine_volume_entry.pack()

        label_horsepower = ttk.Label(add_car_window, text="Лошадиные силы:")
        label_horsepower.pack()

        horsepower_entry = ttk.Entry(add_car_window)
        horsepower_entry.pack()

        label_transmission_type = ttk.Label(add_car_window, text="Тип коробки:")
        label_transmission_type.pack()

        transmission_type_entry = ttk.Entry(add_car_window)
        transmission_type_entry.pack()

        btn_add = ttk.Button(add_car_window, text="Добавить", command=lambda: self.add_car(add_car_window, brand_entry.get(), color_entry.get(), year_entry.get(), engine_volume_entry.get(), horsepower_entry.get(), transmission_type_entry.get()))
        btn_add.pack()

    def add_car(self, add_car_window, brand, color, year, engine_volume, horsepower, transmission_type):
        self.database.add_car(brand, color, year, engine_volume, horsepower, transmission_type)
        add_car_window.destroy()
        # Обновляем отображение таблицы с автомобилями
        self.refresh_cars_table()

    def refresh_cars_table(self):
        # Очищаем таблицу перед обновлением
        for row in self.tree_cars.get_children():
            self.tree_cars.delete(row)

        # Получаем данные из базы данных и добавляем их в таблицу
        cars = self.database.get_cars()
        for car in cars:
            self.tree_cars.insert("", "end", values=car)

    def add_client_window(self):
        add_client_window = tk.Toplevel(self.root)
        add_client_window.title("Добавить клиента")

        # Создаем и размещаем элементы интерфейса для добавления клиента
        label_full_name = ttk.Label(add_client_window, text="ФИО:")
        label_full_name.pack()

        full_name_entry = ttk.Entry(add_client_window)
        full_name_entry.pack()

        label_birth_year = ttk.Label(add_client_window, text="Год рождения:")
        label_birth_year.pack()

        birth_year_entry = ttk.Entry(add_client_window)
        birth_year_entry.pack()

        label_gender = ttk.Label(add_client_window, text="Пол:")
        label_gender.pack()

        gender_entry = ttk.Entry(add_client_window)
        gender_entry.pack()

        label_registration_date = ttk.Label(add_client_window, text="Дата регистрации:")
        label_registration_date.pack()

        registration_date_entry = ttk.Entry(add_client_window)
        registration_date_entry.pack()

        btn_add = ttk.Button(add_client_window, text="Добавить", command=lambda: self.add_client(add_client_window, full_name_entry.get(), birth_year_entry.get(), gender_entry.get(), registration_date_entry.get()))
        btn_add.pack()

    def add_client(self, add_client_window, full_name, birth_year, gender, registration_date):
        self.database.add_client(full_name, birth_year, gender, registration_date)
        add_client_window.destroy()
        # Обновляем отображение таблицы с клиентами
        self.refresh_clients_table()

    def refresh_clients_table(self):
        # Очищаем таблицу перед обновлением
        for row in self.tree_clients.get_children():
            self.tree_clients.delete(row)

        # Получаем данные из базы данных и добавляем их в таблицу
        clients = self.database.get_clients()
        for client in clients:
            self.tree_clients.insert("", "end", values=client)

    def add_application_window(self):
        add_application_window = tk.Toplevel(self.root)
        add_application_window.title("Добавить заявку на просмотр")

        # Создаем и размещаем элементы интерфейса для добавления заявки на просмотр
        label_car_id = ttk.Label(add_application_window, text="ID Автомобиля:")
        label_car_id.pack()

        car_id_entry = ttk.Entry(add_application_window)
        car_id_entry.pack()

        label_client_id = ttk.Label(add_application_window, text="ID Клиента:")
        label_client_id.pack()

        client_id_entry = ttk.Entry(add_application_window)
        client_id_entry.pack()

        label_viewing_date = ttk.Label(add_application_window, text="Дата просмотра:")
        label_viewing_date.pack()

        viewing_date_entry = ttk.Entry(add_application_window)
        viewing_date_entry.pack()

        btn_add = ttk.Button(add_application_window, text="Добавить", command=lambda: self.add_application(add_application_window, car_id_entry.get(), client_id_entry.get(), viewing_date_entry.get()))
        btn_add.pack()

    def add_application(self, add_application_window, car_id, client_id, viewing_date):
        self.database.add_application(car_id, client_id, viewing_date)
        add_application_window.destroy()
        # Обновляем отображение таблицы с заявками на просмотр
        self.refresh_applications_table()

    def refresh_applications_table(self):
        # Очищаем таблицу перед обновлением
        for row in self.tree_applications.get_children():
            self.tree_applications.delete(row)

        # Получаем данные из базы данных и добавляем их в таблицу
        applications = self.database.get_applications()
        for application in applications:
            self.tree_applications.insert("", "end", values=application)
