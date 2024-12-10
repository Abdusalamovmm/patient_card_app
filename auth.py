from tkinter import messagebox


def authenticate_user(username, password, on_success):
    """Аутентификация пользователя."""
    default_username = "doctor"
    default_password = "dsu_it"
    if username == default_username and password == default_password:
        on_success()
    else:
        messagebox.showerror("Ошибка", "Неверное имя пользователя или пароль.")
