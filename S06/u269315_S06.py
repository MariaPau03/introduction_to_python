import sys #Standard libraries for system operations (like reading files) and math (like square roots).
import math
from typing import Dict, List, Tuple, Optional

# File reading -------- 
def read_pdb_lines(pdb_file_path: Optional[str]) -> List[str]: #From either a string (file_path) or None, returns a list of strings (lines from the file)
    if pdb_file_path is None:
        return sys.stdin.read().splitlines(True) #splits the text into lines while keeping the line endings (\n)
      #if the user does not give a file, this part reads the data of PDB from stdin
    with open(pdb_file_path, "r", encoding="utf-8", errors="replace") as f:
        return f.read().splitlines(True)

#Aliases creation to make everything more readable :)
Coordinates = Tuple[float, float, float] #is immutable as it corresponds to a tuple of the 3 coordinates (x,y,z)
ResidueKey = Tuple[str, int, str] #is a tuple containing the residue_name, residue_number, atom_name
Chains = Dict[str, Dict[ResidueKey, List[Coordinates]]] #Dict[Tuple[str, int, str], List[Tuple[float, float, float]]] is a dicitonary mapping atom info and their coordenates
#List[Tuple[float,float,float]] is a list of the coordinate tuple (multiple atoms at ≠ positions)

# Positional PDB parsing --------
def parse_atom_records_positional(lines: List[str]) -> Chains: #Returns a complex nested dictionary structure
    """
    Parse ATOM/HETATM records using fixed columns (positional PDB format).

    Uses (1-based columns):
      1-6   Record name ("ATOM  " or "HETATM")
      18-20 resName
      22    chainID
      23-26 resSeq
      27    iCode
      31-38 x, 39-46 y, 47-54 z
    """
    chains: Chains = {}
    for line in lines:
         #Record name is columns 1-6, so in python it is writen like [0:6], because the last number it is not inlcuded
         rec = line[0:4].strip()
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


# Distance computation ---------
## This function calculates the squared distance between two 3D points
def dist2(a: Tuple[float, float, float], b: Tuple[float, float, float]) -> float:
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    dz = a[2] - b[2]
    return dx * dx + dy * dy + dz * dz

## Minimum squared atom-atom distance between two residues
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


# Main required function!! ---------
def calculate_pdb_chain_mean_minimum_distances(pdb_file_path: Optional[str] = None) -> Dict[str, float]:
    
    """
    For each chain:
      - For each residue i, find the minimum distance to any other residue j != i
      - Return the mean of those per-residue minimum distances

    Returns:
      dict {chain_id: mean_min_distance}
    """

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

# COMMAND-LINE INTERFACE ------

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
            print(f"{chain_id}: {means[chain_id]:.4f}")
            # For example: means[chain_id] = means["A"] = 3.4567
        return 0 #return 0 for sucess

if __name__ == "__main__": #runs only when script is executed directly (not imported)
    raise SystemExit(main(sys.argv))
        # main(sys.argv) passes command-line arguments
        # raise SystemExit() exits with the return code (0 for success)
