from tkinter import messagebox
import json


def load_diseases(filename="data/diseases.json"):
    """Загрузка списка болезней из JSON файла."""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        messagebox.showerror("Ошибка", "Ошибка загрузки списка болезней. Проверьте корректность JSON файла.")
        return []


def save_diseases(diseases, filename="data/diseases.json"):
    """Сохранение списка болезней в JSON файл."""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(diseases, f, ensure_ascii=False, indent=4)
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка сохранения списка болезней: {e}")


def add_disease(diseases, name):
    """Добавление нового вида болезни."""
    if any(d["name"] == name for d in diseases):
        messagebox.showwarning("Предупреждение", "Болезнь с таким названием уже существует.")
        return
    diseases.append({"name": name})


def edit_disease_name(diseases, disease_index, new_name):
    try:
        diseases[disease_index]["name"] = new_name
    except IndexError:
        messagebox.showerror("Error", "Invalid disease index")


def delete_disease(diseases, disease_index):
    """Удаление вида болезни."""
    try:
        del diseases[disease_index]
    except IndexError:
        messagebox.showerror("Ошибка", "Неверный индекс болезни.")
