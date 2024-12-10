from patient_manager import delete_disease as delete_patient_disease
from ui.edit_disease import EditDiseaseRecordWindow
from ui.add_disease import AddDiseaseRecordWindow
from tkinter import ttk, messagebox
import tkinter as tk


class DiseaseHistoryWindow(tk.Toplevel):
    def __init__(self, parent, patient, diseases, patient_index, update_callback, save_callback):
        super().__init__(parent)
        self.parent = parent
        self.patient = patient
        self.diseases = diseases
        self.patient_index = patient_index
        self.update_callback = update_callback
        self.save_callback = save_callback
        self.title(f"История болезней - {patient['name']}")
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('TButton', padding=6, font=('Arial', 12))
        style.configure("Treeview.Heading", font=('Arial', 12, 'bold'))
        style.configure("Treeview", rowheight=25, font=('Arial', 12))
        window_width = 1300
        window_height = 500
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(expand=True, fill="both")
        columns = ("disease_name", "start_date", "recovery_date", "doctor_comment")
        self.tree = ttk.Treeview(main_frame, columns=columns, show="headings")
        self.tree.heading("disease_name", text="Название болезни")
        self.tree.heading("start_date", text="Дата начала")
        self.tree.heading("recovery_date", text="Дата выздоровления")
        self.tree.heading("doctor_comment", text="Комментарий")
        self.update_disease_list()
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(pady=(10, 0), anchor="w")
        add_button = ttk.Button(buttons_frame, text="Добавить болезнь", command=self.open_add_disease_window)
        add_button.grid(row=0, column=0, padx=5, pady=5)
        edit_button = ttk.Button(buttons_frame, text="Редактировать болезнь", command=self.open_edit_disease_window)
        edit_button.grid(row=1, column=0, padx=5, pady=5)
        delete_button = ttk.Button(buttons_frame, text="Удалить болезнь", command=self.delete_disease_record)
        delete_button.grid(row=2, column=0, padx=5, pady=5)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def update_disease_list(self):
        """Обновление списка болезней в Treeview."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        for disease in self.patient['diseases']:
            self.tree.insert("", tk.END, values=(
            disease["disease_name"], disease["start_date"], disease["recovery_date"], disease["doctor_comment"]))

    def open_add_disease_window(self):
        """Открытие окна для добавления записи о болезни."""
        AddDiseaseRecordWindow(self, self.patient, self.diseases, self.patient_index, self.update_disease_list,
                               self.save_callback)

    def open_edit_disease_window(self):
        """Открытие окна для редактирования записи о болезни."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Предупреждение", "Выберите запись для редактирования.")
            return
        try:
            disease_index = self.tree.index(selected_item[0])
            disease = self.patient["diseases"][disease_index]
            EditDiseaseRecordWindow(self, self.patient, self.diseases, self.patient_index, disease_index,
                                    self.update_disease_list, self.save_callback)
        except IndexError:
            messagebox.showerror("Ошибка", "Неверный индекс записи о болезни.")

    def delete_disease_record(self):
        """Удаление записи о болезни."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Предупреждение", "Выберите запись для удаления.")
            return
        try:
            disease_index = self.tree.index(selected_item[0])
            delete_patient_disease(self.parent.patients, self.patient_index, disease_index)
            self.update_disease_list()
        except IndexError:
            messagebox.showerror("Ошибка", "Неверный индекс записи о болезни.")
