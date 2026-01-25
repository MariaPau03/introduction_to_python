

#We need to use the FASTA_iterator
#To handle the case-sensitive requirement, it is best to convert every identifier to lowercase (.lower()) as you read them
#How to visualize the 4 required outputs?
    # UNION: every unique ID found across all files -> set {}
    # INTERSECTION: IDs that appear in every single file -> set{}
    # FREQUENCY: A counter for how many files each ID lives in -> dict
    # SPECIFIC: IDs that belong to File A but not File B or C -> dict{"":""}

def compare_fasta_file_identifiers(fasta_filename_list):
    #Initialize data structures:
    files_with_id_dict={} #empty dictionary to store the filenames and IDs
    from u269315_S04 import FASTA_iterator
    for fasta_file in fasta_filename_list:
        current_file_id_set = set() #Creates a set of IDs for this specific file
        #Use my FASTA_iterator Generator here! (handles opening the file already)
        for header, sequence in FASTA_iterator(fasta_file):
            cleaned_id = header.strip().lower() # Strings are immutable, so that's why I create a new lowercase version
            current_file_id_set.add(cleaned_id)
        #After the iterator finishes, save the set into the main dictionary 
        files_with_id_dict[fasta_file] = current_file_id_set #I'm adding the cleaned and lowercase headers for each file, as it us under the for loop that iterates for each file

    #Now do the maths that the exercise is asking! For that it is used the dictionary
    #dictionaries cannot have duplicates, so for the unique part is done (i think)
    # PREPARATION: Extract just the sets from your dictionary into a list
    # This makes it easier to compare them ALL at once. ".get()" is to look up a single specific value
    all_ids_sets = files_with_id_dict.values() #now all_ids_sets is a collection of all the sets from every file

    # 1. UNION ( All uniq IDs across ALL files)
    # Hint: In Python, you can use set.union(*ALL_SETS)
    union_ids = set.union(*all_ids_sets) #contains every set of ids

    # 2. INTERSECTION (IDs in EVERY file)
    # Hint: In Python, you can use set.intersection(*ALL_SETS)
    intersection_ids = set.intersection(*all_ids_sets)

    # 3. FREQUENCY
    # Logic: For every unique ID we found (the Union), count how many files it's in.
    frequency_dict = {} #the exercise tells that frequency should be in a dictionary format
    for uniq_ids in union_ids:
        count = 0
        for id_set in all_ids_sets:
            if uniq_ids in id_set:
                count += 1
        frequency_dict[uniq_ids] = count #dictionary[key] = value, go to that dictionary, create an entry called "key" and store "value" inside it :)
    
    # 4. SPECIFIC
    # Logic: For each file, find IDs that don't exist in ANY other file.
    specific_dict = {}

    for fasta_file, current_file_id_set in files_with_id_dict.items(): #.items() returns a list of tuples for each key-value pari in a dictionary
        other_ids = set() #create an empty set of other_ids
        # Get all IDs from all files EXCEPT the current one
        for other_files, other_set in files_with_id_dict.items():
            if fasta_file != other_files:
                other_ids = other_ids.union(other_set)
        # Specific IDs = IDs in this file MINUS IDs in all other files
        specific_dict[fasta_file] = current_file_id_set - other_ids


    return{ #we use {} becasuse it will return dictionaries and sets and hese go with {} not with () or [])
        "Intersection" : intersection_ids,
        "Union" : union_ids,
        "Frequency" : frequency_dict,
        "Specificity" : specific_dict,
    }














