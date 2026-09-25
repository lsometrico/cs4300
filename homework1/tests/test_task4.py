import pytest 
from src.task4 import calc_discount

#test on discount calculation using only intergers 
def test_discount_int():
    assert calc_discount(59, 30) == 41.3

#test on discount calculation 
def test_discount_float():
    assert calc_discount(46.34, 90.1) == 4.58766

# test mixed types: int price, float discount
def test_discount_int_price_float_discount():
    assert calc_discount(100, 12.5) == pytest.approx(87.5)

# test mixed types: float price, int discount
def test_discount_float_price_int_discount():
    assert calc_discount(59.99, 20) == pytest.approx(47.992)


#test no discount output 
def test_no_discount():
    assert calc_discount(59.99, 0) == 59.99

