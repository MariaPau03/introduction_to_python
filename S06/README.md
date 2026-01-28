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

### File reading --------

First I'll start by reading the file. The input would be a string, but at the end I want a list of the lines from the given file. If the PDB file is not provided, then the data comes from the stdin of the PDB

```python 
def read_pdb_lines(pdb_file_path: Optional[str]) -> List[str]: #From either a string (file_path) or None, returns a list of strings (lines from the file)
    if pdb_file_path is None:
        return sys.stdin.read().splitlines(True) #splits the text into lines while keeping the line endings (\n)
      #if the user does not give a file, this part reads the data of PDB from stdin
    with open(pdb_file_path, "r", encoding="utf-8", errors="replace") as f:
        return f.read().splitlines(True)
```

### With a PDB file path

```bash
python script.py structure.pdb

cat structure.pdb | python script.py
```
