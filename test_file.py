# Sample Python script for testing
"""Hello."""


def sample_function(param: int) -> None:
    """Hello."""
    if param is None:
        print("Parameter is None")
    elif param == 0:
        print("Parameter is zero")
    else:
        print(f"Parameter is {param}")


sample_function(0)


# Here are some style issues:
import numpy as np


class MyClass:
    def __init__(self):
        self.value = 42

    def print_value(self):
        print(f"Value: {self.value}")


# Unused variable warning
test_value = 10
sample_function(test_value)
