from tkinter import ttk
from .tab import Tab


class TabManager:
    def __init__(self, notebook):
        self.notebook = notebook
        self.tabs = {}

    def add_tab(self, entity_class):
        # Добавление новой вкладки
        tab = Tab(self.notebook, entity_class)
        self.tabs[entity_class.title] = tab

    def remove_tab(self, title):
        # Удаление вкладки
        if title in self.tabs:
            self.notebook.forget(self.tabs[title].frame)
            del self.tabs[title]

    def select_tab(self, title):
        # Выбор вкладки
        if title in self.tabs:
            self.notebook.select(self.tabs[title].frame)
