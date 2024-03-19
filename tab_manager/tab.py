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

    def create_widgets(self, entity_window, window_type):
        # Создание элементов управления на вкладке
        # (Заголовки, поля ввода, кнопки)
        # ...

        if window_type == 'edit':
            selected_item = self.data_grid.selection()

            if not selected_item:
                messagebox.showwarning("Предупреждение", "Выберите элемент для редактирования.")
                return

            element_id = self.data_grid.item(selected_item, "values")[0]
            element_data = self.entity.get_element_data(element_id)
            element_cur = 1
            entry_cur = 0

        widgets = []
        for field_name, field_type in self.entity.fields.items():
            label = ttk.Label(entity_window, text=field_name)
            label.pack()

            if field_type.find('STRING') != -1 or field_type.find('INTEGER') != -1:
                entry = ttk.Entry(entity_window)

                if window_type == 'edit':
                    entry.insert(entry_cur, element_data[element_cur])
                    entry_cur += 1
                    element_cur += 1

                entry.pack()
            else:
                pass # Определить виджеты для других типов

            widgets.append(entry)

        if window_type == 'add':
            btn_add = ttk.Button(entity_window, text="Добавить", command=lambda: self.__add_save_handler(entity_window, widgets, window_type))
            btn_add.pack()
        elif window_type == 'edit':
            btn_save = ttk.Button(entity_window, text="Сохранить", command=lambda: self.__add_save_handler(entity_window, widgets, window_type, element_id))
            btn_save.pack()

    def connect_events(self):
        # Связывание действий с элементами управления
        # (Обработчики кнопок "Добавить", "Редактировать", "Удалить")
        # ...

        self.btn_add_entity.config(command=lambda: self.__window_handler('add'))
        self.btn_edit_entity.config(command=lambda: self.__window_handler('edit'))
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

    def __window_handler(self, window_type):
        entity_window = tk.Toplevel(self.frame.master)
        if window_type == 'add':
            entity_window.title("Добавить")
        elif window_type == 'edit':
            entity_window.title("Редактировать")

        self.create_widgets(entity_window, window_type)

    def __add_save_handler(self, entity_window, widgets, window_type, element_id=None):
        data = []
        for entry in widgets:
            data.append(entry.get())

        if window_type == 'add':
            self.entity.add(data)
        elif window_type == 'edit':
            self.entity.edit(element_id, data)

        entity_window.destroy()
        self.update_data_grid()

    def __delete_handler(self):
        selected_item = self.data_grid.selection()

        if not selected_item:
            messagebox.showwarning("Предупреждение", "Выберите элемент для удаления.")
            return

        element_id = self.data_grid.item(selected_item, "values")[0]

        self.entity.delete(element_id)
        self.update_data_grid()
