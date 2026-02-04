class Cup():
    def __init__(self):
        self.__content = coffee

    def fill(self, beverage):
        self.content = beverage

    def get_beverage(self):
        return self.content
    
#Create another class
   
class Protein():

    aminoacid_mw = {"A": 10, "B": 20}

    def __init__(self, identifier, sequence):
        self.__identifier = str(identifier)
        self.__sequence = sequence
    
    def get_mw(self):
        return sum([self.aminoacid_mw.get(aa, 0) for aa in self.__sequence])
    
# Create another classe named parent

class Parent: #the parent class does not have ()
    def __init__(self, name):
        self.name = name
    
    def print_name(self): #create a method
        print(f"I am the parent and my name is {self.name}")

class Child(Parent): #the sub class has ()!!!!

    def __init__(self, name, age):
        self.age = age #unique attriubte of the child
        #we can access the super init funciton of the suepr class like this:
        super().__init__(name)

    def print_name(self):
       print(f"I am the child and my name is {self.name}")