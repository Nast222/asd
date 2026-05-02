import tkinter as tk
from tkinter import ttk, messagebox
import json
import random
import os

# --- Настройки ---
DATA_FILE = "quotes.json"

# --- Предопределенный список цитат (Шаг 1) ---
PREDEFINED_QUOTES = [
    {"text": "Быть или не быть, вот в чём вопрос.", "author": "Уильям Шекспир", "topic": "Философия"},
    {"text": "Я мыслю, следовательно, я существую.", "author": "Рене Декарт", "topic": "Философия"},
    {"text": "Единственный способ делать великие дела — любить то, что ты делаешь.", "author": "Стив Джобс", "topic": "Мотивация"},
    {"text": "Величайшая слава не в том, чтобы никогда не ошибаться, а в том, чтобы уметь подняться каждый раз, когда падаешь.", "author": "Конфуций", "topic": "Мотивация"},
    {"text": "Две вещи бесконечны: вселенная и человеческая глупость; и я не уверен насчёт вселенной.", "author": "Альберт Эйнштейн", "topic": "Юмор"},
]

# --- Функции работы с данными ---
def load_quotes():
    """Загружает историю цитат из JSON-файла."""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []

def save_quotes(quotes):
    """Сохраняет историю цитат в JSON-файл."""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(quotes, f, ensure_ascii=False, indent=4)

# --- Функции логики приложения ---
def generate_quote():
    """Выбирает случайную цитату из общего пула (предопределенные + история)."""
    all_quotes = PREDEFINED_QUOTES + history_quotes
    if not all_quotes:
        messagebox.showinfo("Информация", "Список цитат пуст. Добавьте свои!")
        return

    quote = random.choice(all_quotes)
    
    # Отображение цитаты
    quote_text_label.config(text=f"«{quote['text']}»")
    author_label.config(text=f"— {quote['author']}")
    
    # Добавление в историю, если её там ещё нет
    if quote not in history_quotes:
        history_quotes.append(quote)
        save_quotes(history_quotes)
        update_history_list()

def add_custom_quote():
    """Добавляет новую цитату, введенную пользователем."""
    text = custom_text_entry.get("1.0", tk.END).strip()
    author = custom_author_entry.get().strip()
    
    # Валидация (Шаг 6)
    if not text or not author:
        messagebox.showerror("Ошибка", "Поля 'Текст' и 'Автор' обязательны для заполнения!")
        return

    new_quote = {"text": text, "author": author, "topic": "Пользовательская"}
    
    history_quotes.append(new_quote)
    save_quotes(history_quotes)
    
    update_history_list()
    
    # Очистка полей
    custom_text_entry.delete("1.0", tk.END)
    custom_author_entry.delete(0, tk.END)
    
    messagebox.showinfo("Успех", "Цитата добавлена в историю!")

def update_history_list(filter_author=None, filter_topic=None):
    """Обновляет список истории с учетом фильтров."""
    history_listbox.delete(0, tk.END)
    
    for quote in history_quotes:
        # Фильтрация по автору (Шаг 5)
        if filter_author and quote['author'].lower() != filter_author.lower():
            continue
        # Фильтрация по теме (Шаг 5)
        if filter_topic and quote['topic'].lower() != filter_topic.lower():
            continue
        
        history_listbox.insert(tk.END, f"{quote['author']}: «{quote['text']}»")

def on_filter():
    """Применяет фильтры при нажатии кнопки."""
    author = author_filter_var.get()
    topic = topic_filter_var.get()
    
    update_history_list(filter_author=author, filter_topic=topic)


# --- Инициализация данных ---
history_quotes = load_quotes()

# --- Создание окна ---
root = tk.Tk()
root.title("Random Quote Generator")
root.geometry("700x600")
root.resizable(False, False)
root.configure(bg='#f8f9fa')

# --- Основной фрейм для генерации ---
main_frame = tk.Frame(root, bg='#f8f9fa')
main_frame.Вот пошаговая инструкция и готовый код для создания приложения **Random Quote Generator** на Python с использованием библиотеки `tkinter`.

### 1. Структура проекта

Создайте папку проекта, например, `QuoteGenerator`. Внутри неё будут:
*   `quote_generator.py` — основной файл программы.
*   `quotes.json` — файл для хранения истории.
*   `README.md` — описание проекта.

### 2. Код приложения (quote_generator.py)

Этот код реализует все требования: генерацию, историю, фильтрацию, валидацию и работу с JSON.
