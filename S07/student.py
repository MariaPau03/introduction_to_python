class   Student:
    def __init__(self, name, surname, nie): #self refers to the instance itself of that class
        # self, name, surname, nie are the atributes in the initialization function
        self.name = name #create an attribute and initialize it to none
        self.surname = surname #second attribute
        self.nie = nie #third atribute
        self.subjects = [] #Initialize it as an empty list, now subjects is an attribute
    

    def add_subject(self, subject):
        self.subjects.append(subject)

    #method creation, is a method. because it contains the self, if not would be a normal funciton:
    def get_nie(self):
        return self.nie #return the attribute nie

        
