#Biological Sequence Analysis Script
This script implements a hierarchical object-oriented system to manage and analyze biological sequences (DNA, RNA, and Protein). It utilizes a custom module, sequence_dictionaries.py, for molecular data such as valid alphabets, weights and translation tables.

## Overview

The script provides a base Sequence class and specialized subclasses to represent different biological molecules. It enforces data integrity by validating sequence characters against specific "alphabets" during object creation.

- Sequence (Parent Class): The base blueprint. It stores the identifier and sequence string as private attributes. It contains shared methods for calculating molecular weight (get_mw) and checking for subsequences (has_subsequence).

- NucleotideSequence (Subclass): A specialized class for nucleic acids. It provides the translate() method to convert nucleotides into amino acids.

- DNASequence (Subclass): Represents DNA. Includes a transcribe() method to create an RNASequence.

- RNASequence (Subclass): Represents RNA. Includes a reverse_transcribe() method to create a DNASequence.

- ProteinSequence (Subclass): Represents amino acid chains.

## Technical Specifications

- Alphabet as a Class Attribute: Each instantiated class (DNASequence, RNASequence, ProteinSequence) defines an alphabet attribute directly in the class body. This allows all instances of that class to share the same validation rules without duplicating data in memory.

- Private Attributes: To ensure encapsulation, the sequence string and identifier are stored with double underscores (e.g., __sequence). They are only accessible outside the class via "getter" methods like get_sequence().

- Validation: Upon instantiation, the __init__ method checks if every character in the input string exists in the class's alphabet. If an invalid character is found, it raises a ValueError with the specific message: Impossible to create instance: X not possible.

## Questions that helped me to understand better this exercise!

- Why is the alphabet attribute in the child classes and not the parent? While the parent class defines that an alphabet should exist, the actual characters differ for each molecule (e.g., DNA uses 'T', RNA uses 'U'). By defining it in the children, we use polymorphism—the parent’s logic stays the same, but it uses the specific "language" of whichever child is being created.

- Why check the alphabet using the raw sequence input instead of self.__sequence? Checking the raw input variable is a safety measure. It ensures that we validate the data before it is officially saved into the object's memory. This prevents the creation of an "invalid" object.

- What is an "instance"? An instance is a specific object created from a class blueprint. For example, dna1 = DNASequence("ID1", "GATC") makes dna1 an instance of the DNASequence class, containing its own unique data.

- Why do we need the weights class attribute? The get_mw() method in the parent class needs to know the "mass" of each letter. By defining a weights dictionary in each child class (sourced from sequence_dictionaries.py), the parent method can remain generic while still calculating the correct weight for DNA, RNA, or Proteins.
