from ui.disease_history import DiseaseHistoryWindow
from tkinter import ttk, messagebox
import tkinter as tk


class PatientListWindow(ttk.Frame):
    def __init__(self, parent, patients, diseases, update_patient_list_callback, save_callback):
        super().__init__(parent)
        self.parent = parent
        self.patients = patients
        self.diseases = diseases
        self.update_patient_list_callback = update_patient_list_callback
        self.save_callback = save_callback
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('TButton', padding=6, font=('Arial', 12))
        style.configure("Treeview.Heading", font=('Arial', 12, 'bold'))
        style.configure("Treeview", rowheight=25, font=('Arial', 12))
        self.create_widgets()

    def create_widgets(self):
        columns = ("name", "birth_date", "phone", "address")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        self.tree.heading("name", text="ФИО")
        self.tree.heading("birth_date", text="Дата рождения")
        self.tree.heading("phone", text="Телефон")
        self.tree.heading("address", text="Адрес")
        for patient in self.patients:
            values = (patient["name"], patient["birth_date"], patient["phone"], patient["address"])
            self.tree.insert("", tk.END, values=values)
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)
        delete_button = ttk.Button(self, text="Удалить пациента", command=self.delete_patient)
        delete_button.grid(row=1, column=0, pady=(5, 0), sticky="w")
        disease_history_button = ttk.Button(self, text="История болезней", command=self.open_disease_history_window)
        disease_history_button.grid(row=2, column=0, sticky="w")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.pack(fill="both", expand=True)

    def delete_patient(self):
        """Удаление пациента из списка."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Предупреждение", "Выберите пациента для удаления.")
            return
        try:
            patient_index = self.tree.index(selected_item[0])
            del self.patients[patient_index]
            self.tree.delete(selected_item)
            self.update_patient_list_callback()
        except IndexError:
            messagebox.showwarning("Предупреждение", "Выберите пациента для удаления.")

    def open_disease_history_window(self):
        """Открывает окно истории болезней для выбранного пациента."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Предупреждение", "Выберите пациента для просмотра истории болезней.")
            return
        try:
            patient_index = self.tree.index(selected_item[0])
            patient = self.patients[patient_index]
            DiseaseHistoryWindow(self, patient, self.diseases, patient_index, self.update_patient_list_callback,
                                 self.save_callback)
        except IndexError:
            messagebox.showwarning("Предупреждение", "Выберите пациента для просмотра истории болезней.")
