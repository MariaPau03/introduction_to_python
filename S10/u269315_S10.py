import sequence_dictionaries as sd
import sys #to print specifically to standrd error 
import os

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
    
    # Sorting 
    print("Sorting the sequences...", file=sys.stderr)
    all_proteins.sort()
    print("Sort process finished.", file=sys.stderr)

    #Final Output 
    out_stream = open(output_file, 'w') if output_file else sys.stdout
    try:
        for p in all_proteins:
            out_stream.write(f"{p.get_identifier()}\t{len(p)}\t{p.get_mw():.2f}\n")
    finally:
        if output_file:
            out_stream.close()

    print("Program finished correctly.", file=sys.stderr)