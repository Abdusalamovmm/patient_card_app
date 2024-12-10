from tkinter import messagebox
import json


def load_patients(filename="data/patients.json"):
    """Загрузка данных пациентов из JSON файла."""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        messagebox.showerror("Ошибка", "Ошибка загрузки данных пациентов. Проверьте корректность JSON файла.")
        return []


def save_patients(patients, filename="data/patients.json"):
    """Сохранение данных пациентов в JSON файл."""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(patients, f, ensure_ascii=False, indent=4)
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка сохранения данных пациентов: {e}")


def add_patient(patients, photo, name, birth_date, phone, address):
    """Добавление нового пациента."""
    new_patient = {
        "photo": photo,
        "name": name,
        "birth_date": birth_date,
        "phone": phone,
        "address": address,
        "diseases": []
    }
    patients.append(new_patient)


def delete_patient(patients, patient_index):
    """Удаление пациента."""
    try:
        del patients[patient_index]
    except IndexError:
        messagebox.showerror("Ошибка", "Неверный индекс пациента.")


def get_patient_diseases(patients, patient_index):
    """Получение истории болезней пациента."""
    try:
        return patients[patient_index]["diseases"]
    except IndexError:
        messagebox.showerror("Ошибка", "Неверный индекс пациента.")
        return []


def add_disease(patients, patient_index, disease_name, start_date, doctor_comment):
    """Добавление записи о болезни в историю болезней пациента."""
    try:
        patients[patient_index]["diseases"].append({
            "disease_name": disease_name,
            "start_date": start_date,
            "doctor_comment": doctor_comment,
            "recovery_date": ""  # Поле для даты выздоровления.  Изначально пустое.
        })
    except IndexError:
        messagebox.showerror("Ошибка", "Неверный индекс пациента.")


def edit_disease(patients, patient_index, disease_index, disease_name, start_date, doctor_comment, recovery_date):
    """Редактирование записи о болезни."""
    try:
        patients[patient_index]["diseases"][disease_index] = {
            "disease_name": disease_name,
            "start_date": start_date,
            "doctor_comment": doctor_comment,
            "recovery_date": recovery_date
        }
    except IndexError:
        messagebox.showerror("Ошибка", "Неверный индекс пациента или болезни.")


def delete_disease(patients, patient_index, disease_index):
    """Удаление записи о болезни из истории болезней пациента."""
    try:
        del patients[patient_index]["diseases"][disease_index]
    except IndexError:
        messagebox.showerror("Ошибка", "Неверный индекс пациента или болезни.")
