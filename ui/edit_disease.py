from utils import validate_date, get_date_from_calendar
from patient_manager import edit_disease
from tkinter import ttk, messagebox
import tkinter as tk


class EditDiseaseRecordWindow(tk.Toplevel):
    def __init__(self, parent, patient, diseases, patient_index, disease_index, update_callback, save_callback):
        super().__init__(parent)
        self.parent = parent
        self.patient = patient
        self.diseases = diseases
        self.patient_index = patient_index
        self.disease_index = disease_index
        self.update_callback = update_callback
        self.save_callback = save_callback
        self.title("Редактировать болезнь")
        self.create_widgets()

    def create_widgets(self):
        initial_disease = self.patient["diseases"][self.disease_index]
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('TLabel', font=('Arial', 12), padding=5)
        style.configure('TButton', padding=6, font=('Arial', 12))
        style.configure('TEntry', padding=5)
        style.configure('TCombobox', padding=5)
        window_width = 600
        window_height = 350
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        main_frame = ttk.Frame(self, padding=10)
        main_frame.pack(expand=True, fill="both")
        disease_name_label = ttk.Label(main_frame, text="Название болезни:")
        disease_name_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.disease_name_var = tk.StringVar(self)
        self.disease_name_combobox = ttk.Combobox(main_frame, textvariable=self.disease_name_var,
                                                  values=[d["name"] for d in self.diseases])
        self.disease_name_combobox.current([d["name"] for d in self.diseases].index(initial_disease["disease_name"]))
        self.disease_name_combobox.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        start_date_label = ttk.Label(main_frame, text="Дата начала:")
        start_date_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.start_date_entry = ttk.Entry(main_frame)
        self.start_date_entry.insert(0, initial_disease["start_date"])
        self.start_date_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        recovery_date_label = ttk.Label(main_frame, text="Дата выздоровления:")
        recovery_date_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.recovery_date_entry = ttk.Entry(main_frame)
        self.recovery_date_entry.insert(0, initial_disease["recovery_date"])
        self.recovery_date_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        comment_label = ttk.Label(main_frame, text="Комментарий доктора:")
        comment_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.comment_entry = ttk.Entry(main_frame)  # main_frame
        self.comment_entry.insert(0, initial_disease["doctor_comment"])
        self.comment_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
        self.start_date_entry.bind("<Button-1>", lambda event: self.open_calendar(self.start_date_entry))
        self.recovery_date_entry.bind("<Button-1>", lambda event: self.open_calendar(self.recovery_date_entry))
        save_button = ttk.Button(main_frame, text="Сохранить", command=self.save_changes)
        save_button.grid(row=4, column=0, columnspan=2, pady=10)
        main_frame.columnconfigure(1, weight=1)

    def open_calendar(self, entry):
        """Открывает окно календаря и устанавливает выбранную дату в поле ввода."""
        date = get_date_from_calendar(self)
        if date:
            entry.delete(0, tk.END)
            entry.insert(0, date)

    def save_changes(self):
        """Сохранение изменений."""
        disease_name = self.disease_name_var.get()
        start_date = self.start_date_entry.get()
        recovery_date = self.recovery_date_entry.get()
        comment = self.comment_entry.get()
        if not disease_name:
            messagebox.showwarning("Ошибка валидации", "Выберите болезнь из списка")
            return
        if not validate_date(start_date):
            messagebox.showwarning("Ошибка валидации",
                                   "Неверный формат даты начала болезни. Используйте формат ДД.MM.ГГГГ.")
            return
        if recovery_date and not validate_date(recovery_date):  # проверка только если дата выздоровления указана
            messagebox.showwarning("Ошибка валидации",
                                   "Неверный формат даты выздоровления. Используйте формат ДД.ММ.ГГГГ.")
            return
        edit_disease(self.parent.parent.patients, self.patient_index, self.disease_index, disease_name, start_date,
                     comment, recovery_date)
        self.update_callback()
        self.save_callback(self.parent.parent.patients, self.parent.parent.diseases)
        self.destroy()
