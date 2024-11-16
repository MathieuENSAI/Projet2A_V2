import pytest

@pytest.mark.parametrize("a,b,result", [(1, 2, 3), (2, 3, 5), (3, 5, 8)])
def test_addition(a, b, result):
    assert a + b == result
