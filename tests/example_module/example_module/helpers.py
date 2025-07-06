"""
Example module that will be obfuscated.
"""


def greet(name):
    """Return a greeting message."""
    return f"Hello, {name}!"


def calculate_fibonacci(n):
    """Calculate the nth Fibonacci number."""
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


class Calculator:
    """A simple calculator class."""

    def __init__(self):
        self.memory = 0

    def add(self, x, y):
        """Add two numbers."""
        return x + y

    def multiply(self, x, y):
        """Multiply two numbers."""
        return x * y
