class Calculator:

    def __init__(self, a, b):
        self.a = a
        self.b = b

        print("Constructor Called")
        print(id(self))

        # Calling a function from the constructor
        self.add()

    def add(self):
        print("Addition =", self.a + self.b)


calc = Calculator(10, 20)

print(id(calc))