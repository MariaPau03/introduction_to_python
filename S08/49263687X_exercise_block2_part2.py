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
# if __name__ == "__main__":
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