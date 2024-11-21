from src.maigic_nyu.api import (
    add as add,
    divide as divide,
    modulo as modulo,
    multiply as multiply,
    subtract as subtract,
)

def test_api_add() -> None:
    assert add(7, 2) == 9
    
def test_api_subtract() -> None:
    assert subtract(7, 2) == 5
    
def test_api_multiply() -> None:
    assert multiply(7, 2) == 14
    
def test_api_divide() -> None:
    assert divide(7, 2) == 3.5

def test_api_modulo() -> None:
    assert modulo(7, 2) == 1