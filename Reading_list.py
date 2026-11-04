import json
import os

# File for saving books
FILE_NAME = "reading_list.json"

# My reading list
books = []

READING_STATUSES = ["Want to Read", "Reading", "Finished"]


# Load saved books
def load_books():
    global books

    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            books = json.load(file)


# Save books
def save_books():
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        json.dump(books, file, indent=4)


# Display one book
def display_book(number, book):
    print(f"\nBook: {number}")
    print("Title:", book.get("Title", "Not available"))
    print("Author:", book.get("Author", "Not available"))
    print("Status:", book.get("Status", "Not available"))


# Display all books
def view_books():
    print("\nMY READING LIST")

    if not books:
        print("Your reading list is empty.")
        return

    for number, book in enumerate(books, start=1):
        display_book(number, book)


# Ask the user to choose a book by its displayed number
def choose_book():
    if not books:
        print("Your reading list is empty.")
        return None

    view_books()
    choice = input("Enter the book number (or press Enter to cancel): ").strip()

    if not choice:
        print("Action cancelled.")
        return None

    try:
        index = int(choice) - 1
    except ValueError:
        print("Please enter a valid number.")
        return None

    if index < 0 or index >= len(books):
        print("That book number is not in the list.")
        return None

    return index


# Add a new book
def add_book():
    title = input("Enter book title: ").strip()
    author = input("Enter author name: ").strip()

    if not title or not author:
        print("Title and author are required. Book not added.")
        return

    book = {
        "Title": title,
        "Author": author,
        "Status": "Want to Read",
    }

    books.append(book)
    save_books()
    print("Book added successfully!")


# Edit a book's title or author
def edit_book():
    index = choose_book()
    if index is None:
        return

    book = books[index]
    print("Press Enter to keep the current value.")
    title = input(f"Title [{book.get('Title', '')}]: ").strip()
    author = input(f"Author [{book.get('Author', '')}]: ").strip()

    if title:
        book["Title"] = title
    if author:
        book["Author"] = author

    save_books()
    print("Book updated successfully!")


# Delete a book
def delete_book():
    index = choose_book()
    if index is None:
        return

    book = books[index]
    confirmation = input(
        f"Delete '{book.get('Title', 'Untitled')}'? (y/n): "
    ).strip().lower()

    if confirmation == "y":
        books.pop(index)
        save_books()
        print("Book deleted successfully!")
    else:
        print("Deletion cancelled.")


# Search books by title or author
def search_books():
    query = input("Search by title or author: ").strip().casefold()

    if not query:
        print("Enter a title or author to search for.")
        return

    matches = [
        (number, book)
        for number, book in enumerate(books, start=1)
        if query in book.get("Title", "").casefold()
        or query in book.get("Author", "").casefold()
    ]

    if not matches:
        print("No matching books found.")
        return

    print("\nSEARCH RESULTS")
    for number, book in matches:
        display_book(number, book)


# Change a book's reading status
def change_status():
    index = choose_book()
    if index is None:
        return

    print("\nChoose a status:")
    for number, status in enumerate(READING_STATUSES, start=1):
        print(f"{number}. {status}")

    choice = input("Choose a status number: ").strip()
    try:
        status_index = int(choice) - 1
    except ValueError:
        print("Please enter a valid status number.")
        return

    if status_index < 0 or status_index >= len(READING_STATUSES):
        print("That status number is not available.")
        return

    books[index]["Status"] = READING_STATUSES[status_index]
    save_books()
    print("Book status updated successfully!")


# Main program
load_books()

while True:
    print("\n===== BOOK READING COMPANION =====")
    print("1. Add a book")
    print("2. View my books")
    print("3. Edit a book")
    print("4. Delete a book")
    print("5. Search the list")
    print("6. Change a book's status")
    print("7. Exit")

    choice = input("Choose an option: ").strip()

    if choice == "1":
        add_book()
    elif choice == "2":
        view_books()
    elif choice == "3":
        edit_book()
    elif choice == "4":
        delete_book()
    elif choice == "5":
        search_books()
    elif choice == "6":
        change_status()
    elif choice == "7":
        print("Thank you for using my Reading Companion!")
        break
    else:
        print("Invalid choice. Try again.")
