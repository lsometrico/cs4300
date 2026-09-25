import pytest
from src.task6 import read_file_count, default_file


# reading task6_read_me.txt with default & explicit argument 
@pytest.mark.parametrize(
    "filename",
    [
        None,         
        default_file,  
    ],
)
def test_word_count_of_default_file(filename):
    if filename is None:
        assert read_file_count() == 127
    else:
        assert read_file_count(filename) == 127


# edge cases with temp files 
@pytest.mark.parametrize(
    "content, expected",
    [
        ("one two three four", 4),                   
        ("one two\nthree\nfour five six", 6),          
        ("", 0),                                       
        ("word1     word2\t\tword3", 3),              
    ],
)
def test_word_count(tmp_path, content, expected):
    f = tmp_path / "sample.txt"
    f.write_text(content)
    assert read_file_count(f) == expected