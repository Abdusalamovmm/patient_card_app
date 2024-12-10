from disease_manager import add_disease as add_disease_type
from utils import validate_date, get_date_from_calendar
from patient_manager import add_disease
from tkinter import ttk, messagebox
import tkinter as tk


class AddDiseaseRecordWindow(tk.Toplevel):
    def __init__(self, parent, patient, diseases, patient_index, update_callback, save_callback):
        super().__init__(parent)
        self.parent = parent
        self.patient = patient
        self.diseases = diseases
        self.patient_index = patient_index
        self.update_callback = update_callback
        self.save_callback = save_callback
        self.title("Добавить болезнь")
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('TLabel', font=('Arial', 12), padding=5)
        style.configure('TButton', padding=6, font=('Arial', 12))
        style.configure('TEntry', padding=5)
        style.configure('TCombobox', padding=5)
        self.create_widgets()

    def create_widgets(self):
        disease_name_label = ttk.Label(self, text="Название болезни:")
        disease_name_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.disease_name_var = tk.StringVar(self)
        self.disease_name_combobox = ttk.Combobox(self, textvariable=self.disease_name_var,
                                                  values=[disease["name"] for disease in self.diseases])
        self.disease_name_combobox.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        start_date_label = ttk.Label(self, text="Дата начала:")
        start_date_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.start_date_entry = ttk.Entry(self)
        self.start_date_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        self.start_date_entry.bind("<Button-1>", lambda event: self.open_calendar(
            self.start_date_entry))
        comment_label = ttk.Label(self, text="Комментарий доктора:")
        comment_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.comment_entry = ttk.Entry(self)
        self.comment_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
        add_button = ttk.Button(self, text="Добавить", command=self.add_disease_record)
        add_button.grid(row=3, column=0, columnspan=2, pady=10)
        self.columnconfigure(1, weight=1)

    def open_calendar(self, entry):
        date = get_date_from_calendar(self)
        if date:
            entry.delete(0, tk.END)
            entry.insert(0, date)

    def add_disease_record(self):
        """Добавление записи о болезни."""
        disease_name = self.disease_name_var.get()
        start_date = self.start_date_entry.get()
        comment = self.comment_entry.get()
        if not disease_name:
            messagebox.showwarning("Ошибка валидации", "Выберите болезнь из списка.")
            return
        if not validate_date(start_date):
            messagebox.showwarning("Ошибка валидации", "Неверный формат даты. Используйте формат ДД.ММ.ГГГГ.")
            return
        add_disease(self.parent.parent.patients, self.patient_index, disease_name, start_date, comment)
        self.update_callback()
        self.save_callback(self.parent.parent.patients, self.parent.parent.diseases)
        self.destroy()


class AddDiseaseWindow(tk.Toplevel):
    def __init__(self, parent, diseases, update_callback):
        super().__init__(parent)
        self.parent = parent
        self.diseases = diseases
        self.update_callback = update_callback
        self.title("Добавить вид болезни")
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('TLabel', font=('Arial', 12), padding=5)
        style.configure('TButton', padding=6, font=('Arial', 12))
        style.configure('TEntry', padding=5)
        self.create_widgets()

    def create_widgets(self):
        name_label = ttk.Label(self, text="Название болезни:")
        name_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.name_entry = ttk.Entry(self)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        add_button = ttk.Button(self, text="Добавить", command=self.add_disease)
        add_button.grid(row=1, column=0, columnspan=2, pady=10)
        self.columnconfigure(1, weight=1)

    def add_disease(self):
        name = self.name_entry.get()
        if not name:
            messagebox.showwarning("Ошибка валидации", "Введите название болезни.")
            return
        add_disease_type(self.diseases, name)
        self.update_callback()
        self.destroy()
