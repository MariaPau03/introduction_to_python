def calculate_aminoacid_frequencies(fasta_filename, subsequences_filename, number_of_repetitions, output_filename):
    sub_w=10
    count_w=10
    prop_w=20 # 10 + 10 + 20 = 40 total chars
    
    def write_header_line(output_file, label, value, total_width=40):
        value_str=str(value)
        spaces = max(1, total_width - len(label) - len(value_str))
        output_file.write(f"{label}{' ' * spaces}{value_str}\n")

    with open(fasta_filename, "r") as fasta_file, open(output_filename, "w") as output_file:
        sequences = [] #tipo lista
        current_seq = "" #tipo string
        for line in fasta_file: #iterates over every line in the FASTA file
            line = line.strip() #removes whitespaces and new line characters
            if line.startswith(">"): #indicating a new protein header
                if current_seq: #if current_seq is not empty
                    sequences.append(current_seq) #append it to the sequence list
                    current_seq= "" #reset curent_seq for the next sequence
            else: #if the line is not a header
                current_seq += line #append the line to the current sequence
        if current_seq: #After the loop ends, check if there's a sequence to add
            sequences.append(current_seq) # The last sequence would not be added in the loop
            #This ensures the final sequence is included
        with open(subsequences_filename, "r") as sub_file:
            subs=[]
            for line in sub_file:
                line=line.strip() #filters out empty lines
                if line: #check line is not empty
                    subs.append(line)
            # RESULT: subs = ["AAA", "GGX", "KLP", "TTT"]

        total_proteins=len(sequences) #list containing full protein sequences
        #the len counts how many proteins were read from the FASTA file
        #so total_proteins stores that number
        #RESULT: sequences = ["MKTL...", "GHTY...", "AAA..."] -> total_protein = 3
        total_subs=len(subs) #list containing each sub

        results=[] #initializing the reuslts list, creating an empty list
        #This will later store results

        for sub in subs:
            #seq.count(sub) --> "MKTAAAALA".count("AAA")  --> returns 1
            sub_count = 0
            for seq in sequences:
                if seq.count(sub) >= number_of_repetitions:
                    sub_count += 1
            if sub_count > 0:
                proportion= sub_count / total_proteins if total_proteins > 0 else 0.0
                #this calculates the fraction of proteins that satisfy the condition
                results.append((sub, sub_count, proportion)) #appends a tuple to results
                #results = [("AAA", 254, 0.4),("GGX", 43, 0.1)]
        def get_proportion(x):
            return x[1] #to get the second element of the tupple
        results.sort(key=get_proportion, reverse=True) #so in this case get the second element of the results tuple, which is the proportion
    
    # Write output like the example :
        write_header_line(output_file, "#Number of proteins:", total_proteins)
        write_header_line(output_file, "#Number of subsequences:", total_subs)
        output_file.write("#Subsequence proportions:\n")

        for sub, sub_count, prop in results:
            output_file.write(f"{sub:<{sub_w}}{sub_count:>{count_w}}{prop:>{prop_w}.4f}\n")

calculate_aminoacid_frequencies("fasta_filename.fa.txt", "sub_sequences.txt", 10, "output_sub_prop.txt")
        


        
        
