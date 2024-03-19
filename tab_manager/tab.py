import tkinter as tk
from tkinter import ttk, BOTH, messagebox


class Tab:
    def __init__(self, notebook, entity):
        self.entity = entity  # Класс сущности (Клиенты, Автомобили)

        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text=self.entity.title)

        # Создание первичного интерфейса
        self.create_firstly_ui()
        self.update_data_grid()

        # Подключение функциональности
        self.connect_events()

    def create_firstly_ui(self):
        # Таблица для отображения данных
        field_names = self.__get_fields_names()

        self.data_grid = ttk.Treeview(self.frame, columns=field_names, show="headings")
        for field_name in field_names:
            self.data_grid.heading(field_name, text=field_name)
        self.data_grid.pack(fill=BOTH, expand=True)

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
            entry = ttk.Entry(self.frame) if field_type == "STRING" else ...  # Определить виджеты для других типов
            # ...

    def connect_events(self):
        # Связывание действий с элементами управления
        # (Обработчики кнопок "Добавить", "Редактировать", "Удалить")
        # ...

        self.btn_delete_entity.config(command=self.__delete_handler)

    def update_data_grid(self):
        # Обновление данных в таблице
        # ...

        # Очищаем таблицу перед обновлением
        for row in self.data_grid.get_children():
            self.data_grid.delete(row)

        # Получаем данные из базы данных и добавляем их в таблицу
        elements = self.entity.get_all_elements()
        for element in elements:
            self.data_grid.insert("", "end", values=element)

    def get_selected_data(self):
        # Получение данных из выбранной строки
        # ...

        pass

    def clear_selected(self):
        # Очистка полей ввода и выбранной строки
        # ...

        pass

    def __get_fields_names(self):
        fields_names = ['id']

        for field_name, field_type in self.entity.fields.items():
            fields_names.append(field_name)

        return tuple(fields_names)

    def __delete_handler(self):
        selected_item = self.data_grid.selection()

        if not selected_item:
            messagebox.showwarning("Предупреждение", "Выберите элемент для удаления.")
            return

        element_id = self.data_grid.item(selected_item, "values")[0]

        self.entity.delete(element_id)
        self.update_data_grid()
