import sqlite3
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import os

class Database:
    def __init__(self, db_path: str = "plantcare.db"):
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_database(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                age INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Plants catalog
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS plant_catalog (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                name_ru TEXT NOT NULL,
                difficulty TEXT NOT NULL,
                light_requirement TEXT NOT NULL,
                water_frequency INTEGER NOT NULL,
                description TEXT,
                care_tips TEXT,
                icon TEXT
            )
        ''')
        
        # User's plants
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_plants (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                plant_id INTEGER NOT NULL,
                nickname TEXT,
                date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_watered TIMESTAMP,
                last_fertilized TIMESTAMP,
                health_status TEXT DEFAULT 'healthy',
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (plant_id) REFERENCES plant_catalog(id)
            )
        ''')
        
        # Tasks
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                user_plant_id INTEGER,
                task_type TEXT NOT NULL,
                description TEXT NOT NULL,
                scheduled_date TIMESTAMP NOT NULL,
                completed BOOLEAN DEFAULT FALSE,
                completed_date TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (user_plant_id) REFERENCES user_plants(id)
            )
        ''')
        
        # Tips
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tips (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                title TEXT NOT NULL,
                content TEXT NOT NULL
            )
        ''')
        
        # Сначала коммитим структуру таблиц
        conn.commit()
        
        # Запускаем популяцию (она отработает на этом же курсоре)
        self.populate_initial_data(cursor)
        
        # ЖЕЛЕЗОБЕТОННЫЙ КОММИТ НАМЕРТВО для растений и советов!
        conn.commit() 
        
        conn.close()
    
    def populate_initial_data(self, cursor):
        print("====== ЗАПУСК ПОПУЛЯЦИИ БАЗЫ ДАННЫХ ======")
        
        # Сбрасываем row_factory для точной проверки
        cursor.row_factory = None 
        cursor.execute('SELECT COUNT(*) FROM plant_catalog')
        res = cursor.fetchone()
        
        print(f"Результат проверки COUNT(*): {res}")
        
        if res and res[0] > 0:
            print(f"Каталог НЕ ПУСТОЙ (найдено {res[0]} записей). Отмена вставки.")
            cursor.row_factory = sqlite3.Row
            return
            
        print("Каталог пуст! Начинаем заливку растений...")
        cursor.row_factory = sqlite3.Row
        
        plants = [
            (1, 'Monstera', 'Монстера', 'medium', 'shade', 7, 'Популярное тропическое растение с крупными листьями', 'Полив раз в неделю, опрыскивание листов', '🌿'),
            (2, 'Ficus', 'Фикус', 'easy', 'sun', 10, 'Классическое комнатное растение', 'Яркий свет, умеренный полив', '🌱'),
            (3, 'Succulent', 'Суккулент', 'easy', 'sun', 14, 'Неприхотливое засухоустойчивое растение', 'Минимальный полив, много света', '🌵'),
            (4, 'Snake Plant', 'Сансевиерия', 'easy', 'shade', 14, 'Очень неприхотливое растение', 'Полив раз в 2 недели', '🌿'),
            (5, 'Peace Lily', 'Спатифиллум', 'medium', 'shade', 5, 'Красивое цветущее растение', 'Влажная почва, рассеянный свет', '🌸'),
            (6, 'Pothos', 'Плющ', 'easy', 'shade', 7, 'Вьющееся растение', 'Полив когда почва подсохла', '🍃'),
            (7, 'Aloe Vera', 'Алоэ', 'easy', 'sun', 14, 'Лекарственное растение', 'Минимальный полив, много света', '🌵'),
            (8, 'Rubber Plant', 'Фикус каучуконосный', 'medium', 'sun', 10, 'Крупное декоративное растение', 'Яркий свет, умеренный полив', '🌳'),
            (9, 'ZZ Plant', 'Замиокулькас', 'easy', 'shade', 21, 'Очень неприхотливое растение', 'Полив раз в 3 недели', '🌿'),
            (10, 'Spider Plant', 'Хлорофитум', 'easy', 'shade', 7, 'Легкое в уходе растение', 'Полив раз в неделю', '🌱'),
        ]
        
        try:
            cursor.executemany('''
                INSERT INTO plant_catalog (id, name, name_ru, difficulty, light_requirement, water_frequency, description, care_tips, icon)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', plants)
            print(f"Успешно добавлено растений в таблицу: {len(plants)}")
        except Exception as e:
            print(f"❌ ОШИБКА при вставке растений: {e}")
        
        tips = [
            (1, 'watering', 'Полив', 'Поливайте когда почва подсохла'),
            (2, 'lighting', 'Освещение', 'Поворачивайте раз в неделю для равномерного роста'),
            (3, 'diseases', 'Болезни', 'Желтые листья - проблема с поливом'),
            (4, 'fertilizing', 'Удобрение', 'Удобряйте весной и летом раз в месяц'),
            (5, 'humidity', 'Влажность', 'Опрыскивайте листья для повышения влажности'),
            (6, 'repotting', 'Пересадка', 'Пересаживайте каждые 1-2 года'),
        ]
        
        try:
            cursor.executemany('''
                INSERT INTO tips (id, category, title, content)
                VALUES (?, ?, ?, ?)
            ''', tips)
            print(f"Успешно добавлено советов в таблицу: {len(tips)}")
        except Exception as e:
            print(f"❌ ОШИБКА при вставке советов: {e}")
            
        print("====== КОНЕЦ ПОПУЛЯЦИИ БАЗЫ ДАННЫХ ======")

    # User operations
    def create_user(self, name: str, email: str, password: str, age: int = None) -> bool:
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO users (name, email, password, age)
                VALUES (?, ?, ?, ?)
            ''', (name, email, password, age))
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def authenticate_user(self, email: str, password: str) -> Optional[Dict]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, name, email, age FROM users WHERE email = ? AND password = ?
        ''', (email, password))
        user = cursor.fetchone()
        conn.close()
        return dict(user) if user else None
    
    def get_user(self, user_id: int) -> Optional[Dict]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, email, age FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        conn.close()
        return dict(user) if user else None
    
    def update_user(self, user_id: int, name: str = None, email: str = None, age: int = None) -> bool:
        conn = self.get_connection()
        cursor = conn.cursor()
        
        updates = []
        params = []
        if name:
            updates.append('name = ?')
            params.append(name)
        if email:
            updates.append('email = ?')
            params.append(email)
        if age is not None:
            updates.append('age = ?')
            params.append(age)
        
        if updates:
            params.append(user_id)
            cursor.execute(f'''
                UPDATE users SET {', '.join(updates)} WHERE id = ?
            ''', params)
            conn.commit()
            conn.close()
            return True
        conn.close()
        return False
    
    # Plant catalog operations
    def get_plant_catalog(self, difficulty: str = None, light: str = None, search: str = None) -> List[Dict]:
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = 'SELECT * FROM plant_catalog WHERE 1=1'
        params = []
        
        if difficulty:
            query += ' AND difficulty = ?'
            params.append(difficulty)
        if light:
            query += ' AND light_requirement = ?'
            params.append(light)
        if search:
            query += ' AND (name LIKE ? OR name_ru LIKE ?)'
            params.extend([f'%{search}%', f'%{search}%'])
        
        cursor.execute(query, params)
        plants = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return plants
    
    def get_plant_by_id(self, plant_id: int) -> Optional[Dict]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM plant_catalog WHERE id = ?', (plant_id,))
        plant = cursor.fetchone()
        conn.close()
        return dict(plant) if plant else None
    
    # User plants operations
    def add_user_plant(self, user_id: int, plant_id: int, nickname: str = None) -> bool:
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO user_plants (user_id, plant_id, nickname)
                VALUES (?, ?, ?)
            ''', (user_id, plant_id, nickname))
            plant_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            # Create initial tasks
            self.create_plant_tasks(user_id, plant_id)
            return True
        except Exception as e:
            print(f"Error adding plant: {e}")
            return False
    
    def get_user_plants(self, user_id: int) -> List[Dict]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT up.*, pc.name, pc.name_ru, pc.icon, pc.water_frequency
            FROM user_plants up
            JOIN plant_catalog pc ON up.plant_id = pc.id
            WHERE up.user_id = ?
            ORDER BY up.date_added DESC
        ''', (user_id,))
        plants = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return plants
    
    def delete_user_plant(self, user_plant_id: int) -> bool:
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM user_plants WHERE id = ?', (user_plant_id,))
            cursor.execute('DELETE FROM tasks WHERE user_plant_id = ?', (user_plant_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error deleting plant: {e}")
            return False
    
    def update_plant_watered(self, user_plant_id: int):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE user_plants SET last_watered = CURRENT_TIMESTAMP WHERE id = ?
        ''', (user_plant_id,))
        conn.commit()
        conn.close()
    
    def update_plant_fertilized(self, user_plant_id: int):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE user_plants SET last_fertilized = CURRENT_TIMESTAMP WHERE id = ?
        ''', (user_plant_id,))
        conn.commit()
        conn.close()
    
    # Task operations
    def create_plant_tasks(self, user_id: int, user_plant_id: int):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Get plant info
        cursor.execute('''
            SELECT water_frequency, name_ru FROM user_plants up
            JOIN plant_catalog pc ON up.plant_id = pc.id
            WHERE up.id = ?
        ''', (user_plant_id,))
        plant = cursor.fetchone()
        
        if plant:
            water_freq = plant['water_frequency']
            plant_name = plant['name_ru']
            
            # Create watering task
            next_water = datetime.now() + timedelta(days=water_freq)
            cursor.execute('''
                INSERT INTO tasks (user_id, user_plant_id, task_type, description, scheduled_date)
                VALUES (?, ?, 'watering', ?, ?)
            ''', (user_id, user_plant_id, f'Полив {plant_name}', next_water.isoformat()))
            
            # Create fertilizing task (monthly)
            next_fertilize = datetime.now() + timedelta(days=30)
            cursor.execute('''
                INSERT INTO tasks (user_id, user_plant_id, task_type, description, scheduled_date)
                VALUES (?, ?, 'fertilizing', ?, ?)
            ''', (user_id, user_plant_id, f'Удобрение {plant_name}', next_fertilize.isoformat()))
        
        conn.commit()
        conn.close()
    
    def get_tasks(self, user_id: int, completed: bool = False) -> List[Dict]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT t.*, up.nickname, pc.name_ru
            FROM tasks t
            LEFT JOIN user_plants up ON t.user_plant_id = up.id
            LEFT JOIN plant_catalog pc ON up.plant_id = pc.id
            WHERE t.user_id = ? AND t.completed = ?
            ORDER BY t.scheduled_date ASC
        ''', (user_id, completed))
        tasks = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return tasks
    
    def complete_task(self, task_id: int):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Get task info
        cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
        task = cursor.fetchone()
        
        if task:
            cursor.execute('''
                UPDATE tasks SET completed = TRUE, completed_date = CURRENT_TIMESTAMP WHERE id = ?
            ''', (task_id,))
            
            # If it's a watering task, update plant
            if task['task_type'] == 'watering' and task['user_plant_id']:
                self.update_plant_watered(task['user_plant_id'])
                
                # Create next watering task
                self.create_plant_tasks(task['user_id'], task['user_plant_id'])
            
            # If it's a fertilizing task, update plant
            if task['task_type'] == 'fertilizing' and task['user_plant_id']:
                self.update_plant_fertilized(task['user_plant_id'])
                
                # Create next fertilizing task
                self.create_plant_tasks(task['user_id'], task['user_plant_id'])
        
        conn.commit()
        conn.close()
    
    def snooze_task(self, task_id: int, days: int = 1):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE tasks SET scheduled_date = datetime(scheduled_date, '+' || ? || ' days')
            WHERE id = ?
        ''', (days, task_id))
        conn.commit()
        conn.close()
    
    # Tips operations
    def get_tips(self, category: str = None) -> List[Dict]:
        conn = self.get_connection()
        cursor = conn.cursor()
        if category:
            cursor.execute('SELECT * FROM tips WHERE category = ?', (category,))
        else:
            cursor.execute('SELECT * FROM tips')
        tips = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return tips
    
    # Statistics
    def get_user_stats(self, user_id: int) -> Dict:
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Total plants
        cursor.execute('SELECT COUNT(*) as count FROM user_plants WHERE user_id = ?', (user_id,))
        total_plants = cursor.fetchone()['count']
        
        # Plants needing water
        cursor.execute('''
            SELECT COUNT(*) as count FROM user_plants up
            JOIN plant_catalog pc ON up.plant_id = pc.id
            WHERE up.user_id = ? AND 
            (up.last_watered IS NULL OR 
             date(up.last_watered, '+' || pc.water_frequency || ' days') <= date('now'))
        ''', (user_id,))
        needs_water = cursor.fetchone()['count']
        
        # Healthy plants
        cursor.execute('''
            SELECT COUNT(*) as count FROM user_plants 
            WHERE user_id = ? AND health_status = 'healthy'
        ''', (user_id,))
        healthy = cursor.fetchone()['count']
        
        conn.close()
        return {
            'total_plants': total_plants,
            'needs_water': needs_water,
            'healthy': healthy
        }
    
    # Data export/import
    def export_user_data(self, user_id: int) -> str:
        conn = self.get_connection()
        cursor = conn.cursor()
        
        data = {
            'user': dict(cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()),
            'plants': [dict(row) for row in cursor.execute('''
                SELECT up.*, pc.* FROM user_plants up
                JOIN plant_catalog pc ON up.plant_id = pc.id
                WHERE up.user_id = ?
            ''', (user_id,)).fetchall()],
            'tasks': [dict(row) for row in cursor.execute('''
                SELECT * FROM tasks WHERE user_id = ?
            ''', (user_id,)).fetchall()]
        }
        
        conn.close()
        return json.dumps(data, indent=2, default=str)
    
    def clear_user_data(self, user_id: int):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM tasks WHERE user_id = ?', (user_id,))
        cursor.execute('DELETE FROM user_plants WHERE user_id = ?', (user_id,))
        conn.commit()
        conn.close()
