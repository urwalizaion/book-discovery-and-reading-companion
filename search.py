"""search.py - Open Library book search for Book Discovery Companion.

Searches Open Library by title, author or ISBN and returns the book details
the app needs (title, authors, year, subjects, pages and cover).
"""
import requests

def search_books(query):
    #Search open library and return as list of books
    url = f"https://openlibrary.org/search.json?q={query}&limit=10"
    response = requests.get(url)
    print(response.status_code)
    return []



if __name__ == "__main__":
    print(search_books("dune"))