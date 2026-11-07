"""search.py - Open Library book search for Book Discovery Companion.

Searches Open Library by title, author or ISBN and returns the book details
the app needs (title, authors, year, subjects, pages and cover).
"""

#ISBN validation with regex, and search by ISBN.
import re
import requests

#add exceptionb classes. later to be raised when a seach for some reacson cant be completed and presumably when a book cant be found. 

#the fields i need to ask open library for. 
FIELDS = "key,title,author_name,first_publish_year,subject,isbn,number_of_pages_median,cover_i"


# ISBN-10: nine digits then a digit or X.  ISBN-13: thirteen digits.
ISBN_10 = re.compile(r"^\d{9}[\dXx]$")
ISBN_13 = re.compile(r"^\d{13}$")

 
# a 4-digit year from 1500 to 2099 that is not part of a longer number.
# (?<!\d) and (?!\d) mean "no digit directly before / after", which also
# works for messy dates like "c1965" and "[1965]" where \b would fail.
YEAR = re.compile(r"(?<!\d)(1[5-9]\d{2}|20\d{2})(?!\d)")

class BookSearchError(Exception):
    """this is raised when a search cant be commpleted"""


class BookNotFound(BookSearchError): 
    """raised whrn a book search returns no books"""

#this should be a function to help clean the input for the isbn
def clean_isbn(text):
    # remove hyphens and spaces: "0-441-17271-7" -> "0441172717"
    return re.sub(r"[\s-]")


def is_valid_isbn(text):
    #check the format only (10 or 13)
    cleaned = clean_isbn(text)
    return bool(ISBN_10.match(cleaned) or ISBN_13.match(cleaned))

def looks_like_isbn(text):
    # mostly digits, hyphens and spaces and 9+ long: the user meant an ISBN
    return bool(re.fullmatch(r"[\d\s-]{9,}[\dXx]?", text))


def extract_year(date_text):
    # "c1965", "March 3, 1965" and "1965-03-01" all give 1965; no year gives None
    match = YEAR.search(str(date_text))
    return int(match.group(1)) if match else None

def clean_text(text):
    # collapse repeated spaces/newlines, then trim stray punctuation at the ends
    text = re.sub(r"\s+", " ", str(text))
    return text.strip(" ,;:/")
 

def search_books(query):
    #Search open library and return as list of books or book dictionaries

    query = query.strip() #strip whatever input (learn more about strip later)
    
    #url = f"https://openlibrary.org/search.json?q={query}&limit=10"
    #response = requests.get(url)
    #print(response.status_code)# temporary check. 

    if not query:
        raise BookSearchError("Please enter a title, author or ISBN")

     # normal search by default, switch to an ISBN search if it looks like one
    params = {"q": query, "limit": 10, "fields": FIELDS}
    if looks_like_isbn(query):
        if not is_valid_isbn(query):
            raise BookSearchError("That doesn't look like a valid ISBN (10 or 13 digits).")
        params = {"isbn": clean_isbn(query), "limit": 10, "fields": FIELDS}
    try:
        response = requests.get(
            "https://openlibrary.org/search.json",
            # params={"q": query, "limit": 10},
            # timeout=10,
            params = params,
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

         # use first_publish_year if present; otherwise dig the earliest year
        # out of the messy publish_date strings
        year = doc.get("first_publish_year")
        if year is None:
            found = [extract_year(d) for d in doc.get("publish_date", [])]
            found = [y for y in found if y]
            year = min(found) if found else "N/A"

            
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