import tkinter as tk

from db import Database
from login_window import LoginWindow
from main_window import MainWindow


def main():
    db = Database()

    root = tk.Tk()
    app_icon = tk.PhotoImage(file='src/icon.png')
    root.iconphoto(False, app_icon)

    def on_successful_login(user):
        main_window = MainWindow(tk.Toplevel(root), db, user)  # Создаем новое окно
        root.withdraw()  # Скрываем окно авторизации

    login_window = LoginWindow(root, db, on_successful_login)

    root.bind("<Escape>", lambda q: exit())
    root.mainloop()

    db.close_connection()


if __name__ == "__main__":
    main()
