from helpers import Calculator, calculate_fibonacci, greet

if __name__ == "__main__":
    print("Hello World!")
    print("This is a test")
    print(greet("World"))
    print(calculate_fibonacci(10))
    calculator = Calculator()
    print(calculator.add(1, 2))
    print(calculator.multiply(2, 3))
