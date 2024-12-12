import customtkinter as ctk
from PIL import Image
import pymysql
from tkinter import messagebox

# Настройки CustomTkinter
ctk.set_appearance_mode("dark")  # Темная/светлая тема
ctk.set_default_color_theme("blue")  # Тема (blue, dark-blue, green)

# Подключение к базе данных
connection = pymysql.connect(
    host="localhost",
    user="root",
    password="",
    database="fitnes"
)


class AdminApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Admin Interface - Fitness")
        self.geometry("800x600")

        # Настройки сетки для основного окна
        self.grid_columnconfigure(1, weight=1)  # Центральная область будет растягиваться
        self.grid_rowconfigure(0, weight=1)

        # Создание боковой панели
        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="ns")
        self.sidebar_frame.grid_rowconfigure(6, weight=1)  # Растягивание нижней части панели

        # Загрузка изображения
        logo_image = ctk.CTkImage(Image.open("Remove-bg.ai_1733168975879.png"), size=(150, 50))

        # Заголовок боковой панели с логотипом
        self.logo_label = ctk.CTkLabel(
        self.sidebar_frame,
        text=" ",  # Текст заголовка
        font=ctk.CTkFont(size=20, weight="bold"),
        image=logo_image,  # Установка изображения
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))


    
        # Кнопки боковой панели
        self.clients_button = ctk.CTkButton(self.sidebar_frame, text="Clients", command=self.show_clients_page)
        self.clients_button.grid(row=1, column=0, padx=20, pady=10)

        self.memberships_button = ctk.CTkButton(self.sidebar_frame, text="Memberships", command=self.show_memberships_page)
        self.memberships_button.grid(row=2, column=0, padx=20, pady=10)

        self.trainers_button = ctk.CTkButton(self.sidebar_frame, text="Trainers", command=self.show_trainers_page)
        self.trainers_button.grid(row=3, column=0, padx=20, pady=10)

        self.trainers_button = ctk.CTkButton(self.sidebar_frame, text="Activities", command=self.show_activities_page)
        self.trainers_button.grid(row=4, column=0, padx=20, pady=10)

        self.memberships_button = ctk.CTkButton(self.sidebar_frame, text="Activity Registration", command=self.show_activity_registration_page)
        self.memberships_button.grid(row=5, column=0, padx=20, pady=10)
        
        self.exit_button = ctk.CTkButton(self.sidebar_frame, text="Exit", fg_color="red", command=self.quit)
        self.exit_button.grid(row=6, column=0, padx=20, pady=50)

        # Центральная область для страниц
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        # Отображение страницы клиентов по умолчанию
        self.show_clients_page()

    def show_clients_page(self):
        # Очистка предыдущей страницы
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Поля ввода
        frame_input = ctk.CTkFrame(self.content_frame)
        frame_input.pack(pady=10)

        label_name = ctk.CTkLabel(frame_input, text="Client Name:")
        label_name.grid(row=0, column=0, padx=5, pady=5)
        self.entry_name = ctk.CTkEntry(frame_input, width=200)
        self.entry_name.grid(row=0, column=1, padx=5, pady=5)

        label_phone = ctk.CTkLabel(frame_input, text="Phone:")
        label_phone.grid(row=1, column=0, padx=5, pady=5)
        self.entry_phone = ctk.CTkEntry(frame_input, width=200)
        self.entry_phone.grid(row=1, column=1, padx=5, pady=5)

        # Кнопки управления
        frame_buttons = ctk.CTkFrame(self.content_frame)
        frame_buttons.pack(pady=10)

        button_add = ctk.CTkButton(frame_buttons, text="Add Client", command=self.add_new_client)
        button_add.grid(row=0, column=0, padx=5, pady=5)

        button_update = ctk.CTkButton(frame_buttons, text="Update Client Phone", command=self.update_client_phone)
        button_update.grid(row=0, column=1, padx=5, pady=5)

        button_delete = ctk.CTkButton(frame_buttons, text="Delete Client", command=self.delete_client)
        button_delete.grid(row=0, column=2, padx=5, pady=5)

        # Список клиентов
        frame_listbox = ctk.CTkFrame(self.content_frame)
        frame_listbox.pack(pady=10, fill="both", expand=True)

        self.listbox_clients = ctk.CTkTextbox(frame_listbox, width=500, height=200)
        self.listbox_clients.pack(padx=10, pady=10, fill="both", expand=True)

        # Загрузка списка клиентов
        self.show_all_clients()
    
    def show_all_clients(self):
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Clients")
            clients = cursor.fetchall()

            # Очистка текстового поля
            self.listbox_clients.delete("1.0", "end")

            # Заполнение текстового поля
            for client in clients:
                self.listbox_clients.insert("end", f"ID: {client[0]}, Name: {client[1]}, Phone: {client[2]}\n")

    def add_new_client(self):
        name = self.entry_name.get()
        phone = self.entry_phone.get()

        if not name or not phone:
            messagebox.showwarning("Input Error", "Please fill in both name and phone fields.")
            return

        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO Clients (Full_Name, Phone) VALUES (%s, %s)", (name, phone))
            connection.commit()
            messagebox.showinfo("Success", "Client added successfully!")
            self.show_all_clients()

    def delete_client(self):
        selected_text = self.listbox_clients.get("insert linestart", "insert lineend")
        if not selected_text:
            messagebox.showwarning("Selection Error", "Please select a client to delete.")
            return

        client_id = selected_text.split(",")[0].split(":")[1].strip()
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM Clients WHERE Client_ID = %s", (client_id,))
            connection.commit()
            messagebox.showinfo("Success", "Client deleted successfully!")
            self.show_all_clients()

    def update_client_phone(self):
        selected_text = self.listbox_clients.get("insert linestart", "insert lineend")
        if not selected_text:
            messagebox.showwarning("Selection Error", "Please select a client to update.")
            return

        client_id = selected_text.split(",")[0].split(":")[1].strip()
        new_phone = self.entry_phone.get()

        if not new_phone:
            messagebox.showwarning("Input Error", "Please enter a new phone number.")
            return

        with connection.cursor() as cursor:
            cursor.execute("UPDATE Clients SET Phone = %s WHERE Client_ID = %s", (new_phone, client_id))
            connection.commit()
            messagebox.showinfo("Success", "Client phone number updated!")
            self.show_all_clients()

    def show_memberships_page(self):
        # Очистка предыдущей страницы
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Заголовок страницы
        label_title = ctk.CTkLabel(self.content_frame, text="Memberships Management", font=ctk.CTkFont(size=20, weight="bold"))
        label_title.pack(pady=10)

        # Поля ввода
        frame_input = ctk.CTkFrame(self.content_frame)
        frame_input.pack(pady=10)

        label_type = ctk.CTkLabel(frame_input, text="Membership Type:")
        label_type.grid(row=0, column=0, padx=5, pady=5)
        self.entry_membership_type = ctk.CTkEntry(frame_input, width=200)
        self.entry_membership_type.grid(row=0, column=1, padx=5, pady=5)

        label_price = ctk.CTkLabel(frame_input, text="Price:")
        label_price.grid(row=1, column=0, padx=5, pady=5)
        self.entry_price = ctk.CTkEntry(frame_input, width=200)
        self.entry_price.grid(row=1, column=1, padx=5, pady=5)

        label_start = ctk.CTkLabel(frame_input, text="Start Date:")
        label_start.grid(row=2, column=0, padx=5, pady=5)
        self.entry_start = ctk.CTkEntry(frame_input, width=200)
        self.entry_start.grid(row=2, column=1, padx=5, pady=5)

        label_end = ctk.CTkLabel(frame_input, text="End Date:")
        label_end.grid(row=3, column=0, padx=5, pady=5)
        self.entry_end = ctk.CTkEntry(frame_input, width=200)
        self.entry_end.grid(row=3, column=1, padx=5, pady=5)

        # Кнопки управления
        frame_buttons = ctk.CTkFrame(self.content_frame)
        frame_buttons.pack(pady=10)

        button_add = ctk.CTkButton(frame_buttons, text="Add Membership", command=self.add_new_membership)
        button_add.grid(row=0, column=0, padx=5, pady=5)

        button_update = ctk.CTkButton(frame_buttons, text="Update Membership", command=self.update_membership)
        button_update.grid(row=0, column=1, padx=5, pady=5)

        button_delete = ctk.CTkButton(frame_buttons, text="Delete Membership", command=self.delete_membership)
        button_delete.grid(row=0, column=2, padx=5, pady=5)

        # Список Memberships
        frame_listbox = ctk.CTkFrame(self.content_frame)
        frame_listbox.pack(pady=10, fill="both", expand=True)

        self.listbox_memberships = ctk.CTkTextbox(frame_listbox, width=500, height=200)
        self.listbox_memberships.pack(padx=10, pady=10, fill="both", expand=True)

        # Загрузка списка memberships
        self.show_all_memberships()

    def add_new_membership(self):
        membership_type = self.entry_membership_type.get()
        price = self.entry_price.get()
        start = self.entry_start.get()
        end = self.entry_end.get()

        if not membership_type or not price:
            messagebox.showwarning("Input Error", "Please fill in both fields!")
            return

        try:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO Memberships (Membership_Type, Price, Start_Date, End_Date) VALUES (%s, %s,%s, %s)", (membership_type, price, start, end))
                connection.commit()
                messagebox.showinfo("Success", "Membership added successfully!")
                self.show_all_memberships()  # Обновить список
        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")

    
    def dummy_function(self):
        print("Button clicked")

    def update_membership(self):
        # Получить выделенный элемент
        selected_text = self.listbox_memberships.get("insert linestart", "insert lineend").strip()

        if not selected_text:
            messagebox.showwarning("Selection Error", "Please select a membership to update.")
            return

        # Извлечение ID членства
        try:
            membership_id = selected_text.split(",")[0].split(":")[1].strip()
            new_type = self.entry_membership_type.get()
            new_price = self.entry_price.get()

            if not (new_type or new_price):
                messagebox.showwarning("Input Error", "Please provide at least one field to update.")
                return

            with connection.cursor() as cursor:
                if new_type and new_price:
                    cursor.execute(
                        "UPDATE Memberships SET Membership_Type = %s, Price = %s WHERE Membership_ID = %s",
                        (new_type, new_price, membership_id)
                    )
                elif new_type:
                    cursor.execute(
                        "UPDATE Memberships SET Membership_Type = %s WHERE Membership_ID = %s",
                        (new_type, membership_id)
                    )
                elif new_price:
                    cursor.execute(
                        "UPDATE Memberships SET Price = %s WHERE Membership_ID = %s",
                        (new_price, membership_id)
                    )
                connection.commit()
                messagebox.showinfo("Success", "Membership updated successfully!")
                self.show_all_memberships()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def delete_membership(self):
        # Получить выбранный текст
        selected_text = self.listbox_memberships.get("insert linestart", "insert lineend").strip()

        if not selected_text:
            messagebox.showwarning("Selection Error", "Please select a membership to delete.")
            return

        # Извлечение ID членства из строки
        try:
            membership_id = selected_text.split(",")[0].split(":")[1].strip()
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM Memberships WHERE Membership_ID = %s", (membership_id,))
                connection.commit()
                messagebox.showinfo("Success", "Membership deleted successfully!")
                self.show_all_memberships()  # Обновить список
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")


    def show_all_memberships(self):
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT Membership_ID, Membership_Type, Price, Start_Date, End_Date FROM Memberships")
                memberships = cursor.fetchall()

                self.listbox_memberships.delete("1.0", "end")  # Очистка текстового поля

                for membership in memberships:
                    self.listbox_memberships.insert(
                        "end",
                        f"ID: {membership[0]}, Type: {membership[1]}, Price: {membership[2]} USD, "
                        f"Start: {membership[3]}, End: {membership[4]}\n"
                    )
        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")

    def show_trainers_page(self):
        # Очистка предыдущей страницы
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Заголовок страницы
        label_title = ctk.CTkLabel(
            self.content_frame, 
            text="Trainers Management", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        label_title.pack(pady=10)

        # Поля ввода
        frame_input = ctk.CTkFrame(self.content_frame)
        frame_input.pack(pady=10)

        label_name = ctk.CTkLabel(frame_input, text="Full Name:")
        label_name.grid(row=0, column=0, padx=5, pady=5)
        self.entry_trainer_name = ctk.CTkEntry(frame_input, width=200)
        self.entry_trainer_name.grid(row=0, column=1, padx=5, pady=5)

        label_specialization = ctk.CTkLabel(frame_input, text="Specialization:")
        label_specialization.grid(row=1, column=0, padx=5, pady=5)
        self.entry_specialization = ctk.CTkEntry(frame_input, width=200)
        self.entry_specialization.grid(row=1, column=1, padx=5, pady=5)

        label_phone = ctk.CTkLabel(frame_input, text="Phone:")
        label_phone.grid(row=2, column=0, padx=5, pady=5)
        self.entry_trainer_phone = ctk.CTkEntry(frame_input, width=200)
        self.entry_trainer_phone.grid(row=2, column=1, padx=5, pady=5)

        # Кнопки управления
        frame_buttons = ctk.CTkFrame(self.content_frame)
        frame_buttons.pack(pady=10)

        button_add = ctk.CTkButton(frame_buttons, text="Add Trainer", command=self.add_new_trainer)
        button_add.grid(row=0, column=0, padx=5, pady=5)

        button_update = ctk.CTkButton(frame_buttons, text="Update Trainer", command=self.update_trainer)
        button_update.grid(row=0, column=1, padx=5, pady=5)

        button_delete = ctk.CTkButton(frame_buttons, text="Delete Trainer", command=self.delete_trainer)
        button_delete.grid(row=0, column=2, padx=5, pady=5)

        # Список тренеров
        frame_listbox = ctk.CTkFrame(self.content_frame)
        frame_listbox.pack(pady=10, fill="both", expand=True)

        self.listbox_trainers = ctk.CTkTextbox(frame_listbox, width=500, height=200)
        self.listbox_trainers.pack(padx=10, pady=10, fill="both", expand=True)

        # Загрузка списка тренеров
        self.show_all_trainers()


    def add_new_trainer(self):
        name = self.entry_trainer_name.get()
        specialization = self.entry_specialization.get()
        phone = self.entry_trainer_phone.get()

        if not name or not specialization or not phone:
            messagebox.showwarning("Input Error", "Please fill in all fields.")
            return

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO Trainers (Full_Name, Specialization, Phone) VALUES (%s, %s, %s)",
                    (name, specialization, phone)
                )
                connection.commit()
                messagebox.showinfo("Success", "Trainer added successfully!")
                self.show_all_trainers()
        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")


    def update_trainer(self):
        selected_text = self.listbox_trainers.get("insert linestart", "insert lineend").strip()

        if not selected_text:
            messagebox.showwarning("Selection Error", "Please select a trainer to update.")
            return

        trainer_id = selected_text.split(",")[0].split(":")[1].strip()
        new_name = self.entry_trainer_name.get()
        new_specialization = self.entry_specialization.get()
        new_phone = self.entry_trainer_phone.get()

        if not (new_name or new_specialization or new_phone):
            messagebox.showwarning("Input Error", "Please provide at least one field to update.")
            return

        try:
            with connection.cursor() as cursor:
                if new_name:
                    cursor.execute("UPDATE Trainers SET Full_Name = %s WHERE Trainer_ID = %s", (new_name, trainer_id))
                if new_specialization:
                    cursor.execute(
                        "UPDATE Trainers SET Specialization = %s WHERE Trainer_ID = %s",
                        (new_specialization, trainer_id)
                    )
                if new_phone:
                    cursor.execute("UPDATE Trainers SET Phone = %s WHERE Trainer_ID = %s", (new_phone, trainer_id))
                connection.commit()
                messagebox.showinfo("Success", "Trainer updated successfully!")
                self.show_all_trainers()
        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")


    def delete_trainer(self):
        selected_text = self.listbox_trainers.get("insert linestart", "insert lineend").strip()

        if not selected_text:
            messagebox.showwarning("Selection Error", "Please select a trainer to delete.")
            return

        trainer_id = selected_text.split(",")[0].split(":")[1].strip()

        try:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM Trainers WHERE Trainer_ID = %s", (trainer_id,))
                connection.commit()
                messagebox.showinfo("Success", "Trainer deleted successfully!")
                self.show_all_trainers()
        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")


    def show_all_trainers(self):
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM Trainers")
                trainers = cursor.fetchall()

                self.listbox_trainers.delete("1.0", "end")  # Очистка текстового поля

                for trainer in trainers:
                    self.listbox_trainers.insert(
                        "end",
                        f"ID: {trainer[0]}, Name: {trainer[1]}, Specialization: {trainer[2]}, Phone: {trainer[3]}\n"
                    )
        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")

    def show_activities_page(self):
        # Очистка предыдущей страницы
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Заголовок страницы
        label_title = ctk.CTkLabel(
            self.content_frame, 
            text="Activities Management", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        label_title.pack(pady=10)

        # Поля ввода
        frame_input = ctk.CTkFrame(self.content_frame)
        frame_input.pack(pady=10)

        label_title = ctk.CTkLabel(frame_input, text="Title:")
        label_title.grid(row=0, column=0, padx=5, pady=5)
        self.entry_activity_title = ctk.CTkEntry(frame_input, width=200)
        self.entry_activity_title.grid(row=0, column=1, padx=5, pady=5)

        label_description = ctk.CTkLabel(frame_input, text="Description:")
        label_description.grid(row=1, column=0, padx=5, pady=5)
        self.entry_activity_description = ctk.CTkEntry(frame_input, width=200)
        self.entry_activity_description.grid(row=1, column=1, padx=5, pady=5)

        label_time = ctk.CTkLabel(frame_input, text="Time (HH:MM):")
        label_time.grid(row=2, column=0, padx=5, pady=5)
        self.entry_activity_time = ctk.CTkEntry(frame_input, width=200)
        self.entry_activity_time.grid(row=2, column=1, padx=5, pady=5)

        label_date = ctk.CTkLabel(frame_input, text="Date (YYYY-MM-DD):")
        label_date.grid(row=3, column=0, padx=5, pady=5)
        self.entry_activity_date = ctk.CTkEntry(frame_input, width=200)
        self.entry_activity_date.grid(row=3, column=1, padx=5, pady=5)

        # Кнопки управления
        frame_buttons = ctk.CTkFrame(self.content_frame)
        frame_buttons.pack(pady=10)

        button_add = ctk.CTkButton(frame_buttons, text="Add Activity", command=self.add_new_activity)
        button_add.grid(row=0, column=0, padx=5, pady=5)

        button_update = ctk.CTkButton(frame_buttons, text="Update Activity", command=self.update_activity)
        button_update.grid(row=0, column=1, padx=5, pady=5)

        button_delete = ctk.CTkButton(frame_buttons, text="Delete Activity", command=self.delete_activity)
        button_delete.grid(row=0, column=2, padx=5, pady=5)

        # Список активностей
        frame_listbox = ctk.CTkFrame(self.content_frame)
        frame_listbox.pack(pady=10, fill="both", expand=True)

        self.listbox_activities = ctk.CTkTextbox(frame_listbox, width=500, height=200)
        self.listbox_activities.pack(padx=10, pady=10, fill="both", expand=True)

        # Загрузка списка активностей
        self.show_all_activities()


    def add_new_activity(self):
        title = self.entry_activity_title.get()
        description = self.entry_activity_description.get()
        time = self.entry_activity_time.get()
        date = self.entry_activity_date.get()

        if not (title and time and date):
            messagebox.showwarning("Input Error", "Please fill in the required fields (Title, Time, Date).")
            return

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO Activities (Title, Description, Time, Date) VALUES (%s, %s, %s, %s)",
                    (title, description, time, date)
                )
                connection.commit()
                messagebox.showinfo("Success", "Activity added successfully!")
                self.show_all_activities()
        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")


    def update_activity(self):
        selected_text = self.listbox_activities.get("insert linestart", "insert lineend").strip()

        if not selected_text:
            messagebox.showwarning("Selection Error", "Please select an activity to update.")
            return

        activity_id = selected_text.split(",")[0].split(":")[1].strip()
        new_title = self.entry_activity_title.get()
        new_description = self.entry_activity_description.get()
        new_time = self.entry_activity_time.get()
        new_date = self.entry_activity_date.get()

        if not (new_title or new_description or new_time or new_date):
            messagebox.showwarning("Input Error", "Please provide at least one field to update.")
            return

        try:
            with connection.cursor() as cursor:
                if new_title:
                    cursor.execute("UPDATE Activities SET Title = %s WHERE Activity_ID = %s", (new_title, activity_id))
                if new_description:
                    cursor.execute("UPDATE Activities SET Description = %s WHERE Activity_ID = %s", (new_description, activity_id))
                if new_time:
                    cursor.execute("UPDATE Activities SET Time = %s WHERE Activity_ID = %s", (new_time, activity_id))
                if new_date:
                    cursor.execute("UPDATE Activities SET Date = %s WHERE Activity_ID = %s", (new_date, activity_id))
                connection.commit()
                messagebox.showinfo("Success", "Activity updated successfully!")
                self.show_all_activities()
        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")


    def delete_activity(self):
        selected_text = self.listbox_activities.get("insert linestart", "insert lineend").strip()

        if not selected_text:
            messagebox.showwarning("Selection Error", "Please select an activity to delete.")
            return

        activity_id = selected_text.split(",")[0].split(":")[1].strip()

        try:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM Activities WHERE Activity_ID = %s", (activity_id,))
                connection.commit()
                messagebox.showinfo("Success", "Activity deleted successfully!")
                self.show_all_activities()
        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")


    def show_all_activities(self):
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM Activities")
                activities = cursor.fetchall()

                self.listbox_activities.delete("1.0", "end")  # Очистка текстового поля

                for activity in activities:
                    self.listbox_activities.insert(
                        "end",
                        f"ID: {activity[0]}, Title: {activity[1]}, Description: {activity[2]}, Time: {activity[3]}, Date: {activity[4]}\n"
                    )
        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
    
    def show_activity_registration_page(self):
        # Очистка предыдущей страницы
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Заголовок страницы
        label_title = ctk.CTkLabel(
            self.content_frame, 
            text="Activity Registration Management", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        label_title.pack(pady=10)

        # Поля ввода
        frame_input = ctk.CTkFrame(self.content_frame)
        frame_input.pack(pady=10)

        # Поле выбора клиента
        label_client = ctk.CTkLabel(frame_input, text="Client:")
        label_client.grid(row=0, column=0, padx=5, pady=5)
        self.optionmenu_client = ctk.CTkOptionMenu(frame_input, values=[])
        self.optionmenu_client.grid(row=0, column=1, padx=5, pady=5)

        # Поле выбора активности
        label_activity = ctk.CTkLabel(frame_input, text="Activity:")
        label_activity.grid(row=1, column=0, padx=5, pady=5)
        self.optionmenu_activity = ctk.CTkOptionMenu(frame_input, values=[])
        self.optionmenu_activity.grid(row=1, column=1, padx=5, pady=5)

        # Поле для ввода статуса регистрации
        label_status = ctk.CTkLabel(frame_input, text="Registration Status:")
        label_status.grid(row=2, column=0, padx=5, pady=5)
        self.entry_registration_status = ctk.CTkEntry(frame_input, width=200)
        self.entry_registration_status.grid(row=2, column=1, padx=5, pady=5)

        # Кнопки управления
        frame_buttons = ctk.CTkFrame(self.content_frame)
        frame_buttons.pack(pady=10)

        button_add = ctk.CTkButton(frame_buttons, text="Add Registration", command=self.add_activity_registration)
        button_add.grid(row=0, column=0, padx=5, pady=5)

        button_update = ctk.CTkButton(frame_buttons, text="Update Registration", command=self.update_activity_registration)
        button_update.grid(row=0, column=1, padx=5, pady=5)

        button_delete = ctk.CTkButton(frame_buttons, text="Delete Registration", command=self.delete_activity_registration)
        button_delete.grid(row=0, column=2, padx=5, pady=5)

        # Список регистраций
        frame_listbox = ctk.CTkFrame(self.content_frame)
        frame_listbox.pack(pady=10, fill="both", expand=True)

        self.listbox_activity_registrations = ctk.CTkTextbox(frame_listbox, width=500, height=200)
        self.listbox_activity_registrations.pack(padx=10, pady=10, fill="both", expand=True)

        # Загрузка клиентов, активностей и регистраций
        self.load_clients_and_activities()
        self.show_all_activity_registrations()


    def load_clients_and_activities(self):
        """Загрузка данных клиентов и активностей для OptionMenu"""
        try:
            with connection.cursor() as cursor:
                # Загрузка клиентов
                cursor.execute("SELECT Client_ID, Full_Name FROM Clients")
                clients = cursor.fetchall()
                client_options = [f"{client[0]} - {client[1]}" for client in clients]
                self.optionmenu_client.configure(values=client_options)

                # Загрузка активностей
                cursor.execute("SELECT Activity_ID, Title FROM Activities")
                activities = cursor.fetchall()
                activity_options = [f"{activity[0]} - {activity[1]}" for activity in activities]
                self.optionmenu_activity.configure(values=activity_options)
        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")


    def add_activity_registration(self):
        selected_client = self.optionmenu_client.get()
        selected_activity = self.optionmenu_activity.get()
        status = self.entry_registration_status.get()

        if not (selected_client and selected_activity and status):
            messagebox.showwarning("Input Error", "Please fill in all fields.")
            return

        client_id = selected_client.split(" - ")[0]
        activity_id = selected_activity.split(" - ")[0]

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO Activity_Registration (Client_ID, Activity_ID, Registration_Status) VALUES (%s, %s, %s)",
                    (client_id, activity_id, status)
                )
                connection.commit()
                messagebox.showinfo("Success", "Activity registration added successfully!")
                self.show_all_activity_registrations()
        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")


    def update_activity_registration(self):
        selected_text = self.listbox_activity_registrations.get("insert linestart", "insert lineend").strip()

        if not selected_text:
            messagebox.showwarning("Selection Error", "Please select a registration to update.")
            return

        registration_id = selected_text.split(",")[0].split(":")[1].strip()
        new_status = self.entry_registration_status.get()

        if not new_status:
            messagebox.showwarning("Input Error", "Please provide a new status.")
            return

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE Activity_Registration SET Registration_Status = %s WHERE Registration_ID = %s",
                    (new_status, registration_id)
                )
                connection.commit()
                messagebox.showinfo("Success", "Activity registration updated successfully!")
                self.show_all_activity_registrations()
        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")


    def delete_activity_registration(self):
        selected_text = self.listbox_activity_registrations.get("insert linestart", "insert lineend").strip()

        if not selected_text:
            messagebox.showwarning("Selection Error", "Please select a registration to delete.")
            return

        registration_id = selected_text.split(",")[0].split(":")[1].strip()

        try:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM Activity_Registration WHERE Registration_ID = %s", (registration_id,))
                connection.commit()
                messagebox.showinfo("Success", "Activity registration deleted successfully!")
                self.show_all_activity_registrations()
        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")


    def show_all_activity_registrations(self):
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """SELECT ar.Registration_ID, c.Full_Name, a.Title, ar.Registration_Status
                    FROM Activity_Registration ar
                    JOIN Clients c ON ar.Client_ID = c.Client_ID
                    JOIN Activities a ON ar.Activity_ID = a.Activity_ID"""
                )
                registrations = cursor.fetchall()

                self.listbox_activity_registrations.delete("1.0", "end")  # Очистка текстового поля

                for reg in registrations:
                    self.listbox_activity_registrations.insert(
                        "end",
                        f"ID: {reg[0]}, Client: {reg[1]}, Activity: {reg[2]}, Status: {reg[3]}\n"
                    )
        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")

# Запуск приложения
if __name__ == "__main__":
    app = AdminApp()
    app.mainloop()
