import tkinter as tk
from tkinter import ttk


class Tab:
    def __init__(self, notebook, title, entity_class):
        self.frame = ttk.Frame(notebook)

        self.entity_class = entity_class  # Класс сущности (Клиенты, Автомобили)
        self.entity = None  # Экземпляр сущности

        # Создание первичного интерфейса
        self.create_firstly_ui()

        # Подключение функциональности
        self.connect_events()

    def create_firstly_ui(self):
        # Таблица для отображения данных
        self.data_grid = ttk.Treeview(self.frame, columns=self.__get_fields_names(), show="headings")
        self.selected_row = None  # Выбранная строка в таблице

        # Основные кнопки
        self.btn_add_entity = ttk.Button(self.frame, text="Добавить", command=None)
        self.btn_add_entity.pack(side="left")

        self.btn_delete_entity = ttk.Button(self.frame, text="Удалить", command=None)
        self.btn_delete_entity.pack(side="right")

        self.btn_edit_entity = ttk.Button(self.frame, text="Редактировать", command=None)
        self.btn_edit_entity.pack(side="left")

    def create_widgets(self):
        # Создание элементов управления на вкладке
        # (Заголовки, поля ввода, кнопки)
        # ...

        self.entity_window = tk.Toplevel(self.frame.master)

        for field_name, field_type in self.entity.fields.items():
            label = ttk.Label(self.frame, text=field_name)
            entry = ttk.Entry(self.frame) if field_type == "string" else ...  # Определить виджеты для других типов
            # ...

    def connect_events(self):
        # Связывание действий с элементами управления
        # (Обработчики кнопок "Добавить", "Редактировать", "Удалить")
        # ...

        pass

    def update_data_grid(self):
        # Обновление данных в таблице
        # ...

        pass

    def get_selected_data(self):
        # Получение данных из выбранной строки
        # ...

        pass

    def clear_selected(self):
        # Очистка полей ввода и выбранной строки
        # ...

        pass

    def __get_fields_names(self):
        fields_names = []

        for field_name, field_type in self.entity.fields.items():
            fields_names.append(field_name)

        return tuple(fields_names)
