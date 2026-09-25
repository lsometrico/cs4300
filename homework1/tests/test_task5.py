import pytest
from src.task5 import fav_books, first_three, student_database, get_student_id


# book list test where each entry is a title, author pair that are both strings 
def test_fav_books_structure():
    for entry in fav_books:
        assert isinstance(entry, tuple)
        assert len(entry) == 2
        title, author = entry
        assert isinstance(title, str)
        assert isinstance(author, str)

# test if it returns the first three books and also that they match the first three entries 
def test_first_three_returns_three_books():
    result = first_three()
    assert len(result) == 3
    assert result == fav_books[:3]

def test_first_three_matches_first_entries():
    assert first_three()[0] == fav_books[0]
    assert first_three()[2] == fav_books[2]


# student database tests
def test_student_database_is_dict():
    assert isinstance(student_database, dict)

def test_get_student_id_known_name():
    assert get_student_id("Porter Robinson") == "S01092019"
    assert get_student_id("Sonny Moore") == "S347678566"

def test_get_student_id_unknown_name():
    assert get_student_id("Nobody Here") is None

def test_student_ids_are_unique():
    ids = list(student_database.values())
    assert len(ids) == len(set(ids))