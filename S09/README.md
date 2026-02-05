# Biological Sequence Analysis System

## Project Overview

This Python project implements an object-oriented hierarchy for handling biological sequences (DNA, RNA, and Protein). The system focuses on encapsulation (using private attributes), inheritance, and operator overloading to make biological objects behave like built-in Python types.

## Class Structure & Inheritance

- Sequence (Parent): Contains the core logic for all sequences, including identification, molecular weight calculation, and subsequence checking.

- NucleotideSequence: A middle layer providing the translate() method for nucleic acids.

- DNASequence, RNASequence, ProteinSequence: The final, instantiated subclasses that define specific alphabets and weights using data from sequence_dictionaries.py.

## Implemented Behaviors (Session 09)

- Length (len()): Implemented via __len__ to return the sequence string length.

- Equality (==): Implemented via __eq__. Two instances are equal only if they share the same identifier AND the same sequence string.

- Inequality (!=): Automatically handled via __ne__ based on the equality logic.

- Concatenation (+): Implemented via __add__. It creates a new instance of the same class with combined sequences and identifiers joined by a +.

- Indexing ([]): Implemented via __getitem__ to allow access to specific bases/amino acids.

- Containment (in): Implemented via __contains__ to check for substrings within the sequence.

- Sorting: Implemented via __lt__ (less than) to allow sorting a list of sequence objects by their molecular weight.

- Hashing: Implemented via __hash__ using a tuple of the identifier and sequence. This allows objects to be used in sets or as dictionary keys.

## Frequently asked questions I had

- Why are these called "Instances"? An instance is a specific object created from a class blueprint. While DNASequence is the rulebook, dna1 is the actual "player" containing specific data.

- Why use a Tuple in __hash__ and not a List? Dictionary keys and set members must be immutable (unchangeable). Tuples are immutable and can be hashed, whereas lists can change and are therefore "unhashable" in Python.

- How does dna1 + dna2 work? Through Operator Overloading. Python sees the + and looks for the __add__ method inside your class. We programmed it to verify that both objects are the same class before creating a new result.
