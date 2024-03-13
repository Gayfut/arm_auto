class Entity:
    def __init__(self, tab):
        self.tab = tab  # Ссылка на вкладку, к которой принадлежит сущность
        self.fields = {}  # {имя_поля: тип_поля}

    def add(self):
        # Действия при добавлении новой сущности
        # (Получение данных из полей ввода, взаимодействие с БД)
        # ...

        data = {}
        for field_name in self.fields:
            data[field_name] = self.tab.frame.children[f"{field_name}_entry"].get()

    def edit(self):
        # Действия при редактировании сущности
        # (Получение данных из полей ввода, взаимодействие с БД)
        # ...

        data = {}
        for field_name in self.fields:
            data[field_name] = self.tab.frame.children[f"{field_name}_entry"].get()

    def delete(self):
        # Действия при удалении сущности
        # (Получение данных из выбранной строки, взаимодействие с БД)
        # ...

        pass
