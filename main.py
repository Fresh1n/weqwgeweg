import customtkinter as ctk
from tkinter import messagebox, filedialog
from database import Database
from datetime import datetime
import json
import os

class PlantCareApp:
    def __init__(self):
        self.db = Database()
        self.current_user = None
        self.current_screen = None
        
        # Configure CustomTkinter
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("green")
        
        # Create main window
        self.root = ctk.CTk()
        self.root.title("PlantCare - Помощник садовода")
        self.root.geometry("500x800")
        self.root.minsize(400, 600)
        
        # Container for screens
        self.screen_container = ctk.CTkFrame(self.root)
        self.screen_container.pack(fill="both", expand=True)
        
        # Bottom navigation
        self.bottom_nav = self.create_bottom_navigation()
        self.bottom_nav.pack(side="bottom", fill="x", padx=10, pady=10)
        
        # Show login screen first
        self.show_login_screen()
        
        self.root.mainloop()
    
    def create_bottom_navigation(self):
        nav_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        
        nav_frame.columnconfigure(0, weight=1)
        nav_frame.columnconfigure(1, weight=1)
        nav_frame.columnconfigure(2, weight=1)
        nav_frame.columnconfigure(3, weight=1)
        
        self.home_btn = ctk.CTkButton(nav_frame, text="🏠 Главная", command=lambda: self.show_home_screen(), fg_color="transparent", hover_color=("gray75", "gray25"))
        self.home_btn.grid(row=0, column=0, padx=5, pady=5)
        
        self.catalog_btn = ctk.CTkButton(nav_frame, text="🔍 Каталог", command=lambda: self.show_catalog_screen(), fg_color="transparent", hover_color=("gray75", "gray25"))
        self.catalog_btn.grid(row=0, column=1, padx=5, pady=5)
        
        self.plants_btn = ctk.CTkButton(nav_frame, text="🌿 Растения", command=lambda: self.show_my_plants_screen(), fg_color="transparent", hover_color=("gray75", "gray25"))
        self.plants_btn.grid(row=0, column=2, padx=5, pady=5)
        
        self.profile_btn = ctk.CTkButton(nav_frame, text="👤 Профиль", command=lambda: self.show_profile_screen(), fg_color="transparent", hover_color=("gray75", "gray25"))
        self.profile_btn.grid(row=0, column=3, padx=5, pady=5)
        
        # Hide navigation initially
        nav_frame.pack_forget()
        return nav_frame
    
    def show_bottom_navigation(self):
        self.bottom_nav.pack(side="bottom", fill="x", padx=10, pady=10)
    
    def hide_bottom_navigation(self):
        self.bottom_nav.pack_forget()
    
    def clear_screen(self):
        for widget in self.screen_container.winfo_children():
            widget.destroy()
    
    def show_login_screen(self):
        self.clear_screen()
        self.hide_bottom_navigation()
        
        frame = ctk.CTkFrame(self.screen_container)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header
        ctk.CTkLabel(frame, text="🌿 PlantCare", font=("Roboto", 32, "bold")).pack(pady=(40, 10))
        ctk.CTkLabel(frame, text="Помощник садовода", font=("Roboto", 16)).pack(pady=(0, 40))
        
        # Login form
        form_frame = ctk.CTkFrame(frame, fg_color=("gray95", "gray10"))
        form_frame.pack(fill="x", pady=20)
        
        ctk.CTkLabel(form_frame, text="Вход в профиль", font=("Roboto", 20, "bold")).pack(pady=(20, 20))
        
        ctk.CTkLabel(form_frame, text="Email").pack(anchor="w", padx=20)
        email_entry = ctk.CTkEntry(form_frame, placeholder_text="email@example.com")
        email_entry.pack(fill="x", padx=20, pady=(0, 15))
        
        ctk.CTkLabel(form_frame, text="Пароль").pack(anchor="w", padx=20)
        password_entry = ctk.CTkEntry(form_frame, placeholder_text="Введите пароль", show="*")
        password_entry.pack(fill="x", padx=20, pady=(0, 20))
        
        ctk.CTkButton(form_frame, text="Войти", command=lambda: self.login(email_entry.get(), password_entry.get())).pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(form_frame, text="Нет аккаунта?").pack(pady=(20, 5))
        ctk.CTkButton(form_frame, text="Зарегистрироваться", command=self.show_register_screen, fg_color="transparent", text_color=("gray10", "gray90")).pack(pady=(0, 20))
    
    def show_register_screen(self):
        self.clear_screen()
        self.hide_bottom_navigation()
        
        frame = ctk.CTkFrame(self.screen_container)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header
        ctk.CTkLabel(frame, text="🌿 PlantCare", font=("Roboto", 32, "bold")).pack(pady=(40, 10))
        ctk.CTkLabel(frame, text="Помощник садовода", font=("Roboto", 16)).pack(pady=(0, 40))
        
        # Register form
        form_frame = ctk.CTkFrame(frame, fg_color=("gray95", "gray10"))
        form_frame.pack(fill="x", pady=20)
        
        ctk.CTkLabel(form_frame, text="Создать профиль", font=("Roboto", 20, "bold")).pack(pady=(20, 20))
        
        ctk.CTkLabel(form_frame, text="Имя").pack(anchor="w", padx=20)
        name_entry = ctk.CTkEntry(form_frame, placeholder_text="Введите ваше имя")
        name_entry.pack(fill="x", padx=20, pady=(0, 15))
        
        ctk.CTkLabel(form_frame, text="Email").pack(anchor="w", padx=20)
        email_entry = ctk.CTkEntry(form_frame, placeholder_text="email@example.com")
        email_entry.pack(fill="x", padx=20, pady=(0, 15))
        
        ctk.CTkLabel(form_frame, text="Пароль").pack(anchor="w", padx=20)
        password_entry = ctk.CTkEntry(form_frame, placeholder_text="Минимум 6 символов", show="*")
        password_entry.pack(fill="x", padx=20, pady=(0, 15))
        
        ctk.CTkLabel(form_frame, text="Возраст").pack(anchor="w", padx=20)
        age_entry = ctk.CTkEntry(form_frame, placeholder_text="25")
        age_entry.pack(fill="x", padx=20, pady=(0, 20))
        
        ctk.CTkButton(form_frame, text="Зарегистрироваться", command=lambda: self.register(name_entry.get(), email_entry.get(), password_entry.get(), age_entry.get())).pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(form_frame, text="Уже есть аккаунт?").pack(pady=(20, 5))
        ctk.CTkButton(form_frame, text="Войти", command=self.show_login_screen, fg_color="transparent", text_color=("gray10", "gray90")).pack(pady=(0, 20))
    
    def login(self, email, password):
        if not email or not password:
            messagebox.showerror("Ошибка", "Заполните все поля")
            return
        
        user = self.db.authenticate_user(email, password)
        if user:
            self.current_user = user
            self.show_bottom_navigation()
            self.show_home_screen()
        else:
            messagebox.showerror("Ошибка", "Неверный email или пароль")
    
    def register(self, name, email, password, age):
        if not name or not email or not password:
            messagebox.showerror("Ошибка", "Заполните все обязательные поля")
            return
        
        if len(password) < 6:
            messagebox.showerror("Ошибка", "Пароль должен быть минимум 6 символов")
            return
        
        try:
            age_int = int(age) if age else None
        except ValueError:
            messagebox.showerror("Ошибка", "Некорректный возраст")
            return
        
        if self.db.create_user(name, email, password, age_int):
            messagebox.showinfo("Успех", "Аккаунт создан! Теперь войдите.")
            self.show_login_screen()
        else:
            messagebox.showerror("Ошибка", "Пользователь с таким email уже существует")
    
    def logout(self):
        self.current_user = None
        self.hide_bottom_navigation()
        self.show_login_screen()
    
    def show_home_screen(self):
        self.clear_screen()
        self.show_bottom_navigation()
        
        scroll_frame = ctk.CTkScrollableFrame(self.screen_container)
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header
        header_frame = ctk.CTkFrame(scroll_frame, fg_color=("gray95", "gray10"))
        header_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(header_frame, text="🌿 Растения+", font=("Roboto", 28, "bold")).pack(pady=(20, 5))
        ctk.CTkLabel(header_frame, text="Помощник садовода", font=("Roboto", 14)).pack(pady=(0, 5))
        ctk.CTkLabel(header_frame, text=f"Привет, {self.current_user['name']}!", font=("Roboto", 12)).pack(pady=(0, 20))
        
        # Navigation buttons
        nav_frame = ctk.CTkFrame(scroll_frame)
        nav_frame.pack(fill="x", pady=10)
        
        ctk.CTkButton(nav_frame, text="➕ Добавить растение", command=self.show_catalog_screen, fg_color="#2d5a3d", hover_color="#1a3d2e").pack(fill="x", padx=10, pady=5)
        ctk.CTkButton(nav_frame, text="🌿 Мои растения", command=self.show_my_plants_screen, fg_color="transparent", border_color="#2d5a3d", text_color="#2d5a3d").pack(fill="x", padx=10, pady=5)
        
        # Tasks section
        ctk.CTkLabel(scroll_frame, text="📋 Задачи", font=("Roboto", 16, "bold")).pack(anchor="w", pady=(20, 10))
        
        tasks = self.db.get_tasks(self.current_user['id'], completed=False)
        if tasks:
            for task in tasks[:3]:
                task_frame = self.create_task_card(scroll_frame, task)
                task_frame.pack(fill="x", pady=5)
        else:
            ctk.CTkLabel(scroll_frame, text="Нет активных задач", text_color="gray").pack(pady=10)
        
        # Tips section
        ctk.CTkLabel(scroll_frame, text="💡 Советы", font=("Roboto", 16, "bold")).pack(anchor="w", pady=(20, 10))
        
        tips = self.db.get_tips()
        for tip in tips[:3]:
            tip_frame = self.create_tip_card(scroll_frame, tip)
            tip_frame.pack(fill="x", pady=5)
    
    def create_task_card(self, parent, task):
        frame = ctk.CTkFrame(parent, fg_color=("gray95", "gray10"))
        
        # Determine urgency based on scheduled date
        scheduled = datetime.fromisoformat(task['scheduled_date'])
        now = datetime.now()
        days_until = (scheduled - now).days
        
        if days_until <= 0:
            urgency_color = "#ff6b6b"
            urgency_text = "Срочно"
        elif days_until <= 1:
            urgency_color = "#ffd93d"
            urgency_text = "Важно"
        else:
            urgency_color = "#6bcb77"
            urgency_text = "Планово"
        
        # Icon based on task type
        icons = {'watering': '💧', 'fertilizing': '🧪', 'lighting': '☀️'}
        icon = icons.get(task['task_type'], '📋')
        
        content_frame = ctk.CTkFrame(frame, fg_color="transparent")
        content_frame.pack(fill="x", padx=15, pady=15)
        
        # Left side - icon and urgency
        left_frame = ctk.CTkFrame(content_frame, fg_color=urgency_color, width=50)
        left_frame.pack(side="left", padx=(0, 15))
        left_frame.pack_propagate(False)
        
        ctk.CTkLabel(left_frame, text=icon, font=("Roboto", 20)).pack(pady=(10, 5))
        ctk.CTkLabel(left_frame, text=urgency_text, font=("Roboto", 10), text_color="white").pack(pady=(0, 10))
        
        # Right side - task details
        right_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        right_frame.pack(side="left", fill="both", expand=True)
        
        ctk.CTkLabel(right_frame, text=task['description'], font=("Roboto", 14, "bold")).pack(anchor="w")
        ctk.CTkLabel(right_frame, text=scheduled.strftime("%d.%m.%Y %H:%M"), font=("Roboto", 12), text_color="gray").pack(anchor="w", pady=(5, 10))
        
        # Action buttons
        btn_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
        btn_frame.pack(fill="x")
        
        ctk.CTkButton(btn_frame, text="✓ Выполнено", width=80, height=30, command=lambda t=task['id']: self.complete_task(t), fg_color="#6bcb77", hover_color="#5aad66").pack(side="left", padx=(0, 5))
        ctk.CTkButton(btn_frame, text="⏰ Отложить", width=80, height=30, command=lambda t=task['id']: self.snooze_task(t), fg_color="transparent", border_color="#ffd93d", text_color="#ffd93d").pack(side="left")
        
        return frame
    
    def create_tip_card(self, parent, tip):
        frame = ctk.CTkFrame(parent, fg_color=("gray95", "gray10"))
        
        icons = {'watering': '💧', 'lighting': '☀️', 'diseases': '⚠️', 'fertilizing': '🧪', 'humidity': '💨', 'repotting': '🪴'}
        icon = icons.get(tip['category'], '💡')
        
        content_frame = ctk.CTkFrame(frame, fg_color="transparent")
        content_frame.pack(fill="x", padx=15, pady=15)
        
        # Icon
        icon_frame = ctk.CTkFrame(content_frame, fg_color="#a5d6a7", width=50)
        icon_frame.pack(side="left", padx=(0, 15))
        icon_frame.pack_propagate(False)
        
        ctk.CTkLabel(icon_frame, text=icon, font=("Roboto", 20)).pack(pady=15)
        
        # Content
        right_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        right_frame.pack(side="left", fill="both", expand=True)
        
        ctk.CTkLabel(right_frame, text=tip['title'], font=("Roboto", 14, "bold")).pack(anchor="w")
        ctk.CTkLabel(right_frame, text=tip['content'], font=("Roboto", 12), wraplength=300).pack(anchor="w", pady=(5, 0))
        
        return frame
    
    def complete_task(self, task_id):
        self.db.complete_task(task_id)
        self.show_home_screen()
    
    def snooze_task(self, task_id):
        self.db.snooze_task(task_id, days=1)
        self.show_home_screen()
    
    def show_catalog_screen(self):
        self.clear_screen()
        self.show_bottom_navigation()
        
        scroll_frame = ctk.CTkScrollableFrame(self.screen_container)
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header with back button
        header_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkButton(header_frame, text="← Назад", command=self.show_home_screen, fg_color="transparent", text_color=("gray10", "gray90"), width=60).pack(side="left")
        ctk.CTkLabel(header_frame, text="🔍 Каталог растений", font=("Roboto", 20, "bold")).pack(side="left", padx=10)
        
        # Search
        search_entry = ctk.CTkEntry(scroll_frame, placeholder_text="Поиск растений...")
        search_entry.pack(fill="x", pady=(0, 15))
        search_entry.bind("<KeyRelease>", lambda e: self.filter_catalog(scroll_frame, search_entry.get(), self.current_filter, self.current_light_filter))
        
        # Filters
        filter_frame = ctk.CTkFrame(scroll_frame, fg_color=("gray95", "gray10"))
        filter_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(filter_frame, text="Сложность:", font=("Roboto", 12, "bold")).pack(anchor="w", padx=10, pady=(10, 5))
        
        self.current_filter = "all"
        self.current_light_filter = "all"
        
        diff_frame = ctk.CTkFrame(filter_frame, fg_color="transparent")
        diff_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        ctk.CTkButton(diff_frame, text="Все", width=60, height=30, command=lambda: self.set_difficulty_filter("all", diff_btn, scroll_frame, search_entry.get())).grid(row=0, column=0, padx=2)
        ctk.CTkButton(diff_frame, text="Легкие", width=60, height=30, command=lambda: self.set_difficulty_filter("easy", diff_btn, scroll_frame, search_entry.get())).grid(row=0, column=1, padx=2)
        ctk.CTkButton(diff_frame, text="Средние", width=60, height=30, command=lambda: self.set_difficulty_filter("medium", diff_btn, scroll_frame, search_entry.get())).grid(row=0, column=2, padx=2)
        ctk.CTkButton(diff_frame, text="Сложные", width=60, height=30, command=lambda: self.set_difficulty_filter("hard", diff_btn, scroll_frame, search_entry.get())).grid(row=0, column=3, padx=2)
        
        ctk.CTkLabel(filter_frame, text="Освещение:", font=("Roboto", 12, "bold")).pack(anchor="w", padx=10, pady=(10, 5))
        
        light_frame = ctk.CTkFrame(filter_frame, fg_color="transparent")
        light_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        ctk.CTkButton(light_frame, text="Все", width=60, height=30, command=lambda: self.set_light_filter("all", light_btn, scroll_frame, search_entry.get())).grid(row=0, column=0, padx=2)
        ctk.CTkButton(light_frame, text="Солнце", width=60, height=30, command=lambda: self.set_light_filter("sun", light_btn, scroll_frame, search_entry.get())).grid(row=0, column=1, padx=2)
        ctk.CTkButton(light_frame, text="Тень", width=60, height=30, command=lambda: self.set_light_filter("shade", light_btn, scroll_frame, search_entry.get())).grid(row=0, column=2, padx=2)
        
        diff_btn = diff_frame
        light_btn = light_frame
        
        # Plants grid
        self.plants_container = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        self.plants_container.pack(fill="both", expand=True)
        
        self.load_plants_to_catalog(self.plants_container)
    
    def set_difficulty_filter(self, difficulty, btn_frame, parent, search):
        self.current_filter = difficulty
        # Передаем строго по порядку, проверяя, что search - это строка текста
        search_text = search if isinstance(search, str) else None
        self.filter_catalog(parent, search_text, difficulty, self.current_light_filter)

    def set_light_filter(self, light, btn_frame, parent, search):
        self.current_light_filter = light
        # Передаем строго по порядку, проверяя, что search - это строка текста
        search_text = search if isinstance(search, str) else None
        self.filter_catalog(parent, search_text, self.current_filter, light)
    
    def filter_catalog(self, parent, search, difficulty, light):
        for widget in self.plants_container.winfo_children():
            widget.destroy()
        
        plants = self.db.get_plant_catalog(
            difficulty=difficulty if difficulty != "all" else None,
            light=light if light != "all" else None,
            search=search if search else None
        )
        
        self.display_plants_grid(self.plants_container, plants)
    
    def load_plants_to_catalog(self, parent):
        plants = self.db.get_plant_catalog()
        print(f"Loaded {len(plants)} plants from catalog")
        for plant in plants:
            print(f"Plant: {plant['name_ru']}")
        self.display_plants_grid(parent, plants)
    
    def display_plants_grid(self, parent, plants):
        grid_frame = ctk.CTkFrame(parent, fg_color="transparent")
        grid_frame.pack(fill="both", expand=True)
        
        for i, plant in enumerate(plants):
            row = i // 2
            col = i % 2
            
            plant_card = self.create_plant_card(grid_frame, plant)
            plant_card.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
        
        grid_frame.columnconfigure(0, weight=1)
        grid_frame.columnconfigure(1, weight=1)
    
    def create_plant_card(self, parent, plant):
        frame = ctk.CTkFrame(parent, fg_color=("gray95", "gray10"))
        
        ctk.CTkLabel(frame, text=plant['icon'], font=("Roboto", 36)).pack(pady=(15, 10))
        ctk.CTkLabel(frame, text=plant['name_ru'], font=("Roboto", 14, "bold")).pack(pady=(0, 5))
        
        difficulty_colors = {'easy': '#6bcb77', 'medium': '#ffd93d', 'hard': '#ff6b6b'}
        difficulty_text = {'easy': 'Легкий', 'medium': 'Средний', 'hard': 'Сложный'}
        
        ctk.CTkLabel(frame, text=difficulty_text.get(plant['difficulty'], plant['difficulty']), 
                     fg_color=difficulty_colors.get(plant['difficulty'], 'gray'), 
                     text_color="white", corner_radius=10, padx=10, pady=5).pack(pady=(5, 10))
        
        ctk.CTkButton(frame, text="Добавить", command=lambda p=plant['id']: self.add_plant_to_collection(p), 
                      fg_color="#2d5a3d", hover_color="#1a3d2e").pack(pady=(0, 15))
        
        return frame
    
    def add_plant_to_collection(self, plant_id):
        nickname = ctk.CTkInputDialog(text="Введите название для растения (необязательно):", title="Добавление растения").get_input()
        
        if self.db.add_user_plant(self.current_user['id'], plant_id, nickname if nickname else None):
            messagebox.showinfo("Успех", "Растение добавлено в коллекцию!")
        else:
            messagebox.showerror("Ошибка", "Не удалось добавить растение")
    
    def show_my_plants_screen(self):
        self.clear_screen()
        self.show_bottom_navigation()
        
        scroll_frame = ctk.CTkScrollableFrame(self.screen_container)
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header with back button
        header_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkButton(header_frame, text="← Назад", command=self.show_home_screen, fg_color="transparent", text_color=("gray10", "gray90"), width=60).pack(side="left")
        ctk.CTkLabel(header_frame, text="🌿 Мои растения", font=("Roboto", 20, "bold")).pack(side="left", padx=10)
        
        # Statistics
        stats = self.db.get_user_stats(self.current_user['id'])
        
        stats_frame = ctk.CTkFrame(scroll_frame, fg_color=("gray95", "gray10"))
        stats_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkFrame(stats_frame, fg_color="transparent").grid(row=0, column=0, padx=10, pady=10)
        ctk.CTkLabel(stats_frame, text=str(stats['total_plants']), font=("Roboto", 24, "bold"), text_color="#2d5a3d").grid(row=0, column=1, padx=10, pady=10)
        ctk.CTkLabel(stats_frame, text="Растений", font=("Roboto", 12)).grid(row=1, column=1, padx=10, pady=(0, 10))
        
        ctk.CTkFrame(stats_frame, fg_color="transparent").grid(row=0, column=2, padx=10, pady=10)
        ctk.CTkLabel(stats_frame, text=str(stats['needs_water']), font=("Roboto", 24, "bold"), text_color="#2196f3").grid(row=0, column=3, padx=10, pady=10)
        ctk.CTkLabel(stats_frame, text="Требуют полива", font=("Roboto", 12)).grid(row=1, column=3, padx=10, pady=(0, 10))
        
        ctk.CTkFrame(stats_frame, fg_color="transparent").grid(row=0, column=4, padx=10, pady=10)
        ctk.CTkLabel(stats_frame, text=str(stats['healthy']), font=("Roboto", 24, "bold"), text_color="#6bcb77").grid(row=0, column=5, padx=10, pady=10)
        ctk.CTkLabel(stats_frame, text="Здоровых", font=("Roboto", 12)).grid(row=1, column=5, padx=10, pady=(0, 10))
        
        # Plants list
        ctk.CTkLabel(scroll_frame, text="📦 Коллекция", font=("Roboto", 16, "bold")).pack(anchor="w", pady=(20, 10))
        
        plants = self.db.get_user_plants(self.current_user['id'])
        
        if plants:
            for plant in plants:
                plant_frame = self.create_user_plant_card(scroll_frame, plant)
                plant_frame.pack(fill="x", pady=5)
        else:
            empty_frame = ctk.CTkFrame(scroll_frame, fg_color=("gray95", "gray10"))
            empty_frame.pack(fill="x", pady=20)
            
            ctk.CTkLabel(empty_frame, text="🌿", font=("Roboto", 48)).pack(pady=(20, 10))
            ctk.CTkLabel(empty_frame, text="В коллекции пока нет растений", font=("Roboto", 16, "bold")).pack(pady=(0, 5))
            ctk.CTkLabel(empty_frame, text="Добавьте первое растение", font=("Roboto", 12), text_color="gray").pack(pady=(0, 15))
            ctk.CTkButton(empty_frame, text="➕ Добавить растение", command=self.show_catalog_screen, fg_color="#2d5a3d").pack(pady=(0, 20))
    
    def create_user_plant_card(self, parent, plant):
        frame = ctk.CTkFrame(parent, fg_color=("gray95", "gray10"))
        
        content_frame = ctk.CTkFrame(frame, fg_color="transparent")
        content_frame.pack(fill="x", padx=15, pady=15)
        
        # Icon
        icon_frame = ctk.CTkFrame(content_frame, fg_color="#a5d6a7", width=60)
        icon_frame.pack(side="left", padx=(0, 15))
        icon_frame.pack_propagate(False)
        
        ctk.CTkLabel(icon_frame, text=plant['icon'], font=("Roboto", 28)).pack(pady=15)
        
        # Plant info
        info_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True)
        
        name = plant['nickname'] if plant['nickname'] else plant['name_ru']
        ctk.CTkLabel(info_frame, text=name, font=("Roboto", 16, "bold")).pack(anchor="w")
        ctk.CTkLabel(info_frame, text=plant['name_ru'], font=("Roboto", 12), text_color="gray").pack(anchor="w")
        
        if plant['last_watered']:
            last_watered = datetime.fromisoformat(plant['last_watered'])
            ctk.CTkLabel(info_frame, text=f"Последний полив: {last_watered.strftime('%d.%m.%Y')}", 
                         font=("Roboto", 11), text_color="gray").pack(anchor="w", pady=(5, 0))
        
        # Actions
        action_frame = ctk.CTkFrame(frame, fg_color="transparent")
        action_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        ctk.CTkButton(action_frame, text="💧 Полить", width=80, height=30, 
                     command=lambda p=plant['id']: self.water_plant(p), fg_color="#2196f3", hover_color="#1976d2").pack(side="left", padx=(0, 5))
        ctk.CTkButton(action_frame, text="🧪 Удобрить", width=80, height=30, 
                     command=lambda p=plant['id']: self.fertilize_plant(p), fg_color="#ffd93d", hover_color="#ffc107", text_color="black").pack(side="left", padx=(0, 5))
        ctk.CTkButton(action_frame, text="🗑️ Удалить", width=80, height=30, 
                     command=lambda p=plant['id']: self.delete_plant(p), fg_color="#ff6b6b", hover_color="#ee5a52").pack(side="right")
        
        return frame
    
    def water_plant(self, plant_id):
        self.db.update_plant_watered(plant_id)
        messagebox.showinfo("Успех", "Растение полито!")
        self.show_my_plants_screen()
    
    def fertilize_plant(self, plant_id):
        self.db.update_plant_fertilized(plant_id)
        messagebox.showinfo("Успех", "Удобрение внесено!")
        self.show_my_plants_screen()
    
    def delete_plant(self, plant_id):
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить это растение?"):
            self.db.delete_user_plant(plant_id)
            self.show_my_plants_screen()
    
    def show_profile_screen(self):
        self.clear_screen()
        self.show_bottom_navigation()
        
        scroll_frame = ctk.CTkScrollableFrame(self.screen_container)
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Profile header
        header_frame = ctk.CTkFrame(scroll_frame, fg_color="#2d5a3d")
        header_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkButton(header_frame, text="← Назад", command=self.show_home_screen, 
                     fg_color="#4a8c6a", text_color="white", width=70, height=30).pack(side="left", padx=15, pady=15)
        
        ctk.CTkFrame(header_frame, fg_color="#4a8c6a", width=50, height=50).pack(side="left", padx=15, pady=15)
        ctk.CTkLabel(header_frame, text="👤", font=("Roboto", 24)).place(in_=header_frame, relx=0.15, rely=0.5, anchor="center")
        
        info_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True, padx=15, pady=15)
        
        ctk.CTkLabel(header_frame, text=self.current_user['name'], font=("Roboto", 18, "bold"), text_color="white").pack(side="left", padx=(15, 0), pady=15)
        ctk.CTkLabel(header_frame, text=self.current_user['email'], font=("Roboto", 12), text_color="#e8f5e9").pack(side="left", padx=(15, 0), pady=(0, 15))
        
        # Stats
        stats = self.db.get_user_stats(self.current_user['id'])
        
        stats_frame = ctk.CTkFrame(scroll_frame, fg_color=("gray95", "gray10"))
        stats_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkFrame(stats_frame, fg_color="transparent").grid(row=0, column=0, padx=10, pady=10)
        ctk.CTkLabel(stats_frame, text=str(stats['total_plants']), font=("Roboto", 28, "bold"), text_color="#2d5a3d").grid(row=0, column=1, padx=10, pady=10)
        ctk.CTkLabel(stats_frame, text="Растений", font=("Roboto", 11)).grid(row=1, column=1, padx=10, pady=(0, 10))
        
        ctk.CTkFrame(stats_frame, fg_color="#2d5a3d").grid(row=0, column=2, padx=10, pady=10)
        ctk.CTkLabel(stats_frame, text="🌿", font=("Roboto", 28), text_color="white").grid(row=0, column=3, padx=10, pady=10)
        ctk.CTkLabel(stats_frame, text="Активен", font=("Roboto", 11), text_color="#e8f5e9").grid(row=1, column=3, padx=10, pady=(0, 10))
        
        # Settings menu
        settings_frame = ctk.CTkFrame(scroll_frame, fg_color=("gray95", "gray10"))
        settings_frame.pack(fill="x", pady=(0, 20))
        
        self.create_menu_button(settings_frame, "✏️ Редактировать профиль", self.show_edit_profile)
        self.create_menu_button(settings_frame, "📥 Экспорт данных", self.export_data)
        self.create_menu_button(settings_frame, "📤 Импорт данных", self.import_data)
        self.create_menu_button(settings_frame, "🌙 Тёмная тема", self.toggle_theme)
        self.create_menu_button(settings_frame, "🗑️ Удалить данные", self.clear_all_data, danger=True)
        self.create_menu_button(settings_frame, "🚪 Выйти", self.logout)
    
    def create_menu_button(self, parent, text, command, danger=False):
        btn = ctk.CTkButton(parent, text=text, command=command, 
                           fg_color="transparent", hover_color=("gray85", "gray15"),
                           text_color=("gray10", "gray90") if not danger else "#ff6b6b",
                           height=45, anchor="w")
        btn.pack(fill="x", padx=15, pady=2)
    
    def show_edit_profile(self):
        edit_window = ctk.CTkToplevel(self.root)
        edit_window.title("Редактировать профиль")
        edit_window.geometry("400x400")
        
        frame = ctk.CTkFrame(edit_window)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(frame, text="Редактировать профиль", font=("Roboto", 20, "bold")).pack(pady=(20, 30))
        
        ctk.CTkLabel(frame, text="Имя").pack(anchor="w")
        name_entry = ctk.CTkEntry(frame)
        name_entry.insert(0, self.current_user['name'])
        name_entry.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(frame, text="Email").pack(anchor="w")
        email_entry = ctk.CTkEntry(frame)
        email_entry.insert(0, self.current_user['email'])
        email_entry.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(frame, text="Возраст").pack(anchor="w")
        age_entry = ctk.CTkEntry(frame)
        if self.current_user['age']:
            age_entry.insert(0, str(self.current_user['age']))
        age_entry.pack(fill="x", pady=(0, 20))
        
        def save_profile():
            name = name_entry.get()
            email = email_entry.get()
            age = age_entry.get()
            
            try:
                age_int = int(age) if age else None
            except ValueError:
                messagebox.showerror("Ошибка", "Некорректный возраст")
                return
            
            if self.db.update_user(self.current_user['id'], name=name, email=email, age=age_int):
                self.current_user = self.db.get_user(self.current_user['id'])
                messagebox.showinfo("Успех", "Профиль обновлен!")
                edit_window.destroy()
                self.show_profile_screen()
            else:
                messagebox.showerror("Ошибка", "Не удалось обновить профиль")
        
        ctk.CTkButton(frame, text="Сохранить", command=save_profile, fg_color="#2d5a3d").pack(fill="x", pady=10)
    
    def export_data(self):
        data = self.db.export_user_data(self.current_user['id'])
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")],
            title="Сохранить данные"
        )
        
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(data)
            messagebox.showinfo("Успех", "Данные экспортированы!")
    
    def import_data(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json")],
            title="Выберите файл для импорта"
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                messagebox.showinfo("Успех", "Данные импортированы! (Функция в разработке)")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось импортировать данные: {e}")
    
    def toggle_theme(self):
        current_mode = ctk.get_appearance_mode()
        new_mode = "Dark" if current_mode == "Light" else "Light"
        ctk.set_appearance_mode(new_mode)
    
    def clear_all_data(self):
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить все данные? Это действие нельзя отменить."):
            self.db.clear_user_data(self.current_user['id'])
            messagebox.showinfo("Успех", "Все данные удалены!")
            self.show_home_screen()


if __name__ == "__main__":
    app = PlantCareApp()
