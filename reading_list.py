import json
import os

FILE = "data/reading_list.json"

def load_list():
    if not os.path.exists(FILE):
        return {"want_to_read": [], "reading": [], "finished": []}
    with open(FILE, 'r') as f:
        return json.load(f)

def save_list(data):
    os.makedirs("data", exist_ok=True)
    with open(FILE, 'w') as f:
        json.dump(data, f, indent=2)

def add_book(book, status="want_to_read"):
    data = load_list()
    # avoid duplicate
    if not any(b['title'] == book['title'] for b in data[status]):
        data[status].append(book)
        save_list(data)

def move_book(title, from_status, to_status):
    data = load_list()
    book_to_move = None
    for b in data[from_status]:
        if b['title'] == title:
            book_to_move = b
            break
    if book_to_move:
        data[from_status] = [b for b in data[from_status] if b['title'] != title]
        data[to_status].append(book_to_move)
        save_list(data)

def delete_book(title, status):
    data = load_list()
    data[status] = [b for b in data[status] if b['title'] != title]
    save_list(data)