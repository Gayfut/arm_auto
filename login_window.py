import tkinter as tk
from tkinter import ttk, messagebox


class LoginWindow:
    def __init__(self, root, database, on_successful_login):
        self.root = root
        self.root.title("Логин")

        self.database = database
        self.on_successful_login = on_successful_login

        # Определение стилей
        self.root.configure(bg='white')

        self.create_widgets()

    def create_widgets(self):
        style = ttk.Style()
        style.configure('TButton', background='orange', font=('Arial', 12))
        style.configure('TEntry', font=('Arial', 12))

        self.label_username = tk.Label(self.root, text="Логин:", bg='white')
        self.label_username.pack()

        self.entry_username = ttk.Entry(self.root, style='TEntry')
        self.entry_username.pack()

        self.label_password = tk.Label(self.root, text="Пароль:", bg='white')
        self.label_password.pack()

        self.entry_password = ttk.Entry(self.root, show="*", style='TEntry')
        self.entry_password.pack()

        self.btn_login = ttk.Button(self.root, text="Войти", command=self.check_login, style='TButton')
        self.btn_login.pack()

    def check_login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        user = self.database.check_user_credentials(username, password)

        if user:
            messagebox.showinfo("Успешно", "Вход выполнен успешно!")
            self.on_successful_login(user[0])
        else:
            messagebox.showerror("Ошибка", "Неправильный логин или пароль")
