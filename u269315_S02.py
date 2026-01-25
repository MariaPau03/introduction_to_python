# 1. Exercise 1: Write a function that reads a FASTA file and returns the ratio of proteins that have at least a given absolute and relative frequency of a specified amino acid residue.
def get_proteins_ratio_by_residue_threshold(filename, residue, relative_threshold=0.05, absolute_threshold=20):
    residue = residue.upper()
    
    def sequence_meets_thresholds(sequence):
        sequence = sequence.upper() #ensure residue is uppercase for matching
        seq_len = len(sequence)
        if seq_len == 0: 
            return False
        absolute_count = sequence.count(residue)   
        relative_freq = absolute_count / seq_len 
        return absolute_count >= absolute_threshold and relative_freq >= relative_threshold

    total_proteins = 0 #how many protein sequences we've processed so far
    matching_proteins = 0 #how many passed both thresholds
    seq_lines = [] #to collect lines of the current protein sequence

    def finalize_current_sequence():
        nonlocal total_proteins, matching_proteins, seq_lines #to modify the outer variables
        if not seq_lines:
            return #no sequence to process
        sequence = "".join(seq_lines)
        total_proteins += 1 #you have finished processing one protein,s o icnrement the counter regardless of whether it passe the thresholds
        if sequence_meets_thresholds(sequence):
            matching_proteins += 1
        seq_lines = [] #reset for the next sequence
    
    with open(filename, "r") as fasta_file:
        for line in fasta_file:
            line = line.strip() #removes whitespaces and new line characters
            if not line:
                continue #skip empty lines
            if line.startswith('>'): #header line indicates a new protein sequence
                finalize_current_sequence() #process the previous sequence before starting a new one
            else:
                seq_lines.append(line) #collect sequence lines
        # Finalize the last sequence after file ends
        finalize_current_sequence()
    return (matching_proteins / total_proteins) if total_proteins > 0 else 0.0

print(get_proteins_ratio_by_residue_threshold('fasta_filename.fa.txt', 'R', 0.05, 20))

# Quick test for all residues:
#residue = list('ACDEFGHIKLMNPQRSTVWY')
#for i in residue:
    #ratio = get_proteins_ratio_by_residue_threshold('example_fasta_file.fa.txt', i, 0.03, 10)
    #print(f"Residue: {i}, Ratio: {ratio}")


 # 2. Exercise 2: Write a function that reads a FASTA file and creates a tab-separated text file summarizing each sequence with the following information: header, first N residues, last M residues, absolute frequency of each amino acid residue in the sequence.      
def print_sequence_summary(filename, output_filename, first_n=10, last_m=10):
    from collections import Counter #A class for counting ocurrences of items in an iterable
    with open (filename, "r") as fasta_file, open(output_filename, "w") as output_file:
        seq_lines = []
        header = ""
    
        def finalize_current_sequence():
            nonlocal seq_lines, header
            if not seq_lines:
                return
            sequence = "".join(seq_lines)
            seq_len = len(sequence)
            first_part = sequence[:first_n]
            last_part = sequence[-last_m:] if seq_len >= last_m else sequence
            absolute_frequency = Counter(sequence)
            counts_str = ";".join(f"{aa}:{absolute_frequency[aa]}" for aa in sorted(absolute_frequency))
            #absolute_frequency[aa] looks up the count associated with the key aa (the amino‑acid letter). In the join you iterate the keys and use [aa] to get each key's count.
            output_file.write(f"{header}\t{first_part}\t{last_part}\t{counts_str}\n")
            seq_lines = []
        for line in fasta_file:
            line = line.strip()
            if not line:
                continue
            if line.startswith('>'):
                finalize_current_sequence()
                header = line[1:] #store header without '>'
            else:
                seq_lines.append(line)
        finalize_current_sequence() #finalize the last sequence

print_sequence_summary('fasta_filename.fa.txt', 'sequence_summary.txt', first_n=10, last_m=10)