from report_generator import generate_excel_report, save_report_to_excel
from ui.patient_list import PatientListWindow
from ui.add_disease import AddDiseaseWindow
from ui.add_patient import AddPatientWindow
from tkinter import ttk, messagebox
from tkinter import scrolledtext
import tkinter as tk


class MainWindow(
    tk.Toplevel):
    def __init__(self, parent, patients, diseases, save_callback):
        super().__init__(parent)
        self.parent = parent
        self.patients = patients
        self.diseases = diseases
        self.save_callback = save_callback
        self.title("Картотека пациентов")
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('TButton', padding=6, font=('Arial', 12))
        style.configure('TLabelFrame', padding=10, font=('Arial', 14, 'bold'))
        style.configure('TLabelFrame.Label', font=('Arial', 12))
        window_width = 1300
        window_height = 700
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.create_widgets()

    def create_widgets(self):
        buttons_frame = ttk.Frame(self)
        buttons_frame.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        add_patient_button = ttk.Button(buttons_frame, text="Добавить пациента", command=self.open_add_patient_window)
        add_patient_button.grid(row=0, column=0, padx=(0, 5), pady=5)
        add_disease_button = ttk.Button(buttons_frame, text="Добавить вид болезни",
                                        command=self.open_add_disease_window)
        add_disease_button.grid(row=0, column=1, padx=(5, 5), pady=5)
        self.patient_list_frame = ttk.LabelFrame(self, text="Текущие пациенты")
        self.patient_list_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.update_patient_list()
        report_button = ttk.Button(self, text="Сформировать отчёт", command=self.generate_and_display_report)
        report_button.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

    def open_add_patient_window(self):
        """Открытие окна добавления пациента."""
        AddPatientWindow(self, self.patients, self.update_patient_list)

    def update_patient_list(self):
        """Обновление списка пациентов на главном экране."""
        for widget in self.patient_list_frame.winfo_children():
            widget.destroy()
        PatientListWindow(self.patient_list_frame, self.patients, self.diseases, self.update_patient_list,
                          self.save_callback)

    def open_add_disease_window(self):
        """Открытие окна добавления болезни."""
        AddDiseaseWindow(self, self.diseases, self.update_patient_list)

    def generate_and_display_report(self):
        report_workbook = generate_excel_report(self.patients)
        save_report_to_excel(report_workbook)

    def destroy(self):
        self.parent.deiconify()
        self.save_callback(self.patients, self.diseases)
        super().destroy()
