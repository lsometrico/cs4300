# test task1.py using pytest; should return the output using stdout 
import pytest
from src.task1 import main

def test_hello(capsys):
    main()
    captured = capsys.readoutter()
    assert captured.out == "Hello, world!\n"
