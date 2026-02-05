class Subject:

    def __init__(self, name, hours, teacher):

        self.name = name
        self.hours = hours
        self.teacher = teacher

        self.students = set()

    def add_student(self, student): #method that keeps adding students to my set
        self.students.add(student)

    def __contains__(self, student):
        return student in self.students #I'm checking wether if student is in the set

    def __getitem__(self, key):
        return sorted(list(self.students))[key] #convert the set into a list and get whatever the element from the set students
        #sets has no indexes, lists yes

    def __iter__(self):
        for student in sorted(list(self.students)):
            yield student #iterate over an object


class Person:

    def __init__(self, name, surname, NIE, birth_date=None):

        self.name = name
        self.surname = surname
        self.NIE = NIE
        self.birth_date = birth_date

    #Added this part!
    def __str__(self):
        return "I am a Person object instance. My name is %s %s and my NIE is %s" %(self.name, self.surname, self.NIE)

    def __repr__(self):
        return f"Person({self.name.__repr__()}, {self.surname!r}, {self.NIE!r})"
    #just put the class which is Person and the attributes

   
    def __eq__(self, other_person):
        return self.NIE == other_person.NIE


    def __lt__(self, other):
        return self.surname < other.surname

    def __le__(self, other):
        return self.surname <= other.surname

    def __gt__(self, other):
        return self.surname > other.surname

    def __ge__(self, other):
        return self.surname >= other.surname
    
    def __hash__(self):
        return self.NIE.__hash__()
    
    def __len__(self):
        return len(self.surname)
    
    def __add__(self, other):
        return Person(self.name + other.name, self.surname, self.NIE)

class Teacher(Person):

    def __init__(self, name, surname, NIE, birth_date, salary):

        self.salary = salary
        super().__init__(name=name,
                         surname=surname,
                         NIE=NIE,
                         birth_date=birth_date)


class Student(Person):
    pass

#Here we have ≠ instances of class student
student_instance1 = Student(name="Pere",
                            surname="Anton",
                            birth_date="1/1/1990",
                            NIE="u5241")

student_instance2 = Student(name="Pere",
                            surname="Anton",
                            birth_date="1/1/1990",
                            NIE="u5241")

student_instance3 = Student("Nuria", "Gonzalez", "u22312", "20/10/1992")
student_instance4 = Student("Toni", "Bonet", "u22312", "20/1071992")

my_student_list = [student_instance1,
                   student_instance2,
                   student_instance3,
                   student_instance4]

teacher_instance = Teacher(name="Xavi", surname="Jalencas", NIE="u1234",
                          birth_date="1/1/1980", salary=100)

PYT = Subject(name="PYT", hours=125, teacher=teacher_instance) #create a subject


PYT.add_student(student_instance1)
PYT.add_student(student_instance2)
PYT.add_student(student_instance3)
PYT.add_student(student_instance4)
PYT.add_student(student_instance1)


