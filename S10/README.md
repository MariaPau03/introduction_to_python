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

First create a class called IncorrectSequenceLetter and inside will be the ValueError type of error, in order ot inherit its properties. Then will define the ```__init__``` function and inside will be the letter (nucleotide or amino acid) followed with the class_name (either could be DNASequence, RNASequence or ProteinSequence). Define the respective attributes and then ```super()```is used to inherit the ValueError.

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

6) Modify the FASTA_iterator generator function to skip sequences having incorrect letters . It must capture specifically the IncorrectSequenceLetter exception. When it happens, it should print a message of error in the standard error and continue with the
next sequence. Do not handle other types of exceptions, only IncorrectSequenceLetter exceptions.


To print specifically to stderr as requires, it is needed to import the ```sys``` module. 

````
def FASTA_iterator(fasta_filename, sequence_class):
    header = None #initialize as none
    sequences_parts = [] #empty list, because sequences are often split across multiple lines 

    with open(fasta_filename, "r") as fasta_file: #closes automatically when the code is done, even if there's an error
        for line in fasta_file:
            line = line.strip() #removes \n at the end of every line
            if line.startswith(">"):
                    if header is not None:
                        try:
                            yield sequence_class(header, "".join(sequences_parts)) 
                        #header: es guarda com a self.identifier
                        #"".join(sequences_parts): converteix la llista de línies en un sol text llarg i es guarda com a self.sequence
                        except IncorrectSequenceLetter as e:
                            #print to stderr and continue
                            print(f"{e}", file=sys.stderr)
                    #we have a smart object tha tknows how to calculate its own eight and length. 
                    header = line[1:] #borrem aquest símbol ">"
                    sequences_parts = [] 
            else: 
                sequences_parts.append(line)
        #Retornar l'última proteïna del fitxer
        if header is not None: 
            try:
                yield sequence_class(header, "".join(sequences_parts)) 
            except IncorrectSequenceLetter as e:       
                print(f"{e}", file=sys.stderr)

````


7) When the script is executed as a standalone application (without being imported (i.e. code under __main__ block), the script should read input DNA FASTA file(s) and calculate the length and molecular weight of their corresponding proteins (i.e. corresponding to ProteinSequence instances obtained after translation). The script must print the output to standard output or to a file. Output should be sorted by molecular weight, from lowest to greatest


Because DNASequence is a subclass of NucleotideSequence (it inherits from it), it "grabs" or inherits all the methods defined in that parent class. Therefore, any DNASequence object automatically has the translate() function available to it.

And to take into account the input fasta file, the input hsould be two things, on position 0 the standaone application and on position 1 the name of the fasta file. If the len of this, is less than 2, print a message warning that in order to run the script, it needs to pass another argument which is the name of the fasta file. If this is provided, the input fasta file is located at position 1 and iterates through every dna_onj in the FASTA_iterator generator that will read the input file and wull be DNASequence. As DNASequence inherits all from its parent class (NucleotideSequence) and this has the translation function, we will use it to translate from DNA --> RNA, and append every sequence into a protein object. If there is a letter not found on the alphabet, it will run the except block and rais the IncorrectSequenceLetter error printing the message value defined inside its class and by adding ```file=sys.stderr``` I am tellig python: ```This is not a result, this is an error message, send i to the error chanel! ``` .
Then sort the proteins and finally, for every protein in proteins get the identifier, separated by a tab spaace, then the lenght and the molecular weight. 

All this code mentioned above will go at the end of the S10.py script:

````
import sequence_dictionaries as sd
import sys #to print specifically to standrd error 

class IncorrectSequenceLetter(ValueError):
    """Exception raised when a sequence contains a letter not in its alphabet."""
    def __init__(self, letter, class_name): #constructor: takes an input and stores it in the object so you can acces it later
        self.letter = letter
        self.class_name = class_name
        super().__init__(f"The sequence item {self.letter} is not found in the alphabet of class {self.class_name}")

class Sequence():
    def __init__(self, identifier, sequence):
        self.__identifier = str(identifier)
        self.__sequence = str(sequence)

        for x in sequence:
            if x not in self.alphabet:
                raise IncorrectSequenceLetter(x, self.__class__.__name__) #it correctly identifies the class (dna, protein or rna) because I use self.__clas__.__name__ inside the __init__
                #raise this new exception error instead of the generic ValueError

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

#Modify FASTA_iterator
def FASTA_iterator(fasta_filename, sequence_class):
    header = None
    sequences_parts = []

    with open(fasta_filename, "r") as fasta_file:
        for line in fasta_file:
            line = line.strip()
            if line.startswith(">"):
                if header is not None:
                    # Requirement 6: Catch the error so the program doesn't crash
                    try:
                        yield sequence_class(header, "".join(sequences_parts))
                    except IncorrectSequenceLetter as e:
                        print(f"Error: {e}", file=sys.stderr)
                
                header = line[1:]
                sequences_parts = []
            else:
                sequences_parts.append(line)
        
        # Handle the last sequence
        if header is not None:
            try:
                yield sequence_class(header, "".join(sequences_parts))
            except IncorrectSequenceLetter as e:
                print(f"Error: {e}", file=sys.stderr)

class ProteinSequence(Sequence): #INSTANTIATED!!!
#Put inside the parent class 

    #Inherits the __init__ function of the parent

    #Specific class attributes for Proteins
    alphabet = sd.protein_letters
    weights = sd.protein_weights
    

class NucleotideSequence(Sequence):
#Put inside the parent class

    #Inherits the __init__ function of the parent

    # To be implemented using rna_table or dna_table
    def translate(self) -> ProteinSequence:
        seq = self.get_sequence()
        protein_seq = "" #empty string

        # Choose the correct table, based on wheter you want to translate into RNA or keep it with DNA
        if isinstance(self, DNASequence):
            table  = sd.dna_table

        else:
            table = sd.rna_table

        #Loop through the sequence
        # Subtract 2 because the loop needs space for 
        # the current item, the next item, and the one after that.
        protein_chars = []
        for i in range(0,len(seq) - 2, 3): #range(start,stop,range)
            codon = seq[i:i+3] # +3 because the first position is position 0, not 1 
            amino_acid = table.get(codon, "X") # 'X' for unknown/stop
            protein_chars.append(amino_acid) 

        # Return a NEW ProteinSequence object as required by the diagram
        return ProteinSequence(self.get_identifier(), "".join(protein_chars))
    

class DNASequence(NucleotideSequence): #INSTANTIATED!!!!
#Put inside the parent class
    alphabet = sd.dna_letters  # This is the class attribute
    weights = sd.dna_weights

    # Inherits the __init__ function of the parent

    def transcribe(self) -> "RNASequence": #put "RNASequence" because appears later, so tell python using "" that this function will apear later on
        rna_seq = self.get_sequence(). replace("T", "U")
        return RNASequence(self.get_identifier(), rna_seq)
        

class RNASequence(NucleotideSequence): #INSTANTIATED!!!!
#Put inside the parent class
    alphabet = sd.rna_letters
    weights = sd.rna_weights

    # Inherits the __init__ function of the parent

    def reverse_transcribe(self) -> DNASequence:
        dna_seq = self.get_sequence(). replace("U", "T")
        return DNASequence(self.get_identifier(), dna_seq)


if __name__ == "__main__":
    #Check if a filename was provided in the temrinal
    if len(sys.argv) < 2:
        print("Usage: python u269315_S10.py <fasta_file>")
    else:
        input_f = sys.argv[1]
        proteins = []

        for dna_obj in FASTA_iterator(input_f, DNASequence):
            try:
                prot_obj = dna_obj.translate()
                proteins.append(prot_obj)
            except IncorrectSequenceLetter as e:
                print(f"{e}", file=sys.stderr)

        proteins.sort()

        for p in proteins:
            print(f"{p.get_identifier()}\t{len(p)}\t{p.get_mw():.2f}")

````

7.1) If the script is executed without arguments, it looks for all “.fasta” or “.fa” files in the current directory, and process all of them with a single sorted output. Print the results to standard output.
7.2) If the script has a single argument, it corresponds to the input. If it is a directory, it looks for all “.fasta” or “.fa” files in the given directory, process them and print the results in standard output. If this single argument corresponds to a file (not necessarily “.fasta”, or “.fa”), process it and print the results in standard output.
7.3) If the script has two arguments, the first one corresponds to the input and the second one to the output file.
7.4) The script should print to standard error a progression log

To finish with this exercise, I had to change a bit the final command-line interface logic as described, to automate file searching, handle errors and organize output based on user input. 

The code below shows the helper function ``` process_file ``` and is designed to handle the core biological logic. 

- FASTA_iterator(filepath, DNASequence): It uses your flexible iterator to yield DNA objects one by one.

- The try...except block: It attempts to translate the DNA into a protein. If dna_obj.translate() triggers an IncorrectSequenceLetter (because of an "X" or invalid codon), the code catches it.

- file=sys.stderr: Instead of the program crashing, it prints the error message to the "error channel" and continues to the next sequence in the file.

- Returns count: It keeps track of how many valid sequences were successfully processed in that specific file.

````
def process_file(filepath, proteins_list):
    count = 0
    for dna_obj in FASTA_iterator(filepath, DNASequence):
        try:
            prot_obj = dna_obj.translate()
            proteins_list.append(prot_obj)
            count += 1
        except IncorrectSequenceLetter as e:
            # Requirement 6: Print error to stderr and continue
            print(f"Error in {filepath}: {e}", file=sys.stderr)
    return count

````

Now, the following section determines where the data is coming from and where it should go based on what the user types in the terminal. 

- len(sys.argv) == 1: If the user just types python u269315_S10.py, the script automatically finds all .fasta or .fa files in the current folder using os.listdir('.').

- os.path.isdir(path): If the user provides a path, the script checks if it is a directory. If it is, it gathers all FASTA files inside that folder.

- output_file = sys.argv[2]: If a second argument is provided, the script stores that name to save the final results there instead of printing them to the screen.

To provide a real-time feedback to the user via stderr, it must:

- print how many files were found
- As each file finished, it logs filename finished
- It explicitly logs when the storing process starts and ends
- stderr to endure that if the results are safed in a file, these lo messages don't end up inside the data file, they stay on the terminal screeen.

The final cleanup of the data:

- all_proteins.sort() uses the ```__lt__```method
- out_stream: This is a "smart" output. If the user provided an output filename, it opens that file; otherwise, it defaults to sys.stdout (the screen).
- The finally block: This ensures that if a file was opened for writing, it gets closed properly even if something goes wrong during the printing process.

````
# Command-line interface script:!

def process_file(filepath, proteins_list):
    count = 0
    for dna_obj in FASTA_iterator(filepath, DNASequence):
        try:
            prot_obj = dna_obj.translate()
            proteins_list.append(prot_obj)
            count += 1
        except IncorrectSequenceLetter as e:
            # Requirement 6: Print error to stderr and continue
            print(f"Error in {filepath}: {e}", file=sys.stderr)
    return count

if __name__ == "__main__":
    input_files = []
    output_file = None
    all_proteins = []

    # Exercise 7.1, 7.2, 7.3
    if len(sys.argv) == 1: # No arguments
        input_files = [f for f in os.listdir('.') if f.endswith(('.fasta', '.fa'))]
    elif len(sys.argv) >= 2:
        path = sys.argv[1]
        if os.path.isdir(path): # Argument is a directory
            input_files = [os.path.join(path, f) for f in os.listdir(path) if f.endswith(('.fasta', '.fa'))]
        else: # Argument is a single file
            input_files = [path]
        
        if len(sys.argv) == 3: # Output file provided
            output_file = sys.argv[2]

    # Exercise 7.4
    print(f"{len(input_files)} FASTA files found.", file=sys.stderr)
    
    total_sequences = 0
    for f in input_files:
        seq_count = process_file(f, all_proteins)
        total_sequences += seq_count
        print(f"{f} finished.", file=sys.stderr)

    print(f"{total_sequences} sequences found.", file=sys.stderr)
    
    # --- Sorting ---
    print("Sorting the sequences...", file=sys.stderr)
    all_proteins.sort()
    print("Sort process finished.", file=sys.stderr)

    # --- Final Output ---
    out_stream = open(output_file, 'w') if output_file else sys.stdout
    try:
        for p in all_proteins:
            out_stream.write(f"{p.get_identifier()}\t{len(p)}\t{p.get_mw():.2f}\n")
    finally:
        if output_file:
            out_stream.close()

    print("Program finished correctly.", file=sys.stderr)

    ````

## Ways to run the script from the terminal:

- Run a specific file (exercise 7.2)

````
python u269315_S10.py small_DNA_seq.fasta
`````

- Run and save the results to a file (exercise 7.3)

````
python u269315_S10.py small_DNA_seq.fasta my_results.txt
`````

- Run on an entire folder (exercise 7.2)

````
python u269315_S10.py ./my_sequences_folder/
`````

- Automatic "No argument" mode (exercise 7.1)

Process every fasta file in the ucrent working directory without typing any names

````
python u269315_S10.py

`````

- See only the data and hide the log (exercise 7.4)

````
python u269315_S10.py 2> log.txt
````
Where the 2> redirector sends the progression log into a file called log.txt

- To verify the progression log is correctly separated from the data, use this command (exercise 7.4)

````
python u269315_S10.py small_DNA_seq.fasta > only_data.txt
`````

## Some insights:

Both pipes (stdout and stderr) are displayed on the screen, which is why they look mixed together. However, they are fundamentally separate. 

1. Normal execution 

- Command: python u269315_S10.py file.fasta

- Where stdout goes: To the terminal screen.

- Where stderr goes: To the terminal screen.

Result: see everything at once.

2. Output redirection 

- Command: python u269315_S10.py file.fasta > results.txt

- Where stdout goes: Into the file results.txt.

- Where stderr goes: Still to the terminal screen.

Result: The progression log stays on the screen to show progress, while the results are saved cleanly in the file without any log messages inside.

3. Error redirection (The "Black Hole" View)

- Command: python u269315_S10.py file.fasta 2> /dev/null

- Where stdout goes: To the terminal screen.

- Where stderr goes: To a special system file that deletes everything sent to it (/dev/null).

Result: see only the table of proteins. 