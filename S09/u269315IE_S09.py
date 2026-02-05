import sequence_dictionaries as sd

class Sequence():
    def __init__(self, identifier, sequence):
        self.__identifier = str(identifier)
        self.__sequence = str(sequence)

        #First check the alphabet. Here I used the sequence because I want to check the raw sequence, and later on I will use the self.__sequence argument
        for x in sequence:
            if x not in self.alphabet:
                raise ValueError(f"Impossible to create instance: {x} not possible")
        
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

# --- TEST BLOCK ---, will only be run when directly executed this file!!!
#if __name__ == "__main__":
#     print("--- Testing Validation ---")
#     try:
#         # This should work (Valid DNA)
#         dna = DNASequence("Gene_01", "GATC")
#         print(f"Successfully created: {dna.get_identifier()}")
#     except ValueError as e:
#         print(f"Error: {e}")

#     try:
#         # This should fail (Protein letters 'M' and 'W' in DNA)
#         # Specification 3: Raise exception for incorrect letters
#         bad_dna = DNASequence("Gene_02", "GATCMW")
#     except ValueError as e:
#         print(f"Caught expected error: {e}")

#     print("\n--- Testing Functionality ---")
#     # Test Molecular Weight (get_mw)
#     protein = ProteinSequence("Prot_01", "ACD")
#     # Calculation: A (89.09) + C (121.16) + D (133.1) = 343.35
#     print(f"Protein MW: {protein.get_mw()}")

#     # Test Transcription and Translation
#     dna_to_tx = DNASequence("Seq_03", "ATG") # Methionine codon
#     rna = dna_to_tx.transcribe()
#     print(f"Transcribed RNA: {rna.get_sequence()}") # Should be 'AUG'
    
#     final_protein = rna.translate()
#     print(f"Translated Protein: {final_protein.get_sequence()}") # Should be 'M'


# Test Concatenation
    # dna1 = DNASequence("ID1", "GATC")
    # dna2 = DNASequence("ID2", "GATC")
    # dna3 = dna1 + dna2
    # print(f"New ID: {dna3.get_identifier()}") # Should be ID1+ID2
    # print(f"New Seq: {dna3.get_sequence()}")   # Should be GATCGATC

# --- COMPREHENSIVE TEST BLOCK ---
# if __name__ == "__main__":
#     print("--- 1. Testing Validation (Spec 3) ---")
#     try:
#         dna1 = DNASequence("DNA_01", "GATC")
#         print("Success: Valid DNA created.")
#         bad_dna = DNASequence("DNA_02", "GATCMW") # Should fail
#     except ValueError as e:
#         print(f"Caught expected error: {e}")

#     print("\n--- 2. Testing Basic Methods & Length (S09-1) ---")
#     prot1 = ProteinSequence("Prot_01", "ACD")
#     print(f"Sequence: {prot1.get_sequence()}")
#     print(f"Length: {len(prot1)}") # Uses __len__
#     print(f"MW: {prot1.get_mw()}")

#     print("\n--- 3. Testing Equality & Inequality (S09-2, S09-3, S09-8) ---")
#     dna_a = DNASequence("ID_A", "GATC")
#     dna_b = DNASequence("ID_A", "GATC")
#     dna_c = DNASequence("ID_C", "GATC") # Same seq, different ID
    
#     # Per your __eq__, these are only equal if BOTH ID and Seq match
#     print(f"DNA_A == DNA_B: {dna_a == dna_b}") # True
#     print(f"DNA_A == DNA_C: {dna_a == dna_c}") # False (different IDs)
#     print(f"DNA_A != DNA_C: {dna_a != dna_c}") # True

#     print("\n--- 4. Testing Concatenation (S09-4) ---")
#     dna_part1 = DNASequence("Gene", "GAT")
#     dna_part2 = DNASequence("Tail", "CCA")
#     combined = dna_part1 + dna_part2 # Uses __add__
#     print(f"New ID: {combined.get_identifier()}") # Gene+Tail
#     print(f"New Seq: {combined.get_sequence()}")   # GATCCA

#     print("\n--- 5. Testing Indexing & Substrings (S09-5, S09-6) ---")
#     test_rna = RNASequence("RNA_01", "AUGCCG")
#     print(f"Base at index 0: {test_rna[0]}") # Uses __getitem__
#     print(f"Is 'AUG' in RNA? {'AUG' in test_rna}") # Uses __contains__

#     print("\n--- 6. Testing Sorting by MW (S09-7) ---")
#     p1 = ProteinSequence("Small", "A")   # Light
#     p2 = ProteinSequence("Large", "WAC") # Heavy
#     seq_list = [p2, p1]
#     seq_list.sort() # Uses __lt__
#     print(f"Sorted by MW: {[s.get_identifier() for s in seq_list]}") # ['Small', 'Large']

#     print("\n--- 7. Testing Hashing (S09-8) ---")
#     # Objects can be keys in a dict if __hash__ is implemented
#     sequence_data = {dna_a: "Original Gene"}
#     print(f"Dictionary access: {sequence_data[dna_b]}") # Works because they hash the same

#     print("\n--- 8. Testing Bio-Transformations (S08) ---")
#     gene = DNASequence("Gene_03", "ATG")
#     rna = gene.transcribe() # DNA -> RNA
#     protein = rna.translate() # RNA -> Protein
#     print(f"DNA: {gene.get_sequence()} -> RNA: {rna.get_sequence()} -> Protein: {protein.get_sequence()}")