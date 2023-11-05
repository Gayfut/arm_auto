import tkinter as tk

from db import Database
from login_window import LoginWindow
from main_window import MainWindow


def main():
    db = Database()
    root = tk.Tk()

    def on_successful_login():
        main_window = MainWindow(tk.Toplevel(root), db)  # Создаем новое окно
        root.withdraw()  # Скрываем окно авторизации

    login_window = LoginWindow(root, db, on_successful_login)
    root.mainloop()
    db.close_connection()


if __name__ == "__main__":
    main()
