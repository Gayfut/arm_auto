class Entity:
    def __init__(self, db, title, fields):
        self.title = title
        self.fields = fields  # {имя_поля: тип_поля}

        self.database = db # Менеджер базы данных

        self.database.add_new_table(self.title, self.fields)

    def add(self, data):
        # Действия при добавлении новой сущности
        # (Получение данных из полей ввода, взаимодействие с БД)
        # ...

        self.database.add_new_element(self.title, data)

    def edit(self, element_id, data):
        # Действия при редактировании сущности
        # (Получение данных из полей ввода, взаимодействие с БД)
        # ...

        self.database.edit_element(self.title, element_id, data)

    def delete(self, element_id):
        # Действия при удалении сущности
        # (Получение данных из выбранной строки, взаимодействие с БД)
        # ...

        self.database.delete_element(self.title, element_id)

    def get_all_elements(self):
        # Возвращает все элементы из базы

        return self.database.get_elements(self.title)

    def get_element_data(self, element_id):
        # Возвращает все данные об элементе из базы

        return self.database.get_element(self.title, element_id)

    def delete_db(self):
        # Удаление всей таблицы сушности

        self.database.delete_table(self.title)
