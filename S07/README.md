# Instructions for exercise 7
## Here I'll explain how to do this exercise and some notes to take into account :)

```python
import sequence_dictionaries
```

The __init__ method is known as the constructor, it is the first thing that runs when you create a new "instance" (an object) of your class. Think of the class as the blueprint for a protein, and hte object as the actual physical molecule you are building. 
- Self: this represents the specific protein object being created. It allows the object to "remember" its own data. 
- identifier and sequence: These are the inputs you provide 
- self.identifier = identifier: This takes the input name and saves it permanently inside the object.
- .strip(): FASTA files often have trailing spaces or hidden newline characters at the end of sequences. If you don't strip these, your proteins length will be wrong. 

!!! If __init__ did't create self.sequence, then as soon as you call prot.lenght(), Python will throw an AttributeError: "protein" object has no attribute "sequence".

```python
class Protein:
    def __init__(self, identifier: str, sequence: str):
        self.identifier = identifier
        self.sequence = sequence.strip().upper()
```
Now, we assign the METHODS, which is a function, but associated to an object that defines the behavior of the object. When you create a protein, you pass two strings. The __init__ method takes those strings and "pins" them to the object using self. 
- self.identifier = identifier: From now on, when I say self.identifier, I mean the ID string we just saved. 
- self.sequence = sequence: From now on, when I say self.sequence, I mean the amino acid string. 

Python looks at the variables you provided and matches them up by their position:
- Whatever is in the first position gets assigned to the name identifier inside the function.

- Whatever is in the second position gets assigned to the name sequence.

```python
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
```
To get the molecular weight, the teacher gave us a file called "Sequence_dictionaries" in which there are, among many other things, the protein weights of each residue. For that, I will create a variable called my_dict, which is a DICTIONARY containing all the aa molecular weights

## THIS IS NOT PART OF THE EXERCISE, JUST TO KNOW HOW WOULD IT BE APPLIED
The Protein class is the blueprint for a single molecula. The functions read_fasta_file and load_subsequence_proteins are the factory workers that read a file and use that blueprint ro build many molecules. 

- The Class (Protein): knows about protein data (seq, weight, length)
- The Functions: know about file formats
- Methods: These are defined inside the class. They always have self as the first argument because they "belong" to an object. You call them using a dot: prot.get_mw().

- Functions: These are defined outside the class (at the top level of your script). They don't have self because they don't belong to a specific protein. You call them directly: read_fasta_file("file.fasta").

```python
def read_fasta_file(path: str) -> list[Protein]:
    proteins = []

    with open (path, "r") as f:
        identifier = None
        sequence_lines = []

        for line in f:
            line = line.strip()
            if line.startswith(">"):
                if identifier is not None:
                    sequence = "".join(sequence_lines)
                    proteins.append(Protein(identifier, sequence))

                identifier = line [1:] #remove ">"
                sequence_lines = []
            else:
                sequence_lines.append(line)
        # Save last protein
        if identifier is not None:
            sequence = "".join(sequence_lines)
            proteins.append(Protein(identifier, sequence))
    return proteins

def load_subsequence_proteins(path: str) -> list[Protein]:
    #Reads a subsequence file where each line is a subsequence
    #Returns a list of Protein objects (one per sequence)
    subs = []
    with open(path, "r") as f:
        for i, line in enumerate(f, start = 1):
            seq = line.strip()
            if seq == "":
                continue
            subs.append(Protein(f"sub_{i}", seq))
    return subs

```
The Main Block (if __name__ == "__main__":) is the site manager who tells the truck where to go and then checks each brick. It decides whether your code should actually run or just stay quiet while being borrowed by another file.
In Python, every file has a hidden variable called __name__.

- If you run the file directly (e.g., typing python u269315_S07.py in your terminal), Python sets __name__ to "__main__".

- If you import the file (e.g., import u269315_S07 inside a different script), Python sets __name__ to the filename.


```python
if __name__ == "__main__":
    proteins = read_fasta_file("uniprot_sprot_sample.fasta")
    subs = load_subsequence_proteins("sub_sequences.txt")

    for prot in proteins:
        print(prot.get_identifier())
        print(prot.get_length())
        print(f"{prot.get_mw():.4f}") 
    
        for sub in subs:
            if prot.has_subsequence(sub):
                print(f" {sub.get_sequence()}: Yes")
            else:
                print(f" {sub.get_sequence()}: No")
        print("-" * 20) # Visual separator between proteins
```




## SECOND EXERCISE

Modify the FASTA_iterator generator function to yield Protein objects instead of tuples. In each iteration, the function must yield a Protein Object:

```python
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
```



