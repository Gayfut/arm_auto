import os
from datetime import datetime

import tkinter as tk
from tkinter import ttk, messagebox, BOTH, Label, filedialog
from tkcalendar import DateEntry
from PIL import ImageTk, Image

#from tab_manager.tab_manager import TabManager
#from tab_manager.entity import Entity


class MainWindow:

    TRANSMISSION_TYPES = ['автомат', 'механика']
    GENDERS = ['М', 'Ж']
    COLORS = ['белый', 'синий', 'красный', 'желтый', 'зеленый', 'черный', 'серый']
    ALL_APPLICATIONS = False

    def __init__(self, root, database, user):
        self.root = root
        self.app_icon = tk.PhotoImage(file='src/icon.png')
        self.root.iconphoto(False, self.app_icon)
        self.root.title("Главная страница")

        self.root.protocol("WM_DELETE_WINDOW", self.close_event)

        self.database = database
        self.current_user = user

        self.cars = []
        self.clients = []

        self.car_image = ''

        # Определение стилей
        self.root.configure(bg='white')

        # Текущий пользователь
        self.label_current_user = ttk.Label(self.root, text=f"Пользователь: {self.database.get_username_by_id(self.current_user)}",
                                            background='white', font=('Arial', 10))
        self.label_current_user.pack(side="top", padx=10, pady=5)

        # Кнопка обновления списков
        self.btn_refresh_all = ttk.Button(self.root, text="Обновить",
                                       command=lambda: self.refresh_all_tables())
        self.btn_refresh_all.pack(side="top")

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

        if self.database.user_is_admin(self.current_user):
            # Вкладка "Пользователи"
            self.tab_users = ttk.Frame(self.notebook)
            self.notebook.add(self.tab_users, text="Пользователи")
            self.create_users_tab()

            self.refresh_users_table()

        self.notebook.pack(fill="both", expand=True)

        # Заполнение вкладок при открытии приложения
        self.refresh_cars_table()
        self.refresh_clients_table()
        self.refresh_applications_table()


        # Пример использования интерфейса
        # self.test = Entity(self.database, 'test', {'name': 'STRING'})

        #self.tab_manager = TabManager(self.notebook)
        #self.tab_manager.add_tab(self.test)

    def close_event(self):
        self.root.destroy()
        exit()

    def refresh_all_tables(self):
        self.refresh_cars_table()
        self.refresh_clients_table()
        self.refresh_applications_table()
        self.refresh_users_table()

    def create_cars_tab(self):
        self.tree_cars = ttk.Treeview(self.tab_cars, columns=("ID", "Brand", "Color", "Year", "Engine Volume", "Horsepower", "Transmission Type"), show="headings")
        self.tree_cars.heading("ID", text="id")
        self.tree_cars.heading("Brand", text="Марка, модель")
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

        self.btn_show_all = ttk.Button(self.tab_applications, text="Все",
                                       command=lambda: self.refresh_applications_table(True))
        self.btn_show_all.pack(side="right")

        btn_delete_application = ttk.Button(self.tab_applications, text="Удалить", command=self.delete_application)
        btn_delete_application.pack(side="right")

        btn_edit_application = ttk.Button(self.tab_applications, text="Редактировать", command=self.edit_application)
        btn_edit_application.pack(side="left")

        btn_mark_as_shown = ttk.Button(self.tab_applications, text="Отметить как показанную",
                                       command=self.mark_application_as_shown)
        btn_mark_as_shown.pack(side="left")

    def create_users_tab(self):
        self.tree_users = ttk.Treeview(self.tab_users, columns=("ID", "Username"), show="headings")
        self.tree_users.heading("ID", text="id")
        self.tree_users.heading("Username", text="Пользователь")

        self.tree_users.pack(fill=BOTH, expand=True)

        btn_add_user = ttk.Button(self.tab_users, text="Добавить", command=self.add_user_window)
        btn_add_user.pack(side="left")

        btn_delete_user = ttk.Button(self.tab_users, text="Удалить", command=self.delete_user)
        btn_delete_user.pack(side="right")

        btn_edit_user = ttk.Button(self.tab_users, text="Редактировать", command=self.edit_user)
        btn_edit_user.pack(side="left")

    def add_car_window(self):
        add_car_window = tk.Toplevel(self.root)
        add_car_window.iconphoto(False, self.app_icon)
        add_car_window.title("Добавить автомобиль")

        # Создаем и размещаем элементы интерфейса для добавления автомобиля
        label_brand = ttk.Label(add_car_window, text="Марка, модель:")
        label_brand.pack()

        brand_entry = ttk.Entry(add_car_window)
        brand_entry.pack()

        label_color = ttk.Label(add_car_window, text="Цвет:")
        label_color.pack()

        color_entry = ttk.Combobox(add_car_window, values=self.COLORS, state="readonly")
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

        transmission_type_entry = ttk.Combobox(add_car_window, values=self.TRANSMISSION_TYPES, state="readonly")
        transmission_type_entry.pack()

        btn_add = ttk.Button(add_car_window, text="Добавить", command=lambda: self.add_car(add_car_window, brand_entry.get(), color_entry.get(), year_entry.get(), engine_volume_entry.get(), horsepower_entry.get(), transmission_type_entry.get()))
        btn_add.pack()

        new_img_button = ttk.Button(add_car_window, text='Новое изображение',
                                    command=lambda: self.new_car_photo(add_car_window))
        new_img_button.pack()

    def new_car_photo(self, car_window):
        new_image_path = filedialog.askopenfilename(title='Изображение для авто')

        if new_image_path != '':
            self.car_image = self.convert_to_binary_data_car_img(new_image_path)

            widgets = car_window.winfo_children()
            for widget in widgets:
                if hasattr(widget, 'myId'):
                    if widget.myId == 'car_image':
                        widget.destroy()

            self.create_car_image(car_window)

    def convert_to_binary_data_car_img(self, filename):
        # Преобразование данных в двоичный формат
        with open(filename, 'rb') as file:
            blob_data = file.read()

        return blob_data

    def write_to_file_car_img(self):
        file_path = 'temp_img.jpg'

        # Преобразование двоичных данных в нужный формат
        with open(file_path, 'wb') as file:
            file.write(self.car_image)

        return file_path

    def delete_temp_img(self):
        temp_file = 'temp_img.jpg'

        if os.path.isfile(temp_file):
            os.remove(temp_file)

    def create_car_image(self, car_window):
        car_image_path = self.write_to_file_car_img()

        img = Image.open(car_image_path)
        img = img.resize((250, 250))
        img = ImageTk.PhotoImage(img)
        img_panel = Label(car_window, image=img)
        img_panel.image = img
        img_panel.myId = 'car_image'
        img_panel.pack()

        self.delete_temp_img()

    def add_car(self, add_car_window, brand, color, year, engine_volume, horsepower, transmission_type):
        self.database.add_car(brand, color, year, engine_volume, horsepower, transmission_type, self.car_image)
        add_car_window.destroy()
        # Обновляем отображение таблицы с автомобилями
        self.refresh_cars_table()

    def delete_car(self):
        selected_item = self.tree_cars.selection()

        if not selected_item:
            messagebox.showwarning("Предупреждение", "Выберите автомобиль для удаления.")
            return

        car_id = self.tree_cars.item(selected_item, "values")[0]

        if self.database.check_car(car_id):
            messagebox.showerror("Ошибка", "Данный автомобиль используется в заявке на просмотр!")
        else:
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
        edit_car_window.iconphoto(False, self.app_icon)
        edit_car_window.title("Редактировать автомобиль")

        label_brand = ttk.Label(edit_car_window, text="Марка, модель:")
        label_brand.pack()

        brand_entry = ttk.Entry(edit_car_window)
        brand_entry.insert(0, car_data[1])
        brand_entry.pack()

        label_color = ttk.Label(edit_car_window, text="Цвет:")
        label_color.pack()

        color_entry = ttk.Combobox(edit_car_window, values=self.COLORS, state="readonly")
        color_entry.current(self.COLORS.index(car_data[2]))
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

        transmission_type_entry = ttk.Combobox(edit_car_window, values=self.TRANSMISSION_TYPES, state="readonly")
        transmission_type_entry.current(self.TRANSMISSION_TYPES.index(car_data[6]))
        transmission_type_entry.pack()

        btn_save = ttk.Button(edit_car_window, text="Сохранить",
                              command=lambda: self.save_edited_car(edit_car_window, car_id, brand_entry.get(),
                                                                   color_entry.get(), year_entry.get(),
                                                                   engine_volume_entry.get(), horsepower_entry.get(),
                                                                   transmission_type_entry.get()))
        btn_save.pack()

        new_img_button = ttk.Button(edit_car_window, text='Новое изображение',
                                    command=lambda: self.new_car_photo(edit_car_window))
        new_img_button.pack()

        self.car_image = car_data[7]
        self.create_car_image(edit_car_window)

    def save_edited_car(self, edit_car_window, car_id, brand, color, year, engine_volume, horsepower,
                        transmission_type):
        self.database.edit_car(car_id, brand, color, year, engine_volume, horsepower, transmission_type, self.car_image)
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
        add_client_window.iconphoto(False, self.app_icon)
        add_client_window.title("Добавить клиента")

        # Создаем и размещаем элементы интерфейса для добавления клиента
        label_full_name = ttk.Label(add_client_window, text="ФИО:")
        label_full_name.pack()

        full_name_entry = ttk.Entry(add_client_window)
        full_name_entry.pack()

        label_birth_year = ttk.Label(add_client_window, text="Год рождения:")
        label_birth_year.pack()

        birth_year_entry = DateEntry(add_client_window, selectmode='day')
        birth_year_entry.pack()

        label_gender = ttk.Label(add_client_window, text="Пол:")
        label_gender.pack()

        gender_entry = ttk.Combobox(add_client_window, values=self.GENDERS, state="readonly")
        gender_entry.pack()

        label_registration_date = ttk.Label(add_client_window, text="Дата регистрации:")
        label_registration_date.pack()

        registration_date_entry = DateEntry(add_client_window, selectmode='day')
        registration_date_entry.pack()

        btn_add = ttk.Button(add_client_window, text="Добавить", command=lambda: self.add_client(add_client_window, full_name_entry.get(), birth_year_entry.get_date(), gender_entry.get(), registration_date_entry.get_date()))
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

        if self.database.check_client(client_id):
            messagebox.showerror("Ошибка", "Данный клиент используется в заявке на просмотр!")
        else:
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
        edit_client_window.iconphoto(False, self.app_icon)
        edit_client_window.title("Редактировать клиента")

        label_full_name = ttk.Label(edit_client_window, text="ФИО:")
        label_full_name.pack()

        full_name_entry = ttk.Entry(edit_client_window)
        full_name_entry.insert(0, client_data[1])
        full_name_entry.pack()

        label_birth_year = ttk.Label(edit_client_window, text="Год рождения:")
        label_birth_year.pack()

        birth_year_entry = DateEntry(edit_client_window, selectmode='day')
        birth_year_entry.set_date(datetime.strptime(client_data[2], '%Y-%m-%d'))
        birth_year_entry.pack()

        label_gender = ttk.Label(edit_client_window, text="Пол:")
        label_gender.pack()

        gender_entry = ttk.Combobox(edit_client_window, values=self.GENDERS, state="readonly")
        gender_entry.current(self.GENDERS.index(client_data[3]))
        gender_entry.pack()

        label_registration_date = ttk.Label(edit_client_window, text="Дата регистрации:")
        label_registration_date.pack()

        registration_date_entry = DateEntry(edit_client_window, selectmode='day')
        registration_date_entry.set_date(datetime.strptime(client_data[4], '%Y-%m-%d'))
        registration_date_entry.pack()

        btn_save = ttk.Button(edit_client_window, text="Сохранить",
                              command=lambda: self.save_edited_client(edit_client_window, client_id, full_name_entry.get(),
                                                                      birth_year_entry.get_date(), gender_entry.get(),
                                                                      registration_date_entry.get_date()))
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
        add_application_window.iconphoto(False, self.app_icon)
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

        viewing_date_entry = DateEntry(add_application_window, selectmode='day')
        viewing_date_entry.pack()

        btn_add = ttk.Button(add_application_window, text="Добавить", command=lambda: self.add_application(add_application_window, self.get_car_id_by_name(combo_car.get()), self.get_client_id_by_name(combo_client.get()), viewing_date_entry.get_date()))
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
        edit_application_window.iconphoto(False, self.app_icon)
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

        viewing_date_entry = DateEntry(edit_application_window, selectmode='day')
        viewing_date_entry.set_date(datetime.strptime(application_data[3], '%Y-%m-%d'))
        viewing_date_entry.pack()

        btn_save = ttk.Button(edit_application_window, text="Сохранить",
                              command=lambda: self.save_edited_application(edit_application_window, application_id, self.get_car_id_by_name(combo_car.get()), self.get_client_id_by_name(combo_client.get()), viewing_date_entry.get_date()))
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

    def refresh_applications_table(self, all_command=False):
        # Очищаем таблицу перед обновлением
        for row in self.tree_applications.get_children():
            self.tree_applications.delete(row)

        # Получаем данные из базы данных и добавляем их в таблицу
        if all_command:
            self.ALL_APPLICATIONS = not self.ALL_APPLICATIONS

            if self.ALL_APPLICATIONS:
                self.btn_show_all.config(text="Непоказанные")
            else:
                self.btn_show_all.config(text="Все")

            applications = self.database.get_applications(self.ALL_APPLICATIONS)
        else:
            applications = self.database.get_applications(self.ALL_APPLICATIONS)

        for application in applications:
            application = list(application)
            application[1] = self.database.get_car_name_by_id(application[1])
            application[2] = self.database.get_client_name_by_id(application[2])
            application = tuple(application)

            self.tree_applications.insert("", "end", values=application)

    def mark_application_as_shown(self):
        selected_item = self.tree_applications.selection()

        if not selected_item:
            messagebox.showwarning("Предупреждение", "Выберите заявку для отметки.")
            return

        application_id = self.tree_applications.item(selected_item, "values")[0]

        self.database.mark_application_as_shown(application_id)

        self.refresh_applications_table()

    def add_user_window(self):
        add_user_window = tk.Toplevel(self.root)
        add_user_window.iconphoto(False, self.app_icon)
        add_user_window.title("Добавить пользователя")

        # Создаем и размещаем элементы интерфейса для добавления пользователя
        label_username = ttk.Label(add_user_window, text="Логин:")
        label_username.pack()

        username_entry = ttk.Entry(add_user_window)
        username_entry.pack()

        label_password = ttk.Label(add_user_window, text="Пароль:")
        label_password.pack()

        password_entry = ttk.Entry(add_user_window)
        password_entry.pack()

        is_admin_var = tk.BooleanVar()
        is_admin = ttk.Checkbutton(add_user_window, text="Админ", variable=is_admin_var, onvalue=True, offvalue=False)
        is_admin.pack()

        btn_add = ttk.Button(add_user_window, text="Добавить", command=lambda: self.add_user(add_user_window, username_entry.get(), password_entry.get(), is_admin_var.get()))
        btn_add.pack()

    def add_user(self, add_user_window, username, password, is_admin):
        self.database.add_user(username, password, is_admin)
        add_user_window.destroy()
        # Обновляем отображение таблицы с клиентами
        self.refresh_users_table()

    def delete_user(self):
        selected_item = self.tree_users.selection()

        if not selected_item:
            messagebox.showwarning("Предупреждение", "Выберите пользователя для удаления.")
            return

        user_id = self.tree_users.item(selected_item, "values")[0]
        self.database.delete_user(user_id)
        self.refresh_users_table()

    def edit_user(self):
        selected_item = self.tree_users.selection()

        if not selected_item:
            messagebox.showwarning("Предупреждение", "Выберите клиента для редактирования.")
            return

        user_id = self.tree_users.item(selected_item, "values")[0]
        user_data = self.database.get_user(user_id)

        edit_user_window = tk.Toplevel(self.root)
        edit_user_window.iconphoto(False, self.app_icon)
        edit_user_window.title("Редактировать пользователя")

        label_username = ttk.Label(edit_user_window, text="Логин:")
        label_username.pack()

        username_entry = ttk.Entry(edit_user_window)
        username_entry.insert(0, user_data[1])
        username_entry.pack()

        label_password = ttk.Label(edit_user_window, text="Пароль:")
        label_password.pack()

        password_entry = ttk.Entry(edit_user_window)
        password_entry.insert(0, user_data[2])
        password_entry.pack()

        is_admin_var = tk.BooleanVar()
        is_admin_var.set(user_data[3])
        is_admin = ttk.Checkbutton(edit_user_window, text="Админ", variable=is_admin_var, onvalue=True, offvalue=False)
        is_admin.pack()

        btn_save = ttk.Button(edit_user_window, text="Сохранить",
                              command=lambda: self.save_edited_user(edit_user_window, user_id, username_entry.get(),
                                                                      password_entry.get(), is_admin_var.get()))
        btn_save.pack()

    def save_edited_user(self, edit_user_window, user_id, username, password, is_admin):
        self.database.edit_user(user_id, username, password, is_admin)
        edit_user_window.destroy()
        self.refresh_users_table()

    def refresh_users_table(self):
        self.clients = self.database.get_users(self.current_user)

        # Очищаем таблицу перед обновлением
        for row in self.tree_users.get_children():
            self.tree_users.delete(row)

        # Получаем данные из базы данных и добавляем их в таблицу
        users = self.database.get_users(self.current_user)
        for user in users:
            self.tree_users.insert("", "end", values=user)
