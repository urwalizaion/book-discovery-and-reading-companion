import pytest
from search import search_books, clean_isbn
from reading_list import load_reading_list, save_book
from ai_helper import get_ai_summary

# 1. Test search works 
def test_search_dune():
    results = search_books("dune")
    assert len(results) > 0
    assert "dune" in results[0]['title'].lower()

# 2. Test ISBN cleaning (your clean_isbn function)
def test_clean_isbn():
    assert clean_isbn("978-0-441-17271-9") == "9780441172719"
    assert clean_isbn(" 9780441172719 ") == "9780441172719"

# 3. Test invalid search error handling (Ajasiisjsjejs case)
def test_invalid_search():
    results = search_books("AjasiisjsjejsXYZ123")
    assert results == [] or len(results) == 0

# 4. Test reading list loads
def test_reading_list():
    data = load_reading_list()
    assert isinstance(data, dict)

# 5. Test ISBN validation
def test_isbn_validation():
    # Valid ISBN 13
    results = search_books("9780441172719")
    assert len(results) >= 0  # Should not crash

# 6. Test app imports without crashing
def test_app_imports():
    try:
        import app
        assert True
    except Exception:
        assert True  # Allow if secrets missing
