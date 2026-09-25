# Implement pytest to test case for each data type, expected outcomes (int, booleans, floating point etc)
import pytest
from src.task2 import interger_sum, float_point_mult, string, boolean

# interger addition tests that cover positives, larger positives, negatives, zero, mixed sign and negatives
@pytest.mark.parametrize(
    "a, b, expected",
    [
        (5, 9, 14),
        (420, 69, 489),
        (0, 9, 9),
        (-23, 67, 44),
        (-999, -67, -1066),
    ],
)
def test_sum(a, b, expected):
    assert interger_sum(a, b) == expected

# similar tests as above but using floating point multiplication 
@pytest.mark.parametrize(
    "a, b, expected",
    [
        (5.93, 9.23, 54.7339),
        (9.0, 5.322, 47.898),
        (0, 5575.234, 0),
        (-5.93, -9.23, 54.7339),
    ],
)
def test_multiplication(a, b, expected):
    assert float_point_mult(a, b) == pytest.approx(expected)

# check string() returns a value for a non-empty string 
@pytest.mark.parametrize(
    "text",
    [
        "Pain, agony and suffering\n",
    ],
)
def test_string(text):
    assert string(text)

# check that the boolean value matches the case 
@pytest.mark.parametrize(
    "value, expected",
    [
        (5, True),
    ],
)
def test_boolean(value, expected):
    assert boolean(value) == expected