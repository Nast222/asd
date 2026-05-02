import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

# --- Настройки ---
DATA_FILE = "books.json"

# --- Функции работы с данными ---
def load_books():
    """Загружает книги из JSON-файла."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_books(books):
    """Сохраняет список книг в JSON-файл."""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(books, f, ensure_ascii=False, indent=4)

# --- Функции логики приложения ---
def add_book():
    """Добавляет новую книгу в список после проверки ввода."""
    title = title_entry.get().strip()
    author = author_entry.get().strip()
    genre = genre_entry.get().strip()
    pages = pages_entry.get().strip()

    # Валидация
    if not title or not author or not genre or not pages:
        messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
        return
    if not pages.isdigit():
        messagebox.showerror("Ошибка", "Количество страниц должно быть числом!")
        return

    book = {
        "title": title,
        "author": author,
        "genre": genre,
        "pages": int(pages)
    }
    books.append(book)
    save_books(books)
    update_treeview()
    clear_entries()

def clear_entries():
    """Очищает поля ввода."""
    title_entry.delete(0, tk.END)
    author_entry.delete(0, tk.END)
    genre_entry.delete(0, tk.END)
    pages_entry.delete(0, tk.END)

def update_treeview(filter_genre=None, filter_pages=None):
    """Обновляет таблицу книг с учетом фильтров."""
    for i in tree.get_children():
        tree.delete(i)
    
    for book in books:
        # Фильтрация по жанру
        if filter_genre and book['genre'].lower() != filter_genre.lower():
            continue
        # Фильтрация по количеству страниц (больше указанного)
        if filter_pages is not None and book['pages'] <= filter_pages:
            continue
        
        tree.insert("", tk.END, values=(book['title'], book['author'], book['genre'], book['pages']))

def on_filter():
    """Применяет фильтры при нажатии кнопки."""
    genre = genre_filter_var.get()
    try:
        pages = int(pages_filter_var.get()) if pages_filter_var.get() else None
    except ValueError:
        messagebox.showerror("Ошибка", "В фильтре страниц должно быть число или пустое поле!")
        return
    
    update_treeview(filter_genre=genre, filter_pages=pages)

# --- Инициализация данных ---
books = load_books()

# --- Создание окна ---
root = tk.Tk()
root.title("Book Tracker")
root.geometry("800x500")
root.resizable(False, False)
root.configure(bg='#f0f0f0')

# --- Стиль для Treeview (таблицы) ---
style = ttk.Style(root)
style.theme_use('clam')
style.configure("Treeview.Heading", font=('Arial', 10, 'bold'), background='#e0e0e0')
style.configure("Treeview", rowheight=25)

# --- Вкладка 1: Добавление книги (Notebook) ---
notebook = ttk.Notebook(root)
notebook.pack(pady=10, expand=True, fill='both')

tab_add = ttk.Frame(notebook)
tab_filter = ttk.Frame(notebook)
notebook.add(tab_add, text='Добавить книгу')
notebook.add(tab_filter, text='Фильтр')

# --- Вкладка "Добавить книгу" ---
frame_inputs = tk.LabelFrame(tab_add, text="Данные книги", bg='#f0f0f0')
frame_inputs.pack(pady=10, padx=10, fill='x')

tk.Label(frame_inputs, text="Название:", bg='#f0f0f0').grid(row=0, column=0, padx=5, pady=5, sticky='e')
tk.Label(frame_inputs, text="Автор:", bg='#f0f0f0').grid(row=1, column=0, padx=5, pady=5, sticky='e')
tk.Label(frame_inputs, text="Жанр:", bg='#f0f0f0').grid(row=2, column=0, padx=5, pady=5, sticky='e')
tk.Label(frame_inputs, text="Страниц:", bg='#f0f0f0').grid(row=3, column=0, padx=5, pady=5, sticky='e')

title_entry = tk.Entry(frame_inputs)
author_entry = tk.Entry(frame_entry)
genre_entry = tk.Entry(frame_inputs)
pages_entry = tk.Entry(frame_inputs)

title_entry.grid(row=0, column=1, padx=5, pady=5)
author_entry.grid(row=1, column=1, padx=5, pady=5)
genre_entry.grid(row=2, column=1, padx=5, pady=5)
pages_entry.grid(row=3, column=1, padx=5, pady=5)

btn_add = tk.Button(tab_add, text="Добавить книгу", command=add_book)
btn_add.pack(pady=5)


# --- Вкладка "Фильтр" ---
frame_filters = tk.LabelFrame(tab_filter, text="Фильтры", bg='#f0f0f0')
frame_filters.pack(pady=10, padx=10, fill='x')

tk.Label(frame_filters, text="Жанр:", bg='#f0f0f0').grid(row=0, column=0, padx=5, pady=5)
tk.Label(frame_filters, text="Страниц >", bg='#f0f0f0').grid(row=1, column=0, padx=5, pady=5)

genre_filter_var = tk.StringVar()
pages_filter_var = tk.StringVar()

ent_genre_filter = tk.Entry(frame_filters, textvariable=genre_filter_var)
ent_pages_filter = tk.Entry(frame_filters, textvariable=pages_filter_var)
ent_genre_filter.grid(row=0, column=1, padx=5, pady=5)
ent_pages_filter.grid(row=1, column=1, padx=5, pady=5)

btn_filter = tk.Button(tab_filter, text="Применить фильтр", command=on_filter)
btn_filter.pack(pady=5)


# --- Таблица книг (Treeview) ---
frame_tree = tk.Frame(root)
frame_tree.pack(pady=10)

columns = ('title', 'author', 'genre', 'pages')
tree = ttk.Treeview(frame_tree, columns=columns, show='headings', height=15)
tree.heading('title', text='Название')
tree.heading('author', text='Автор')
tree.heading('genre', text='Жанр')
tree.heading('pages', text='Страниц')
tree.column('title', width=250)
tree.column('author', width=200)
tree.column('genre', width=150)
tree.column('pages', width=80)
tree.pack()


# Запуск приложения и первоначальная загрузка данных
update_treeview()
root.mainloop()
