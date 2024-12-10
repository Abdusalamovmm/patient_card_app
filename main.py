from ui.main_window import MainWindow
from tkinter import messagebox, ttk
from auth import authenticate_user
import tkinter as tk
import json


def load_data():
    """Загрузка данных из JSON файлов."""
    try:
        with open("data/patients.json", "r", encoding="utf-8") as f:
            patients = json.load(f)
        with open("data/diseases.json", "r", encoding="utf-8") as f:
            diseases = json.load(f)
        return patients, diseases
    except FileNotFoundError:
        return [], []
    except json.JSONDecodeError:
        messagebox.showerror("Ошибка", "Ошибка загрузки данных из JSON файлов. Проверьте корректность данных.")
        return [], []


def save_data(patients, diseases):
    """Сохранение данных в JSON файлы."""
    try:
        with open("data/patients.json", "w", encoding="utf-8") as f:
            json.dump(patients, f, ensure_ascii=False, indent=4)  # ensure_ascii=False для корректной записи кириллицы
        with open("data/diseases.json", "w", encoding="utf-8") as f:
            json.dump(diseases, f, ensure_ascii=False, indent=4)
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка сохранения данных в JSON файлы: {e}")


def show_main_window(patients, diseases):
    """Отображение главного окна приложения."""
    root = tk.Tk()
    root.title("")
    root.geometry("250x10")
    main_window = MainWindow(root, patients, diseases, save_data)
    root.mainloop()


def main():
    patients, diseases = load_data()

    def on_login_success():
        """Действия после успешной авторизации."""
        login_window.destroy()  # Закрываем окно авторизации
        show_main_window(patients, diseases)  # Открываем главное окно

    login_window = tk.Tk()
    login_window.title("Авторизация")
    window_width = 500
    window_height = 200
    screen_width = login_window.winfo_screenwidth()
    screen_height = login_window.winfo_screenheight()
    x_coordinate = int((screen_width / 2) - (window_width / 2))
    y_coordinate = int((screen_height / 2) - (window_height / 2))
    login_window.geometry(
        "{}x{}+{}+{}".format(window_width, window_height, x_coordinate, y_coordinate))
    style = ttk.Style(login_window)
    style.theme_use('clam')
    style.configure('TLabel', font=('Arial', 12))
    style.configure('TButton', font=('Arial', 12), padding=5)
    style.configure('TEntry', padding=5)
    username_label = ttk.Label(login_window, text="Имя пользователя:")
    username_label.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")
    username_entry = ttk.Entry(login_window)
    username_entry.grid(row=0, column=1, padx=10, pady=(10, 5), sticky="ew")
    password_label = ttk.Label(login_window, text="Пароль:")
    password_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
    show_password = tk.IntVar(value=0)
    password_entry = ttk.Entry(login_window, show="*")
    password_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
    login_window.columnconfigure(1, weight=1)
    login_window.grid_rowconfigure(0, weight=1)
    login_window.grid_rowconfigure(1, weight=1)
    login_window.grid_rowconfigure(2, weight=1)
    login_window.grid_rowconfigure(3, weight=1)

    def toggle_password_visibility():
        if show_password.get():
            password_entry.config(show="")
        else:
            password_entry.config(show="*")

    show_password_checkbutton = ttk.Checkbutton(login_window, text="Показать пароль", variable=show_password,
                                                command=toggle_password_visibility)
    show_password_checkbutton.grid(row=2, column=1, padx=5, pady=(0, 5), sticky="e")
    login_button = ttk.Button(login_window, text="Войти",
                              command=lambda: authenticate_user(username_entry.get(), password_entry.get(),
                                                                on_login_success))
    login_button.grid(row=3, column=0, columnspan=2, pady=10)
    login_window.mainloop()


if __name__ == "__main__":
    main()
