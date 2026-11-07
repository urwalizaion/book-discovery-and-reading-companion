"""search.py - Open Library book search for Book Discovery Companion.

Searches Open Library by title, author or ISBN and returns the book details
the app needs (title, authors, year, subjects, pages and cover).
"""
import requests

#add exceptionb classes. later to be raised when a seach for some reacson cant be completed and presumably when a book cant be found. 

#the fields i need to ask open library for. 
FIELDS = "key,title,author_name,first_publish_year,subject,isbn,number_of_pages_median,cover_i"


class BookSearchError(Exception):
    """this is raised when a search cant be commpleted"""


class BookNotFound(BookSearchError): 
    """raised whrn a book search returns no books"""



def search_books(query):
    #Search open library and return as list of books or book dictionaries

    query = query.strip() #strip whatever input (learn more about strip later)
    
    #url = f"https://openlibrary.org/search.json?q={query}&limit=10"
    #response = requests.get(url)
    #print(response.status_code)# temporary check. 

    if not query:
        raise BookSearchError("Please enter a title, author or ISBN")


    try:
        response = requests.get(
            "https://openlibrary.org/search.json",
            params={"q": query, "limit": 10},
            timeout=10,
        )



        response.raise_for_status()
        data = response.json()

    except requests.exceptions.Timeout:
        raise BookSearchError("Your seach took too long, please try again. ")
    except requests.exceptions.ConnectionError:
        raise BookSearchError("couldn't connect, please check that you have an internet connection")
    except (requests.exceptions.RequestException, ValueError):
        raise BookSearchError("Open Library gave an unexpected reply, try again later")


    docs = data.get("docs", [])
    if not docs:
        raise BookNotFound (f"There we no books found for '{query}'. ")
    # print(len(data.get("docs", [])))
    # return []

    books = []
    #for doc in data.get("docs",[]):
    for doc in docs:
        cover_id = doc.get("cover_i")
        books.append({
            "title": doc.get("title", "No Title"),
            "author": ", ".join(doc.get("author_name", ["Unkown"])),
            "year": doc.get("first_publish_year", "N/A"),
            "cover_id": doc.get("cover_i"),
             # None when the book has no cover, so the app can check for it
            "cover_url": f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg" if cover_id else None,
            "subjects": doc.get("subject", [])[:5],
            "pages": doc.get("number_of_pages_median", "N/A"),
            "isbn": (doc.get("isbn") or [None])[0],

        })

    return books



if __name__ == "__main__":
   # print(search_books("flrresdf"))
    for test in ["friend","flrissds", " "]:
        try:
           print(test, "-->", len(search_books(test)), "books")
        except BookSearchError as err:
            print(repr(test), "-->", err)


    
    # look at one full result to check every key is there
print(search_books("dune")[0])