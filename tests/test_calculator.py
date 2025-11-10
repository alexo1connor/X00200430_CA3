import pytest
from src.calculator import add, subtract, multiply, divide

class TestCalculator:
    def test_add(self):
        assert add(2, 3) == 5
        assert add(-1, 1) == 0
        assert add(-1, -1) == -2
    
    def test_subtract(self):
        assert subtract(5, 3) == 2
        assert subtract(0, 0) == 0
        assert subtract(-1, -1) == 0
    
    def test_multiply(self):
        assert multiply(2, 3) == 6
        assert multiply(-1, 1) == -1
        assert multiply(-1, -1) == 1