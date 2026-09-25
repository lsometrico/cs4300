import pytest
from src.task7 import stats_summary, dot_product


# summary_stats tests
def test_summary_stats_basic():
    stats = stats_summary([2, 4, 4, 4, 5, 5, 7, 9])
    assert stats["mean"] == pytest.approx(5.0)
    assert stats["median"] == pytest.approx(4.5)
    assert stats["std dev"] == pytest.approx(2.0)

def test_summary_stats_single_value():
    # mean/median of one number is itself, and std is 0 (no spread)
    stats = stats_summary([7])
    assert stats["mean"] == pytest.approx(7.0)
    assert stats["median"] == pytest.approx(7.0)
    assert stats["std dev"] == pytest.approx(0.0)


# dot product tests
def test_dot_product_basic():
    assert dot_product([1, 2, 3], [4, 5, 6]) == 32.0

def test_dot_product_with_zeros():
    assert dot_product([0, 0, 0], [1, 2, 3]) == 0.0

def test_dot_product_negative_values():
    assert dot_product([-1, 2, -3], [4, -5, 6]) == pytest.approx(-32.0)