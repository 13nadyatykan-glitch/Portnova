import tkinter as tk
from tkinter import ttk, messagebox
import json
import random

class QuoteGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор случайных цитат")
        self.root.geometry("600x500")
        
        # Загрузка данных из JSON
        self.quotes_data = self.load_quotes()
        self.history = self.load_history()

        # Создание виджетов
        self.create_widgets()
        self.display_quote()
        self.update_history_list()

    def load_quotes(self):
        """Загрузка предопределённых цитат и истории."""
        try:
            with open('quotes.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            # Если файла нет, создаем структуру по умолчанию
            default_data = {
                "predefined_quotes": [
                    {"text": "Единственный способ делать великие дела — любить то, что ты делаешь.", "author": "Стив Джобс", "topic": "Мотивация"},
                    {"text": "Будь тем изменением, которое ты хочешь видеть в мире.", "author": "Махатма Ганди", "topic": "Жизнь"},
                    {"text": "Знание — сила.", "author": "Фрэнсис Бэкон", "topic": "Знания"}
                ],
                "history": []
            }
            with open('quotes.json', 'w', encoding='utf-8') as f:
                json.dump(default_data, f, ensure_ascii=False, indent=4)
            return default_data

    def save_quotes(self):
        """Сохранение данных в JSON."""
        with open('quotes.json', 'w', encoding='utf-8') as f:
            json.dump(self.quotes_data, f, ensure_ascii=False, indent=4)

    def create_widgets(self):
        # Рамка для текущей цитаты
        quote_frame = ttk.LabelFrame(self.root, text="Текущая цитата", padding=10)
        quote_frame.pack(fill="x", padx=10, pady=5)

        self.quote_text_label = ttk.Label(quote_frame, text="", wraplength=400, font=("Arial", 12))
        self.quote_text_label.pack()
        
        self.author_label = ttk.Label(quote_frame, text="", font=("Arial", 10, "italic"))
        self.author_label.pack()
        
        self.topic_label = ttk.Label(quote_frame, text="", font=("Arial", 10))
        self.topic_label.pack()

        # Кнопка генерации
        ttk.Button(self.root, text="Сгенерировать цитату", command=self.generate_quote).pack(pady=10)

        # Фильтрация
        filter_frame = ttk.Frame(self.root)
        filter_frame.pack(fill="x", padx=10)
        
        ttk.Label(filter_frame, text="Фильтр по автору:").grid(row=0, column=0, sticky="w")
        self.author_filter = ttk.Entry(filter_frame)
        self.author_filter.grid(row=0, column=1, sticky="ew", padx=5)
        
        ttk.Label(filter_frame, text="Фильтр по теме:").grid(row=1, column=0, sticky="w")
        self.topic_filter = ttk.Entry(filter_frame)
        self.topic_filter.grid(row=1, column=1, sticky="ew", padx=5)
        
        ttk.Button(filter_frame, text="Применить фильтр", command=self.apply_filter).grid(row=2, column=0, columnspan=2)

        # История
        history_frame = ttk.LabelFrame(self.root, text="История цитат", padding=5)
        history_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.history_listbox = tk.Listbox(history_frame, height=10)
        self.history_listbox.pack(side="left", fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(history_frame, orient="vertical", command=self.history_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        
        self.history_listbox.config(yscrollcommand=scrollbar.set)

    def generate_quote(self):
        """Генерация случайной цитаты из предопределенного списка."""
        if not self.quotes_data["predefined_quotes"]:
            messagebox.showwarning("Ошибка", "Список предопределенных цитат пуст.")
            return

        quote = random.choice(self.quotes_data["predefined_quotes"])
        
        # Отображение на экране
        self.quote_text_label.config(text=f'"{quote["text"]}"')
        self.author_label.config(text=f"Автор: {quote['author']}")
        self.topic_label.config(text=f"Тема: {quote['topic']}")

        # Добавление в историю (без повторов подряд)
        if not self.history or self.history[-1] != quote:
            self.history.append(quote)
            if len(self.history) > 20: # Ограничение истории до 20 элементов
                self.history.pop(0)
            self.update_history_list()
            self.save_quotes() # Сохраняем историю

    def update_history_list(self):
        """Обновление виджета списка истории."""
        self.history_listbox.delete(0, tk.END)
        for i, quote in enumerate(self.history):
            self.history_listbox.insert(tk.END, f"{i+1}. {quote['author']} - {quote['topic']}")

    def apply_filter(self):
        """Фильтрация истории по автору и теме."""
        author = self.author_filter.get().lower()
        topic = self.topic_filter.get().lower()
        
        filtered = []
        
        for quote in self.history:
            author_match = (author == "" or author in quote["author"].lower())
            topic_match = (topic == "" or topic in quote["topic"].lower())
            
            if author_match and topic_match:
                filtered.append(quote)
                
        # Временно заменяем историю для отображения
        temp_history = self.history
        self.history = filtered
        
        self.update_history_list()
        
         # Возвращаем полную историю после обновления (чтобы не сохранять фильтр)
         # Или можно реализовать сохранение отфильтрованного списка, но здесь просто обновляем вид
         self.history = temp_history 

if __name__ == "__main__":
    root = tk.Tk()
    app = QuoteGeneratorApp(root)
    root.mainloop()
