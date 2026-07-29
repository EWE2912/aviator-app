import sqlite3
import numpy as np
from datetime import datetime

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

class DatabaseManager:
    def __init__(self, db_name="aviator_data.db"):
        self.db_name = db_name
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    multiplier REAL NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

    def add_multiplier(self, value):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO history (multiplier, timestamp) VALUES (?, ?)",
                (float(value), datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            )
            conn.commit()

    def get_all_multipliers(self, limit=100):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT multiplier FROM history ORDER BY id DESC LIMIT ?", (limit,))
            rows = cursor.fetchall()
            return [r[0] for r in reversed(rows)]

class MultiplierAnalyzer:
    @staticmethod
    def calculate_stats(data):
        if not data:
            return {"count": 0, "mean": 0.0, "median": 0.0, "max": 0.0, "min": 0.0, "std_dev": 0.0}
        arr = np.array(data)
        return {
            "count": len(arr),
            "mean": float(np.mean(arr)),
            "median": float(np.median(arr)),
            "max": float(np.max(arr)),
            "min": float(np.min(arr)),
            "std_dev": float(np.std(arr))
        }

class AviatorDashboard(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=10, spacing=8, **kwargs)
        self.db = DatabaseManager()

        self.overlay_label = Label(text="[b]AVIATOR ANALYZER[/b]", markup=True, halign='center')
        self.add_widget(self.overlay_label)

        input_layout = BoxLayout(size_hint_y=None, height=40, spacing=8)
        self.input_field = TextInput(hint_text="Ex: 1.85", input_filter='float', multiline=False)
        btn_add = Button(text="Adicionar", size_hint_x=0.3)
        btn_add.bind(on_press=self.add_value)
        input_layout.add_widget(self.input_field)
        input_layout.add_widget(btn_add)
        self.add_widget(input_layout)

        self.stats_label = Label(text="Sem histórico", markup=True)
        self.add_widget(self.stats_label)

    def add_value(self, instance):
        val = self.input_field.text.strip()
        if val:
            try:
                num = float(val.replace(',', '.'))
                self.db.add_multiplier(num)
                self.input_field.text = ""
                self.update_ui()
            except ValueError:
                pass

    def update_ui(self):
        data = self.db.get_all_multipliers()
        if not data:
            return
        stats = MultiplierAnalyzer.calculate_stats(data)
        self.stats_label.text = f"Média: {stats['mean']:.2f}x | Total: {stats['count']}"

class AviatorApp(App):
    def build(self):
        return AviatorDashboard()

if __name__ == "__main__":
    AviatorApp().run()
