# 1. A Generator Function that reads a Fasta file. In each iteration, the function must return a tuple with the following format: (identifier, sequence).
## Using a Generator is a key step in learning how to handle llarge genomic files efficiently because it does not load the whole file into memory at once. 
def FASTA_iterator(fasta_filename):
    header = None #initialize as none
    sequences_parts = [] #empty list, because sequences are often split across multiple lines 
    #It is much faster to append to a list than to constantly add to a string

    with open(fasta_filename, "r") as fasta_file: #closes automatically when the code is done, even if there's an error
        for line in fasta_file:
            line = line.strip() #removes \n at the end of every line
            if line.startswith(">"): #Quan el codi arriba a un > (nou header), es dona compte de que la seq anterior finalment ha acabat
                if header is not None:
                    yield(header, "".join(sequences_parts)) #instead of returning and stop the function, it "hands over" the result as a tuple (the old header, the joined seuqence)
                    #"".join(sequences_parts) takes the list sequence fragments and glues them into one long string
                #after yielding the old data, we save the new header (using [1:]) to skip the >
                header = line[1:] #to remove the >
                sequences_parts = [] #and empty the list to start collecting the new sequence
            else: #if the line does not start with >, it is assumed that it is a piece of the sequence and adds it to the list
                sequences_parts.append(line)
        if header is not None: #Yield the very last record
            yield(header, "".join(sequences_parts))

if __name__ == "__main__": #This is telling -> ONLY RUN THE CODE BELOW IF I RAN THIS SPECIFIC FILE. If I import this function into another script later, it wouldn't start printing things automatically
#To call a generator in the script:
    for head, seq in FASTA_iterator("uniprot_sprot_sample.fasta"):
        # Note: 'head' and 'seq' match the variables assigned in this loop
        print(f"ID: {head}")
        print(f"Sequence: {(seq)}")
        print("-" * 10)
    