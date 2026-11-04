import json
import os

# File for saving books
FILE_NAME = "reading_list.json"

# My reading list
books = []


# Load saved books
def load_books():
    global books

    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            books = json.load(file)


# Save books
def save_books():
    with open(FILE_NAME, "w") as file:
        json.dump(books, file, indent=4)


# Add a new book
def add_book():

    title = input("Enter book title: ")
    author = input("Enter author name: ")

    book = {
        "Title": title,
        "Author": author,
        "Status": "Want to Read"
    }

    books.append(book)

    save_books()

    print("Book added successfully!")


# Display all books
def view_books():

    print("\nMY READING LIST")

    if len(books) == 0:
        print("Your reading list is empty.")

    else:
        for number, book in enumerate(books, start=1):

            print("\nBook:", number)
            print("Title:", book.get("Title", "Not available"))
            print("Author:", book.get("Author", "Not available"))
            print("Status:", book.get("Status", "Not available"))


# Main program
load_books()

while True:

    print("\n===== BOOK READING COMPANION =====")
    print("1. Add a book")
    print("2. View my books")
    print("3. Exit")

    choice = input("Choose an option: ")

    if choice == "1":
        add_book()

    elif choice == "2":
        view_books()

    elif choice == "3":
        print("Thank you for using my Reading Companion!")
        break

    else:
        print("Invalid choice. Try again.")