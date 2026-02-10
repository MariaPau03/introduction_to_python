from u269315_S10 import DNASequence, ProteinSequence, RNASequence, FASTA_iterator, IncorrectSequenceLetter

if __name__ == "__main__":
    # 1. Create the dummy file
    with open("test_sequences.fasta", "w") as f:
        f.write(">DNA_01\nATGC\n")
        f.write(">PROT_01\nACDEF\n")

    print("--- 1. Testing Custom Exception (Spec 1-3) ---")
    try:
        DNASequence("Manual_Test", "GATCX")
    except IncorrectSequenceLetter as e:
        print(f"{e}")

    print("\n--- 2. Testing Flexible FASTA_iterator (Spec 5) ---")
    
    # Testing DNA mode
    print("Reading as DNASequence objects:")
    dna_gen = FASTA_iterator("test_sequences.fasta", DNASequence)
    while True:
        try:
            dna_obj = next(dna_gen)
            print(f"ID: {dna_obj.get_identifier()} | Type: {type(dna_obj).__name__}")
        except IncorrectSequenceLetter as e:
            print(f"{e}")
            continue # Move to next sequence
        except StopIteration:
            break

    # Testing Protein mode
    print("\nReading as ProteinSequence objects:")
    # Protein alphabet includes A, T, G, C, D, E, F so both should pass
    for prot_obj in FASTA_iterator("test_sequences.fasta", ProteinSequence):
        print(f"ID: {prot_obj.get_identifier()} | Type: {type(prot_obj).__name__}")


    #Testing RNA mode
    print("\nReading as RNAsequence objects:")
    rna_gen = FASTA_iterator("test_sequences.fasta", RNASequence)

    while True:
        try:
            rna_obj = next(rna_gen)
            #this part only runs if NO error is raised
            print(f"ID: {rna_obj.get_identifier()} | Type: {type(rna_obj).__name__}")
        except IncorrectSequenceLetter as e:
            #This part catches the error and lets the loop continue to the next item
            print(f"{e}")
            continue #skip the bad one and keep going
        except StopIteration:
            break #the file is finished