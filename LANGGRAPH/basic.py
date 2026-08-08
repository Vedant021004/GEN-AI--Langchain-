# # x = print
# # x("hello")

# class Classic:
        
#     def __init__(self):
#         print("i'm printed by init without calling ")
#     def sam(self):
#         print("i'm second")

#     def sum(self):
#         print("i'm third")   

# s1 = Classic()
# s1.sam()
# s1.sum()

# class Student:
#     pass

# s1 = Student()
# s1.age = 21
# s1.name = "vedant kapil"
# s1.job = "in malad neso soft"

# print(s1.age)
# print(s1.name)
# print(s1.job)

# class Student:
#     def obj(self,name,age):
#         self.name = name
#         self.age = age
        
#         print(name,age)
    
# s1 = Student()    
# s1.obj("vedant",21)


# class Car:
#     def BMW(self,price, brand ,colour):
#         self.name = price,
#         self.brand = brand,
#         self.colour = colour
#         print("heyyyy",price,brand,colour)

#     def AUDI(self,price, brand ,colour):
#         self.name = price,
#         self.brand = brand,
#         self.colour = colour
#         print("heyyyy",price,brand,colour)


#     def MERCIDES(self,price, brand ,colour):
#         self.name = price,
#         self.brand = brand,
#         self.colour = colour                
#         print("heyyyy",price,brand,colour)


# s1 = Car()
# s1.BMW(100000,"BMW","BLACK")
# s1.AUDI(20000,"AUDI","NEO")
# s1.MERCIDES(432940,"MERCIDES","WHITE")


# class Student:
#     pass

# print(Student)
# print(type(Student))

# x = Student

# print(x)
# print(type(x))        




class Student:
    def __init__(self):
        print("i'm first")
        

    def cllass(self):
        print("i'm second")

    def mwaah(self):
        print("i'm third")    

obj = Student() 
obj.cllass()
obj.mwaah()



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


# Important for the langgraph

class Calculator:

    def __init__(self, a, b):
        self.a = a
        self.b = b


def add(calc: Calculator):
    print(calc.a + calc.b)


c1 = Calculator(10, 20)

add(c1)