from utils import validate_name, validate_date, validate_phone, get_date_from_calendar, load_and_resize_image
from tkinter import ttk, messagebox
from tkinter import filedialog
import tkinter as tk


class AddPatientWindow(tk.Toplevel):
    def __init__(self, parent, patients, update_callback):
        super().__init__(parent)
        self.parent = parent
        self.patients = patients
        self.update_callback = update_callback
        self.title("Добавить пациента")
        self.photo = None
        self.filepath = ""
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('TLabel', font=('Arial', 12), padding=5)
        style.configure('TButton', padding=6, font=('Arial', 12))
        style.configure('TEntry', padding=5)
        window_width = 600
        window_height = 400
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self)
        main_frame.pack(expand=True, fill="both", padx=10, pady=10)
        name_label = ttk.Label(main_frame, text="ФИО:")
        name_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.name_entry = ttk.Entry(main_frame)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        birth_date_label = ttk.Label(main_frame, text="Дата рождения:")
        birth_date_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.birth_date_entry = ttk.Entry(main_frame)
        self.birth_date_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.birth_date_entry.bind("<Button-1>", lambda event: self.open_calendar(self.birth_date_entry))
        phone_label = ttk.Label(main_frame, text="Номер телефона:")
        phone_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.phone_entry = ttk.Entry(main_frame)
        self.phone_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        address_label = ttk.Label(main_frame, text="Адрес:")
        address_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.address_entry = ttk.Entry(main_frame)
        self.address_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
        photo_label = ttk.Label(main_frame, text="Фотография:")
        photo_label.grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.photo_button_frame = ttk.Frame(main_frame)
        self.photo_button_frame.grid(row=4, column=1, sticky="ew")
        self.photo_button = ttk.Button(self.photo_button_frame, text="Выбрать фото", command=self.choose_photo)
        self.photo_button.pack(side="left", padx=(0, 5))
        self.photo_image_label = ttk.Label(self.photo_button_frame)
        self.photo_image_label.pack(side="left")
        add_button = ttk.Button(main_frame, text="Добавить", command=self.add_patient)
        add_button.grid(row=5, column=0, columnspan=2, pady=10)
        self.birth_date_entry.bind("<Button-1>", lambda event: self.open_calendar(
            self.birth_date_entry))
        main_frame.columnconfigure(1, weight=1)

    def open_calendar(self, entry):
        date = get_date_from_calendar(self)
        if date:
            entry.delete(0, tk.END)
            entry.insert(0, date)

    def choose_photo(self):
        """Выбор фотографии пациента."""
        self.filepath = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif *.bmp")]
        )
        if self.filepath:
            self.photo = load_and_resize_image(self.filepath)
            if self.photo:
                self.photo_image_label.config(image=self.photo)

    def add_patient(self):
        """Добавление пациента в список."""
        name = self.name_entry.get()
        birth_date = self.birth_date_entry.get()
        phone = self.phone_entry.get()
        address = self.address_entry.get()
        if not validate_name(name):
            messagebox.showwarning("Ошибка валидации", "ФИО должно содержать только буквы и пробелы.")
            return
        if not validate_date(birth_date):
            messagebox.showwarning("Ошибка валидации", "Неверный формат даты. Используйте формат ДД.ММ.ГГГГ.")
            return
        if not validate_phone(phone):
            messagebox.showwarning("Ошибка валидации", "Номер телефона должен содержать только цифры.")
            return
        new_patient = {
            "photo": "" if self.photo is None else self.filepath,
            "name": name,
            "birth_date": birth_date,
            "phone": phone,
            "address": address,
            "diseases": []
        }
        self.patients.append(new_patient)
        self.update_callback()
        self.destroy()
