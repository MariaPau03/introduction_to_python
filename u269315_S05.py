import os  # import os module to iterate through many fasta files
from u269315_S04 import FASTA_iterator
from collections import Counter
from Bio.SeqUtils.ProtParam import ProteinAnalysis #for exercise 6, 7 and 8
import numpy as np

DIR_PATH = os.path.dirname(os.path.realpath(__file__)) # set directory path

# !!!!! 1. REPEAT THE SAME EXERCISES PROPOSED IN SESSION 2 BUT USING THE FASTA_ITERATOR FUNCTION CREATED IN SESSION 4 TO READ THE FASTA FILES!!!!!!!!

## 1. Write a function that reads a FASTA file and returns the ratio of proteins that have at least a given absolute and relative frequency of a specified amino acid residue.
print("--------- Exercise 1 ----------")

#ACLARIMENT!!!: En aquest exercisi he volgut posar una funció que itera per tots els archius fasta que pugui tenir en el meu directori, així que si surten molts resultats, dependrà de quants .fasta tinguis!!!
def get_proteins_ratio_by_residue_threshold(filename, residue, relative_threshold=0.05, absolute_threshold=20):
    residue=residue.upper()
    total_proteins = 0 
    matching_proteins = 0 #how many passed bith thresholds

    for header, sequence in FASTA_iterator(filename):
        sequence = sequence.upper()
        seq_len = len(sequence)
        if seq_len == 0:
            continue

        total_proteins += 1
        absolute_count = sequence.count(residue)
        relative_freq = absolute_count / seq_len

        if absolute_count >= absolute_threshold and relative_freq >= relative_threshold:
            matching_proteins += 1
    return (matching_proteins /total_proteins) if total_proteins > 0 else 0.0

 ## 2. Exercise 2: Write a function that reads a FASTA file and creates a tab-separated text file summarizing each sequence with the following information: header, first N residues, last M residues, absolute frequency of each amino acid residue in the sequence.      
def print_sequence_summary(filename, output_filename, first_n = 10, last_m = 10):
    with open(output_filename, "w") as output_file:
        for header, sequence in FASTA_iterator(filename):
            if not sequence:
                continue
            else:
                header = header.upper()
                seq_len = len(sequence)
                first_part = sequence[:first_n]
                last_part = sequence[-last_m:] if seq_len >= last_m else sequence

            counts = Counter(sequence)
            counts_str = ",".join(f"{aa}:{counts[aa]}" for aa in counts)

            output_file.write(f"{header}\t{first_part}\t{last_part}\t{counts_str}\n")

for entry in os.scandir(DIR_PATH):  #Això em permet iterar per cada arxiu .fasta que puc tenir al meu folder
    if entry.is_file() and entry.path.endswith(".fasta"):   # check if it's a file
        print(get_proteins_ratio_by_residue_threshold(entry.path, "L"))
        print_sequence_summary(entry.path, "sequence_summary.txt")

print("--------- Exercise 2 ----------")
# !!!!! 2. A FUNCTION THAT, GIVEN A MULTILINE FASTA FILE, RETURNS THE LENGTH OF THE SEQUENCE WITH THE MAXIMUM LENGTH
def get_max_sequence_length_from_FASTA_file(fasta_filename):
    max_seq = "" #is a string
    #max_header = ""
    for header, sequence in FASTA_iterator(fasta_filename):
        if max_seq == "":
            max_seq = sequence
            #max_header = header
        else:
            if len(sequence) > len(max_seq):
                max_seq = sequence
                #max_header = header
    return len(max_seq)
print(get_max_sequence_length_from_FASTA_file("uniprot_sprot_sample.fasta"))

print("--------- Exercise 3 ----------")
# !!!!! 3. A FUNCTION THAT, GIVEN A MULTILINE FASTA FILE, RETURNS THE LENGTH OF THE SEQUENCE WITH THE MINIMUM LENGTH
def get_min_sequence_length_from_FASTA_file(fasta_filename):
    min_seq = ""
    for header, sequence in FASTA_iterator(fasta_filename):
        if min_seq == "":
            min_seq = sequence
        else:
            if len(sequence) < len(min_seq):
                min_seq = sequence
    return len(min_seq)
print(get_min_sequence_length_from_FASTA_file("uniprot_sprot_sample.fasta"))

print("--------- Exercise 4 ----------")
# !!!!! 4. A FUNCTION THAT, GIVEN A FASTA FILE, RETURNS A LIST OF TUPLES (ID, SEQ) CORRESPONDING TO THE SEQUENCE(S) WITH MAX_LEN. THE LIST MUST BE SORTED BY THE ID (CASE INSESITIVE SORTED).
def get_longest_sequences_from_FASTA_file(fasta_filename):
    max_length = 0
    longest_sequences = []
    for header, sequence in FASTA_iterator(fasta_filename):
        seq_len = len(sequence)
        if seq_len > max_length:
            max_length = seq_len
            longest_sequences = [(header, sequence)]
        else:
            if seq_len == max_length:
                longest_sequences.append((header, sequence))
    longest_sequences.sort(key=lambda x: x[0].lower())
    return longest_sequences
print(get_longest_sequences_from_FASTA_file("uniprot_sprot_sample3.fasta"))
print("--------- Exercise 5 ----------")
# !!!!! 5. A FUNCTION THAT, GIVEN A FASTA FILE, RETURNS A LIST OF TUPLES (ID, SEQ) CORRESPONDING TO THE SEQUENCE(S) WITH MIN_LEN. THE LIST MUST BE SORTED BY THE ID (CASE INSESITIVE SORTED).
def get_shortest_sequences_from_FASTA_file(fasta_filename):
    min_length = None #no value yet
    shortest_sequences = []
    for header, sequence in FASTA_iterator(fasta_filename):
        seq_len = len(sequence)
        if min_length is None or seq_len < min_length: #always check for non before comparing
            min_length = seq_len
            shortest_sequences = [(header, sequence)]
        else:
            if seq_len == min_length:
                shortest_sequences.append((header, sequence))
    shortest_sequences.sort(key=lambda x: x[0].lower())
    return shortest_sequences
print(get_shortest_sequences_from_FASTA_file("uniprot_sprot_sample.fasta"))

print("--------- Exercise 6 ----------")
# !!!!! 6. A FUNCTION, THAT GIVEN A PROTEIN FASTA FILE, RETURNS A DICTIONARY WITH THE MOLECULAR WEIGHTS OF ALL THE PROTEINS IN THE FILE. THE DICTIONARY KEYS BUST BE THE PROTEIN IDENTIFIERS AND THE ASSOCIATED VALUES MUST BE A FLOAT CORRESPONDING TO THE MOLECULAR WEIGHT.
def get_molecular_weights(fasta_filename):
    weights_dict = {}
    for header, sequence in FASTA_iterator(fasta_filename):
        clean_seq = sequence.replace("X", "")
        analysed_seq = ProteinAnalysis(clean_seq)
        weight = analysed_seq.molecular_weight()
        weights_dict[header] = round(float(weight), 2) #arrodinir a dos decimals després de la coma, que si on és massa llarg :(
    return weights_dict
print(get_molecular_weights("uniprot_sprot_sample.fasta"))

print("--------- Exercise 7 ----------")
# !!!!! 7. A FUNCTION THAT, GIVEN A PROTEIN FASTA FILE, RETURNS A TUPLE WITH (ID, SEQ) OF THE PROTEIN WITH THE LOWEST MOLECULAR WEIGHT. IF THERE ARE TWO OR MORE PROTEINS HVING THE MINIMUM WEIGHT, JUST RETURN THE FIRST ONE. 
def get_sequence_with_min_molecular_weight(fasta_filename):
    min_weight = float("inf") #is useful to find the lowest values for something!!
    #if not using float("inf") it would start at 0.0 and somethin less than 0.0 is not true ;)
    min_protein = (None, None) # to store (ID, seq) in a tuple format

    for header, sequence in FASTA_iterator(fasta_filename):
        clean_seq = sequence.replace("X", "") #Remove the X because it was inside some aa sequences
        analysed_seq = ProteinAnalysis(clean_seq)
        weight = analysed_seq.molecular_weight()
        if weight < min_weight:
            min_weight = weight
            min_protein = (header, sequence)

    return min_protein
print(get_sequence_with_min_molecular_weight("uniprot_sprot_sample.fasta"))

print("--------- Exercise 8 ----------")
# !!!!! 8. A FUNCTION THAT, GIVEN A PROTEIN FASTA FILE, RETURNS THE MEAN OF THE MOLECULAR WIGHTS OF ALL THE PROTEINS
def get_mean_molecular_weight(fasta_filename):
    weights = [] #creates a list 
    for header, sequence in FASTA_iterator(fasta_filename):
        clean_seq = sequence.replace("X", "")
        analysed_seq = ProteinAnalysis(clean_seq)
        weight = analysed_seq.molecular_weight()
        weights.append(weight) #append each weigth to at the end, calculate the average
    mean_weight = round(np.mean(weights), 2)
    return mean_weight
print(get_mean_molecular_weight("uniprot_sprot_sample.fasta"))

