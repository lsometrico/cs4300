# Control structure correctness tests
import pytest
from src.task3 import sign_check, print_prime, sum_hundred, prime_numbers

# if / elif / else to sign check numbers sign_check 
@pytest.mark.parametrize(
    "number, expected",
    [
        (5, "Positive"),      
        (0.1, "Positive"),    
        (-3, "Negative"),     
        (-0.5, "Negative"),   
        (0, "Number is 0"),   
    ],
)
def test_sign_check(number, expected, capsys):
    sign_check(number)
    assert capsys.readouterr().out.strip() == expected


# helper used by the for loop: prime_numbers
@pytest.mark.parametrize(
    "n, expected",
    [
        (-5, False),  # negative numbers aren't prime
        (0, False),
        (1, False),
        (2, True),    # smallest prime
        (3, True),
        (9, False),   # 3 x 3
        (13, True),
        (25, False),  # 5 x 5
        (29, True),   # 10th prime
    ],
)
def test_prime_numbers(n, expected):
    assert prime_numbers(n) is expected


# print_prime numbers out 
def test_print_prime(capsys):
    print_prime()
    lines = capsys.readouterr().out.split()
    # first 10 primes, printed one per line
    assert lines == ["2", "3", "5", "7", "11", "13", "17", "19", "23", "29"]
    assert len(lines) == 10


# --- while loop: sum_hundred ---
def test_sum_hundred(capsys):
    sum_hundred()
    assert capsys.readouterr().out.strip() == "5050"