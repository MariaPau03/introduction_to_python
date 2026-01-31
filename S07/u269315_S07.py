from sequence_dictionaries import protein_weights

class Protein(): #Define the class Protein
    def __init__(self, identifier, sequence):
        #Define the attributes:
        self.identifier = str(identifier)
        self.sequence = str(sequence).strip().upper()

    #Define the methods
    def get_identifier(self) -> str:
        return self.identifier

    def get_sequence(self) -> str:
        return self.sequence
    
    def get_length(self) -> int:
        return len(self.sequence)
    
    def get_mw(self) -> float:
        my_dict = protein_weights
        if self.get_length() == 0:
            return 0.0
        #Fer el càlculr i retornar directmanet! Per això fem un Generator Expression
        return sum(my_dict.get(aa,0) for aa in self.sequence) - (self.get_length() - 1) * 18.015
        #Recorre cada aa de la meva seq i get busca l'aa, i si no el troba, dona-li un pes de 0, de manera que el codi no s'atura mai per un error de dades
        #sum va suant cada pes que treu del .get(), com una guardiola. 

    def has_subsequence(self, subsequence) -> bool:
        if subsequence.sequence in self.sequence:
            return True
        else:
            return False

 #Aquí és on connecto la definició de la classe (motlle) amb les dades reals del fitxer.    
def FASTA_iterator(fasta_filename):
    header = None #initialize as none
    sequences_parts = [] #empty list, because sequences are often split across multiple lines 

    with open(fasta_filename, "r") as fasta_file: #closes automatically when the code is done, even if there's an error
        for line in fasta_file:
            line = line.strip() #removes \n at the end of every line
            if line.startswith(">"):
                    if header is not None:
                        #Retorno l'objecte protein amb la seqüència acumulada fins ara
                        yield Protein(header, "".join(sequences_parts)) 
                        #header: es guarda com a self.identifier
                        #"".join(sequences_parts): converteix la llista de línies en un sol text llarg i es guarda com a self.sequence

                    #we have a smart object tha tknows how to calculate its own eight and length. 
                    header = line[1:] #borrem aquest símbol ">"
                    sequences_parts = [] 
            else: 
                sequences_parts.append(line)
        #Retornar l'última proteïna del fitxer
        if header is not None: 
            yield Protein(header, "".join(sequences_parts))
        

              
        
        
