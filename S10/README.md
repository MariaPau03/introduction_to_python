# S09 exercise

1) Create a new ValueError exception subclass named IncorrectSequenceLetter
2) The new exception instance should be created with the letter not found in the alphabet and the class name of the sequence. Example:
```e = IncorrectSequenceLetter(“B”, class_name)```
3) The description string of the exception must be the following:
```“The sequence item B is not found in the alphabet of class ProteinSequence”```
4) Sequence class should raise an IncorrectSequenceLetter exception when a sequence is created using an incorrect letter not found in the alphabet.
5) Modify the FASTA_iterator to be able to iterate in any type of Sequence

To do this first part of the exercise, first I had to create two scripts of python (.py), one would be the one containing the classes and methods described and the other one would be the test script to test if the exercise was done correclty. 

For this exercise, I will continue with the previous exercise file (S09) and add new things. 

1. First create a class called IncorrectSequenceLetter and inside will be the ValueError type of error, in order ot inherit its properties. Then will define the ```__init__``` function and inside will be the letter (nucleotide or amino acid) followed with the class_name (either could be DNASequence, RNASequence or ProteinSequence). Define the respective attributes and then ```super()```is used to inherit the ValueError.

````
class IncorrectSequenceLetter(ValueError):
    """Exception raised when a sequence contains a letter not in its alphabet."""
    def __init__(self, letter, class_name): #constructor: takes an input and stores it in the object so you can acces it later
        self.letter = letter
        self.class_name = class_name
        super().__init__(f"The sequence item {self.letter} is not found in the alphabet of class {self.class_name}")
````

To continue, ```class Sequence()``` will be modified in order to raise our defined previous error and inside it will contian ```x``` (letter) and ```self.__clas__.__name__``` to correctly identify the class (DNASequence, RNASequence or ProteinSequence).

````
class Sequence():
    def __init__(self, identifier, sequence):
        self.__identifier = str(identifier)
        self.__sequence = str(sequence)

        for x in sequence:
            if x not in self.alphabet:
                raise IncorrectSequenceLetter(x, self.__class__.__name__) #it correctly identifies the class (dna, protein or rna) because I use self.__clas__.__name__ inside the __init__
                #raise this new exception error instead of the generic ValueError
````
The following code has not changed from the preivous exercise:

````
def get_identifier(self) -> str:
        return self.__identifier
    
    def get_sequence(self) -> str:
        return self.__sequence
    
    def get_mw(self) -> float:
        return sum([self.weights.get(char, 0) for char in self.__sequence])
    
    def has_subsequence(self, sequence_object) -> bool:
        # The getter method is better because __sequence is private
        return sequence_object.get_sequence() in self.__sequence

    #Returns the length
    def __len__(self):
        return len(self.__sequence)
    
    #Compare = sequence strings
    def __eq__(self, other):
        if not isinstance(other, Sequence):
            return False
        return (self.get_sequence() == other.get_sequence() and
                self.get_identifier() == other.get_identifier()) #for exercise 8!
    
    #Compare ≠ sequence strings
    def __ne__(self, other):
        return not self.__eq__(other)
    
    #Concatenation
    def __add__(self, other):
        #Check if both are the same class:
        if type(self) is not type(other):
            raise TypeError("Only sequences of the same class can be concatenated")
        
        #Creating new object instances
        new_id = self.__identifier + "+" + other.get_identifier()
        new_seq = self.__sequence + other.get_sequence()

        #self.__class__ calls the constructor of the current subclass
        return self.__class__(new_id, new_seq) #if I add two DNASequence objects, self.__class__ ensures the reuslts is a DNASequence. 
    
    #Indexing: Sequence[i]
    def __getitem__(self, key):
        return self.get_sequence()[key]

    #Substring Check: in operator
    def __contains__(self, substring) -> bool:
        return substring in self.get_sequence()
    
    #Sorting by Molecular Weight
    def __lt__(self, other):
        return self.get_mw() < other.get_mw()

    def __hash__(self):
        # We create a tuple of the attributes that define "uniqueness" and then use Python's built-in hash() function on that tuple.
        #only immutable (unchangeable) objects can be hashed -> USE TUPLE!
        return hash((self.get_identifier(), self.get_sequence()))
````

Here I will define the ```FASTA_iterator()``` function (copy paste from the previous one). The only change I did here is to add a sequence_class argument:

````
#Modify FASTA_iterator
def FASTA_iterator(fasta_filename, sequence_class):
    header = None #initialize as none
    sequences_parts = [] #empty list, because sequences are often split across multiple lines 

    with open(fasta_filename, "r") as fasta_file: #closes automatically when the code is done, even if there's an error
        for line in fasta_file:
            line = line.strip() #removes \n at the end of every line
            if line.startswith(">"):
                    if header is not None:
                        #Retorno l'objecte protein amb la seqüència acumulada fins ara
                        yield sequence_class(header, "".join(sequences_parts)) 
                        #header: es guarda com a self.identifier
                        #"".join(sequences_parts): converteix la llista de línies en un sol text llarg i es guarda com a self.sequence

                    #we have a smart object tha tknows how to calculate its own eight and length. 
                    header = line[1:] #borrem aquest símbol ">"
                    sequences_parts = [] 
            else: 
                sequences_parts.append(line)
        #Retornar l'última proteïna del fitxer
        if header is not None: 
            yield sequence_class(header, "".join(sequences_parts))
        
`````

------------------- END OF THE MODIFICATED CODE, THE FOLLWOING IS THE SAME AS S09 -------------------

So in the ``` test.py ``` file, when creating a new instance of ```dna_gen = FASTA_iterator("test_sequences.fasta", DNASequence)``` for isntance, the newly created variable dna_gen is a generator object, which does not contain the sequences yet, it contians the instructions and the current state needed to produce those sequences one by one when you ask for them (like in a for loopr or using next()). So the generator reads the file lines, and when it hits the end of a record, it executes ```yield sequence_class(...)``` .

When you use a generator like FASTA_iterator, you usually use a for loop. However, a for loop stops immediately if an error occurs. By using while True and next(dna_gen), we are manually asking the generator for the "next" item one by one.

IMPORTANT KEY ASPECTS!:

- The "Try": It tries to create the DNASequence object.

- The "Except": If the sequence contains a bad letter (like 'D' in DNA), your ```Sequence.__init__ raises``` the ``` IncorrectSequenceLetter error ```.

- The continue: Instead of the program crashing, this tells Python: "Okay, that sequence was bad. Print the error message, skip it, and go back to the top of the loop to try the next one".

- Generators don't just "end" quietly when they run out of data; they raise a special signal called StopIteration.

`````
from u269315_S10 import DNASequence, ProteinSequence, FASTA_iterator, IncorrectSequenceLetter

if __name__ == "__main__":
    # 1. Create the dummy file
    with open("test_sequences.fasta", "w") as f:
        f.write(">DNA_01\nATGC\n")
        f.write(">PROT_01\nACDEF\n")

    print("--- 1. Testing Custom Exception (Spec 1-3) ---")
    try:
        DNASequence("Manual_Test", "GATCX")
    except IncorrectSequenceLetter as e:
        print(f"{e}")

    print("\n--- 2. Testing Flexible FASTA_iterator (Spec 5) ---")
    
    # Testing DNA mode
    print("Reading as DNASequence objects:")
    dna_gen = FASTA_iterator("test_sequences.fasta", DNASequence)
    while True:
        try:
            dna_obj = next(dna_gen)
            print(f"ID: {dna_obj.get_identifier()} | Type: {type(dna_obj).__name__}")
        except IncorrectSequenceLetter as e:
            print(f"{e}")
            continue # Move to next sequence
        except StopIteration:
            break

    # Testing Protein mode
    print("\nReading as ProteinSequence objects:")
    # Protein alphabet includes A, T, G, C, D, E, F so both should pass
    for prot_obj in FASTA_iterator("test_sequences.fasta", ProteinSequence):
        print(f"ID: {prot_obj.get_identifier()} | Type: {type(prot_obj).__name__}")

    
    #Testing RNA mode
    print("\nReading as RNAsequence objects:")
    rna_gen = FASTA_iterator("test_sequences.fasta", RNASequence)

    while True:
        try:
            rna_obj = next(rna_gen)
            #this part only runs if NO error is raised
            print(f"ID: {rna_obj.get_identifier()} | Type: {type(rna_obj).__name__}")
        except IncorrectSequenceLetter as e:
            #This part catches the error and lets the loop continue to the next item
            print(f"{e}")
            continue #skip the bad one and keep going
        except StopIteration:
            break #the file is finished

`````
