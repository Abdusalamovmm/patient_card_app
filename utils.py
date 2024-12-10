from tkcalendar import DateEntry
from tkinter import messagebox
from PIL import Image, ImageTk
import tkinter as tk
import json
import io


def load_data(filename):
    """Универсальная функция загрузки данных из JSON файла."""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        messagebox.showerror("Ошибка", f"Ошибка загрузки данных из {filename}. Проверьте корректность JSON файла.")
        return []


def save_data(data, filename):
    """Универсальная функция сохранения данных в JSON файл."""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка сохранения данных в {filename}: {e}")


def validate_name(name):
    """Валидация ФИО (только буквы и пробелы)."""
    if not name.replace(" ", "").isalpha():
        return False
    return True


def validate_date(date_str):
    """Валидация даты (формат ДД.MM.ГГГГ)."""
    try:
        parts = date_str.split(".")
        if len(parts) != 3 or not all(part.isdigit() for part in parts):
            return False
        day, month, year = map(int, parts)
        if not (1 <= month <= 12 and 1 <= day <= 31 and 1900 <= year <= 2100):
            return False
        return True
    except ValueError:
        return False


def validate_phone(phone):
    """Валидация номера телефона (только цифры, + и -)."""
    return all(char.isdigit() or char in "+-" for char in phone)


def get_date_from_calendar(parent):
    """Открывает календарь и возвращает выбранную дату в формате ДД.MM.ГГГГ."""

    def on_date_select():
        nonlocal selected_date
        selected_date = cal.get_date().strftime("%d.%m.%Y")
        top.destroy()

    selected_date = None
    top = tk.Toplevel(parent)
    cal = DateEntry(top, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='dd.mm.yyyy')
    cal.pack(padx=10, pady=10)
    ok_button = tk.Button(top, text="OK", command=on_date_select)
    ok_button.pack()
    top.wait_window(top)
    return selected_date


def load_and_resize_image(filepath):
    """Загружает изображение и масштабирует его до 256x256 пикселей."""
    if not filepath:
        return None
    try:
        image = Image.open(filepath)
        image = image.resize((64, 64), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        return photo
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка загрузки изображения: {e}")
        return None
