import pytest


def test_addition() -> None:
    assert 2 + 2 == 4

def test_subtraction() -> None:
    assert 5 - 3 == 2

def test_multiplication() -> None:
    assert 3 * 3 == 9

def test_division() -> None:
    assert 8 / 2 == 4

def test_string_equality() -> None:
    assert "hello".upper() == "HELLO"

def test_list_append() -> None:
    lst = [1, 2, 3]
    lst.append(4)
    assert lst == [1, 2, 3, 4]

def test_dictionary_key() -> None:
    d = {"name": "Alice", "age": 30}
    assert "name" in d
    assert d["name"] == "Alice"

def test_raise_error() -> None:
    with pytest.raises(ZeroDivisionError):
        1 / 0
