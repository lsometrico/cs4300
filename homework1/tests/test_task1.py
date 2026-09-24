# test task1.py using pytest; should return the output using stdout 
import pytest
from src.task1 import hello_world

def test_hello(capsys):
    hello_world()
    captured = capsys.readoutter()
    assert captured.out == "Hello, world!\n"

