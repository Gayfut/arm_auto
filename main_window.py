import tkinter as tk
from tkinter import ttk, messagebox, BOTH


class MainWindow:
    def __init__(self, root, database, current_user):
        self.root = root
        self.root.title("Главная страница")
        self.root.protocol("WM_DELETE_WINDOW", self.close_event)

        self.database = database
        self.current_user = current_user

        self.cars = []
        self.clients = []

        # Определение стилей
        self.root.configure(bg='white')

        # Текущий пользователь
        self.label_current_user = ttk.Label(self.root, text=f"Пользователь: {self.current_user}",
                                            background='white', font=('Arial', 10))
        self.label_current_user.pack(side="top", padx=10, pady=5)

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

    def close_event(self):
        self.root.destroy()
        exit()

    def create_cars_tab(self):
        self.tree_cars = ttk.Treeview(self.tab_cars, columns=("ID", "Brand", "Color", "Year", "Engine Volume", "Horsepower", "Transmission Type"), show="headings")
        self.tree_cars.heading("ID", text="id")
        self.tree_cars.heading("Brand", text="Марка")
        self.tree_cars.heading("Color", text="Цвет")
        self.tree_cars.heading("Year", text="Год")
        self.tree_cars.heading("Engine Volume", text="Объем двигателя")
        self.tree_cars.heading("Horsepower", text="Лошадиные силы")
        self.tree_cars.heading("Transmission Type", text="Тип коробки")

        self.tree_cars.pack(fill=BOTH, expand=True)

        btn_add_car = ttk.Button(self.tab_cars, text="Добавить", command=self.add_car_window)
        btn_add_car.pack(side="left")

        btn_delete_car = ttk.Button(self.tab_cars, text="Удалить", command=self.delete_car)
        btn_delete_car.pack(side="right")

        btn_edit_car = ttk.Button(self.tab_cars, text="Редактировать", command=self.edit_car)
        btn_edit_car.pack(side="left")

    def create_clients_tab(self):
        self.tree_clients = ttk.Treeview(self.tab_clients, columns=("ID", "Full Name", "Birth Year", "Gender", "Registration Date"), show="headings")
        self.tree_clients.heading("ID", text="id")
        self.tree_clients.heading("Full Name", text="ФИО")
        self.tree_clients.heading("Birth Year", text="Год рождения")
        self.tree_clients.heading("Gender", text="Пол")
        self.tree_clients.heading("Registration Date", text="Дата регистрации")

        self.tree_clients.pack(fill=BOTH, expand=True)

        btn_add_client = ttk.Button(self.tab_clients, text="Добавить", command=self.add_client_window)
        btn_add_client.pack(side="left")

        btn_delete_client = ttk.Button(self.tab_clients, text="Удалить", command=self.delete_client)
        btn_delete_client.pack(side="right")

        btn_edit_client = ttk.Button(self.tab_clients, text="Редактировать", command=self.edit_client)
        btn_edit_client.pack(side="left")

    def create_applications_tab(self):
        self.tree_applications = ttk.Treeview(self.tab_applications, columns=("ID", "Car", "Client", "Viewing Date"), show="headings")
        self.tree_applications.heading("ID", text="id")
        self.tree_applications.heading("Car", text="Автомобиль")
        self.tree_applications.heading("Client", text="Клиент")
        self.tree_applications.heading("Viewing Date", text="Дата просмотра")

        self.tree_applications.pack(fill=BOTH, expand=True)

        btn_add_application = ttk.Button(self.tab_applications, text="Добавить", command=self.add_application_window)
        btn_add_application.pack(side="left")

        btn_delete_application = ttk.Button(self.tab_applications, text="Удалить", command=self.delete_application)
        btn_delete_application.pack(side="right")

        btn_edit_application = ttk.Button(self.tab_applications, text="Редактировать", command=self.edit_application)
        btn_edit_application.pack(side="left")

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

    def delete_car(self):
        selected_item = self.tree_cars.selection()

        if not selected_item:
            messagebox.showwarning("Предупреждение", "Выберите автомобиль для удаления.")
            return

        car_id = self.tree_cars.item(selected_item, "values")[0]
        self.database.delete_car(car_id)
        self.refresh_cars_table()

    def edit_car(self):
        selected_item = self.tree_cars.selection()

        if not selected_item:
            messagebox.showwarning("Предупреждение", "Выберите автомобиль для редактирования.")
            return

        car_id = self.tree_cars.item(selected_item, "values")[0]
        car_data = self.database.get_car(car_id)

        edit_car_window = tk.Toplevel(self.root)
        edit_car_window.title("Редактировать автомобиль")

        label_brand = ttk.Label(edit_car_window, text="Марка:")
        label_brand.pack()

        brand_entry = ttk.Entry(edit_car_window)
        brand_entry.insert(0, car_data[1])
        brand_entry.pack()

        label_color = ttk.Label(edit_car_window, text="Цвет:")
        label_color.pack()

        color_entry = ttk.Entry(edit_car_window)
        color_entry.insert(1, car_data[2])
        color_entry.pack()

        label_year = ttk.Label(edit_car_window, text="Год:")
        label_year.pack()

        year_entry = ttk.Entry(edit_car_window)
        year_entry.insert(2, car_data[3])
        year_entry.pack()

        label_engine_volume = ttk.Label(edit_car_window, text="Объем двигателя:")
        label_engine_volume.pack()

        engine_volume_entry = ttk.Entry(edit_car_window)
        engine_volume_entry.insert(3, car_data[4])
        engine_volume_entry.pack()

        label_horsepower = ttk.Label(edit_car_window, text="Лошадиные силы:")
        label_horsepower.pack()

        horsepower_entry = ttk.Entry(edit_car_window)
        horsepower_entry.insert(4, car_data[5])
        horsepower_entry.pack()

        label_transmission_type = ttk.Label(edit_car_window, text="Тип коробки:")
        label_transmission_type.pack()

        transmission_type_entry = ttk.Entry(edit_car_window)
        transmission_type_entry.insert(5, car_data[6])
        transmission_type_entry.pack()

        btn_save = ttk.Button(edit_car_window, text="Сохранить",
                              command=lambda: self.save_edited_car(edit_car_window, car_id, brand_entry.get(),
                                                                   color_entry.get(), year_entry.get(),
                                                                   engine_volume_entry.get(), horsepower_entry.get(),
                                                                   transmission_type_entry.get()))
        btn_save.pack()

    def save_edited_car(self, edit_car_window, car_id, brand, color, year, engine_volume, horsepower,
                        transmission_type):
        self.database.edit_car(car_id, brand, color, year, engine_volume, horsepower, transmission_type)
        edit_car_window.destroy()
        self.refresh_cars_table()

    def refresh_cars_table(self):
        self.cars = self.database.get_cars()

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

    def delete_client(self):
        selected_item = self.tree_clients.selection()

        if not selected_item:
            messagebox.showwarning("Предупреждение", "Выберите клиента для удаления.")
            return

        client_id = self.tree_clients.item(selected_item, "values")[0]
        self.database.delete_client(client_id)
        self.refresh_clients_table()

    def edit_client(self):
        selected_item = self.tree_clients.selection()

        if not selected_item:
            messagebox.showwarning("Предупреждение", "Выберите клиента для редактирования.")
            return

        client_id = self.tree_clients.item(selected_item, "values")[0]
        client_data = self.database.get_client(client_id)

        edit_client_window = tk.Toplevel(self.root)
        edit_client_window.title("Редактировать клиента")

        label_full_name = ttk.Label(edit_client_window, text="ФИО:")
        label_full_name.pack()

        full_name_entry = ttk.Entry(edit_client_window)
        full_name_entry.insert(0, client_data[1])
        full_name_entry.pack()

        label_birth_year = ttk.Label(edit_client_window, text="Год рождения:")
        label_birth_year.pack()

        birth_year_entry = ttk.Entry(edit_client_window)
        birth_year_entry.insert(1, client_data[2])
        birth_year_entry.pack()

        label_gender = ttk.Label(edit_client_window, text="Пол:")
        label_gender.pack()

        gender_entry = ttk.Entry(edit_client_window)
        gender_entry.insert(2, client_data[3])
        gender_entry.pack()

        label_registration_date = ttk.Label(edit_client_window, text="Дата регистрации:")
        label_registration_date.pack()

        registration_date_entry = ttk.Entry(edit_client_window)
        registration_date_entry.insert(3, client_data[4])
        registration_date_entry.pack()

        btn_save = ttk.Button(edit_client_window, text="Сохранить",
                              command=lambda: self.save_edited_client(edit_client_window, client_id, full_name_entry.get(),
                                                                      birth_year_entry.get(), gender_entry.get(),
                                                                      registration_date_entry.get()))
        btn_save.pack()

    def save_edited_client(self, edit_client_window, client_id, full_name, birth_year, gender, registration_date):
        self.database.edit_client(client_id, full_name, birth_year, gender, registration_date)
        edit_client_window.destroy()
        self.refresh_clients_table()

    def refresh_clients_table(self):
        self.clients = self.database.get_clients()

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
        label_car = ttk.Label(add_application_window, text="Автомобиль:")
        label_car.pack()

        combo_car = ttk.Combobox(add_application_window, values=[car[1] for car in self.cars], state="readonly")
        combo_car.pack()

        label_client = ttk.Label(add_application_window, text="Клиент:")
        label_client.pack()

        combo_client = ttk.Combobox(add_application_window, values=[client[1] for client in self.clients],
                                    state="readonly")
        combo_client.pack()

        label_viewing_date = ttk.Label(add_application_window, text="Дата просмотра:")
        label_viewing_date.pack()

        viewing_date_entry = ttk.Entry(add_application_window)
        viewing_date_entry.pack()

        btn_add = ttk.Button(add_application_window, text="Добавить", command=lambda: self.add_application(add_application_window, self.get_car_id_by_name(combo_car.get()), self.get_client_id_by_name(combo_client.get()), viewing_date_entry.get()))
        btn_add.pack()

    def get_car_id_by_name(self, car_name):
        for car in self.cars:
            if car[1] == car_name:
                return car[0]

    def get_client_id_by_name(self, client_name):
        for client in self.clients:
            if client[1] == client_name:
                return client[0]

    def add_application(self, add_application_window, car_id, client_id, viewing_date):
        self.database.add_application(car_id, client_id, viewing_date)
        add_application_window.destroy()
        # Обновляем отображение таблицы с заявками на просмотр
        self.refresh_applications_table()

    def delete_application(self):
        selected_item = self.tree_applications.selection()

        if not selected_item:
            messagebox.showwarning("Предупреждение", "Выберите заявку на просмотр для удаления.")
            return

        application_id = self.tree_applications.item(selected_item, "values")[0]
        self.database.delete_application(application_id)
        self.refresh_applications_table()

    def edit_application(self):
        selected_item = self.tree_applications.selection()

        if not selected_item:
            messagebox.showwarning("Предупреждение", "Выберите заявку для редактирования.")
            return

        application_id = self.tree_applications.item(selected_item, "values")[0]
        application_data = self.database.get_application(application_id)

        edit_application_window = tk.Toplevel(self.root)
        edit_application_window.title("Редактировать заявку")

        label_car = ttk.Label(edit_application_window, text="Автомобиль:")
        label_car.pack()

        car_values = [car[1] for car in self.cars]
        combo_car = ttk.Combobox(edit_application_window, values=car_values, state="readonly")
        combo_car.pack()
        combo_car.current(self.get_car_index_by_id(car_values, application_data[1]))

        label_client = ttk.Label(edit_application_window, text="Клиент:")
        label_client.pack()

        client_values = [client[1] for client in self.clients]
        combo_client = ttk.Combobox(edit_application_window, values=client_values,
                                    state="readonly")
        combo_client.pack()
        combo_client.current(self.get_client_index_by_id(client_values, application_data[2]))

        label_viewing_date = ttk.Label(edit_application_window, text="Дата просмотра:")
        label_viewing_date.pack()

        viewing_date_entry = ttk.Entry(edit_application_window)
        viewing_date_entry.insert(2, application_data[3])
        viewing_date_entry.pack()

        btn_save = ttk.Button(edit_application_window, text="Сохранить",
                              command=lambda: self.save_edited_application(edit_application_window, application_id, self.get_car_id_by_name(combo_car.get()), self.get_client_id_by_name(combo_client.get()), viewing_date_entry.get()))
        btn_save.pack()

    def get_car_index_by_id(self, car_values, car_id):
        for car in car_values:
            if car == self.database.get_car_name_by_id(car_id):
                return car_values.index(car)

    def get_client_index_by_id(self, client_values, client_id):
        for client in client_values:
            if client == self.database.get_client_name_by_id(client_id):
                return client_values.index(client)

    def save_edited_application(self, edit_application_window, application_id, car_id, client_id, viewing_date):
        self.database.edit_application(application_id, car_id, client_id, viewing_date)
        edit_application_window.destroy()
        self.refresh_applications_table()

    def refresh_applications_table(self):
        # Очищаем таблицу перед обновлением
        for row in self.tree_applications.get_children():
            self.tree_applications.delete(row)

        # Получаем данные из базы данных и добавляем их в таблицу
        applications = self.database.get_applications()
        for application in applications:
            self.tree_applications.insert("", "end", values=application)
