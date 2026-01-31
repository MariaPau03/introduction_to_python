# Instructions for exercise 6:

## PDB Chain Mean Minimum Distances

This script calculates, for each chain in a PDB structure, the mean of the minimum distances between each residue and its closest neighboring residue.

## Code

### Start importing the necessary modules

```python
import sys #Standard libraries for system operations (like reading files) and math (like square roots).
import math
from typing import Dict, List, Tuple, Optional
```

### File reading 
This function reads the contents of a PDB file and returns it as a list of text lines. It takes one argument, `pdb_file_path`, which can either be a file path (a string) or `None`. If the argument is `None`, it means no file was provided, so the function reads the PDB data from standard input (`sys.stdin`), allowing the user to pipe or redirect a file into the program from the terminal. Otherwise, if a path is given, it opens that file in read mode and reads all its contents. In both cases, `.splitlines(True)` is used to split the text into individual lines while keeping the newline characters, so the rest of the program can process the PDB file line by line.

```python 
def read_pdb_lines(pdb_file_path: Optional[str]) -> List[str]: #From either a string (file_path) or None, returns a list of strings (lines from the file)
    if pdb_file_path is None:
        return sys.stdin.read().splitlines(True) #splits the text into lines while keeping the line endings (\n)
      #if the user does not give a file, this part reads the data of PDB from stdin
    with open(pdb_file_path, "r", encoding="utf-8", errors="replace") as f:
        return f.read().splitlines(True)
```

### Aliases creation to make everything more readable :)
These three lines define type aliases that make the code easier to understand by giving meaningful names to complex data structures. `Coordinates` represents a 3D point in space as a tuple of three floating-point numbers `(x, y, z)`, which is immutable. `ResidueKey` represents the identifier of a residue as a tuple containing the residue name (string), its sequence number (integer), and the insertion code (string). Finally, `Chains` describes the main nested dictionary used in the program: the outer dictionary maps each chain ID (like `"A"` or `"B"`) to another dictionary, which maps each residue key to a list of atomic coordinates belonging to that residue. This structure allows the program to group atoms correctly by residue and chain when computing distances.

```python
Coordinates = Tuple[float, float, float] #is immutable as it corresponds to a tuple of the 3 coordinates (x,y,z)
ResidueKey = Tuple[str, int, str] #is a tuple containing the residue_name, residue_number, atom_name
Chains = Dict[str, Dict[ResidueKey, List[Coordinates]]] #Dict[Tuple[str, int, str], List[Tuple[float, float, float]]] is a dicitonary mapping atom info and their coordenates
```

### Positional PDB parsing 
This function parses the PDB file line by line and builds a nested dictionary that groups atomic coordinates by chain and residue using the fixed-column (positional) PDB format. For each line, it first checks whether the record is an atom entry (`ATOM` or `HETATM`) and skips any other type of line. It also ensures the line is long enough to contain coordinate data. Inside the `try` block, it extracts key information from specific column positions: the residue name, chain identifier, residue sequence number, insertion code, and the x, y, z coordinates of the atom. If any of these values cannot be read correctly, the line is skipped. Each residue is uniquely identified by a tuple `(resname, resseq, icode)`, and the atom’s coordinates are stored in a list associated with that residue inside the correct chain. In the end, the function returns the full dictionary structure containing all chains, their residues, and the atomic coordinates needed later for distance calculations.

```python
def parse_atom_records_positional(lines: List[str]) -> Chains: #Returns a complex nested dictionary structure
  chains: Chains = {}
    for line in lines:
         #Record name is columns 1-6, so in python it is writen like [0:6], because the last number it is not inlcuded
         rec = line[0:6]
         if rec not in ("ATOM"):
              continue
         #Ensure to have enough width for coordinates up to column 54
         if len(line) < 54:
              continue
         try:
            #Residue name columns 18-20, so in python it is writen like [17-20]
            resname = line[17:20].strip() #The .strip() method removes whitespace (spaces, tabs, newlines) from both the beginning and end of a string.
            
            #Chain ID column is at 22, but in python is [21]
            chain_id = line[21].strip() or "_" #if the chainID is epmty, chain_id = "_" only if the first statement is false

            #Residue sequence columns 23-26, in python is [22:26]
            resseq = int(line[22:26].strip()) #in the PDB instructions, it is an integer, the previous ones are character or strings

            #Insertion code column 27, so [26]
            icode = line[26].strip() or " " #in this part of the line, i have seen white spaces

            #Coordinates:
            x = float(line[30:38].strip())
            y = float(line[38:46].strip())
            z = float(line[46:54].strip())
         except Exception: #If any error occurs while parsing (e.g., invalid float conversion), the except block catches it and continue skips to the next line. This prevents the entire program from crashing on malformed data.
            #Any parse failure -> skip the line
            continue

         residue_key = (resname, resseq, icode) #this creates a tuple, used as a key in the nested dictionary
         chains.setdefault(chain_id, {}). setdefault(residue_key, []).append((x, y, z))
    return chains
```

### Distance computation
The function `dist2` computes the squared distance between two points in 3D space by subtracting their x, y, and z coordinates, squaring the differences, and summing them, which avoids using a square root and is faster for comparisons. The function `min_residue_residue_dist2` uses this helper to calculate the minimum squared distance between two residues by comparing every atom in the first residue (`atoms_a`) with every atom in the second residue (`atoms_b`). It starts with the value infinity, then updates `best` whenever a smaller atom–atom distance is found. If a distance of zero occurs, it immediately returns because that is the smallest possible value. In the end, it returns the smallest squared distance between any pair of atoms from the two residues, which is later used to measure how close the residues are.

```python
def dist2(a: Tuple[float, float, float], b: Tuple[float, float, float]) -> float:
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    dz = a[2] - b[2]
    return dx * dx + dy * dy + dz * dz
def min_residue_residue_dist2(
        atoms_a: List[Coordinates],
        atoms_b: List[Coordinates],
        ) -> float:
    best = float("inf") #starts with infinity, so any real distance will be smaller
    for pa in atoms_a: #compares all atoms pairs
        for pb in atoms_b:
            d2 = dist2(pa, pb) #computes the distance between every pair of atos
            if d2 < best: #keep updating best, whenever a smaller distance is found
                best = d2
                if best == 0.0:
                    return 0.0
    return best
```

### Main required function!!
This part of the function reads and parses the PDB file into a nested dictionary (`chains`), then computes one final mean value per chain and stores it in `results`. For each chain, it first builds a clean list of residues that actually contain atom coordinates and skips chains with fewer than two residues (because you can’t compute inter-residue distances). It then sorts residues in a consistent order (by residue number, insertion code, and name), extracts only the coordinate lists into `coords_list`, and creates `per_res_min_d2`, a list initialized to infinity to store each residue’s closest-neighbor squared distance. Next, it loops over every unique residue pair `(i, j)`, computes the minimum squared atom–atom distance between those two residues, and updates the current best (smallest) distance for both residues `i` and `j`. After all pairs are processed, it converts each residue’s best squared distance to a real distance using `sqrt`, averages these per-residue minimum distances, and saves the mean into `results[chain_id]`; finally, it returns the dictionary mapping each chain to its mean minimum residue distance.

```python
def calculate_pdb_chain_mean_minimum_distances(pdb_file_path: Optional[str] = None) -> Dict[str, float]:
lines = read_pdb_lines(pdb_file_path)
    chains = parse_atom_records_positional(lines)

    results: Dict[str, float] = {} #Stores actual data and results is the variable name

    for chain_id, residue_map in chains.items(): #chains is a dictionary that contains everything
        #residue_map = the inner dictionary with all residues for that chain
        #rk = residue key tuple, like ("ALA", 1, " ")
        #coords = list of coordinates for that residue, like [(1.0, 2.0, 3.0), (1.1, 2.1, 3.1)]
        #Create a clean list of residues that actually have atom data, removing the empty ones
        #residue_map.items() gives all residue key-value pairs, and for each pair, unpack it itno rk and coords(list) and only keep pairs where coords is not empty
        residues = [(rk, coords) for rk, coords in residue_map.items() if coords]
        #residues = [] creates a filtered list of residues
        if len(residues) < 2: #we need at least 2 residues to calculate distances between them
            continue

        
        #sort residues by resseq, idcode, resname
        #rk --> residue_key = (resname, resseq, icode)
        #lambda is a keyword for creating anonymous functions. t is the argument (each residue tuple from the list)
        #Basic syntax --> lambda arguments: expression
        residues.sort(key=lambda t: (t[0][1], t[0][2], t[0][0]))
        coords_list = [coords for _, coords in residues]
        n = len(coords_list)

        #For each residue, track its closest other-residue distance ^2
        # [float("inf")] = a list with one element: infinity
        # * n = repeat that list n times (where n is the number of residues)
        per_res_min_d2 = [float("inf")] * n

        #Compute mean of all pairwise residue minimum distances
        pairwise_distances = []
        for i in range(n):
            for j in range(i + 1, n):
                # Find minimum distance between atoms in these two residues
                d2 = min_residue_residue_dist2(coords_list[i], coords_list[j])
                d = math.sqrt(d2)
                pairwise_distances.append(d)

        if not pairwise_distances:
            continue

        results[chain_id] = sum(pairwise_distances) / len(pairwise_distances)
    return results
```
### Command-line interface
This final part of the script defines the `main` function, which handles running the program from the command line. It checks whether the user provided a PDB file path as an argument (`argv[1]`); if not, it sets `pdb_path` to `None`, which makes the program read the PDB data from standard input instead. It then calls `calculate_pdb_chain_mean_minimum_distances`, storing the returned dictionary of mean distances per chain in `means`. The script loops through the chain IDs in sorted order and prints each chain with its mean minimum distance formatted to four decimal places. The `return 0` indicates successful execution. Finally, the block `if __name__ == "__main__":` ensures that `main` is only executed when the file is run directly as a script, not when it is imported as a module, and `raise SystemExit(...)` terminates the program cleanly using the return code.

```python
#argv -> a list of command-line arguments, and the function will return an integer, typically 0 for sucess and non-0 for errors
def main(argv: List[str]) -> int:
        pdb_path = argv[1] if len(argv) >= 2 else None
        means = calculate_pdb_chain_mean_minimum_distances(pdb_path) #stores the reuslts in means dictionary
        '''
        means = {
                "A": 3.4567,    # chain_id "A" → mean distance 3.4567
                "B": 2.1234,    # chain_id "B" → mean distance 2.1234
                "C": 5.6789,    # chain_id "C" → mean distance 5.6789
                }
        '''
        for chain_id in sorted(means): #loop through chainIDs in alphabetical order
            print(f"{chain_id}:\t{means[chain_id]:.4f}")
            # For example: means[chain_id] = means["A"] = 3.4567
        return 0 #return 0 for sucess

if __name__ == "__main__": #runs only when script is executed directly (not imported)
    raise SystemExit(main(sys.argv))
        # main(sys.argv) passes command-line arguments
        # raise SystemExit() exits with the return code (0 for success)
```






### With a PDB file path

```bash
python script.py structure.pdb

cat structure.pdb | python script.py
```
