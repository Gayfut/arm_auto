from tkinter import ttk
from tab import Tab


class TabManager:
    def __init__(self, parent):
        self.parent = parent
        self.notebook = ttk.Notebook(parent)
        self.tabs = {}

    def add_tab(self, title, entity_class):
        tab = Tab(self.notebook, title, entity_class)
        self.tabs[title] = tab
        self.notebook.add(tab.frame, text=title)

    def remove_tab(self, title):
        if title in self.tabs:
            self.notebook.forget(self.tabs[title].frame)
            del self.tabs[title]

    def select_tab(self, title):
        if title in self.tabs:
            self.notebook.select(self.tabs[title].frame)
