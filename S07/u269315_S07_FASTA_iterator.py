from u269315_S07 import Protein
def FASTA_iterator(fasta_filename):
    header = None #initialize as none
    sequences_parts = [] #empty list, because sequences are often split across multiple lines 

    with open(fasta_filename, "r") as fasta_file: #closes automatically when the code is done, even if there's an error
        for line in fasta_file:
            line = line.strip() #removes \n at the end of every line
            if line.startswith(">"):
                    if header is not None:
                        yield Protein(header, "".join(sequences_parts)) #The raw header string is saved to self.identifier, and teh same for sequence saved to self.sequence
                    #we have a smart object tha tknows how to calculate its own eight and length. 
                    header = line[1:] 
                    sequences_parts = [] 
            else: 
                sequences_parts.append(line)
        if header is not None: #Yield the very last record
            yield Protein(header, "".join(sequences_parts))

if __name__ == "__main__": 
    for prot in FASTA_iterator("uniprot_sprot_sample.fasta"):
        print(f"ID: {prot.get_identifier()}")
        print(f"Sequence: {prot.get_sequence()}")
        print("-" * 10)
    