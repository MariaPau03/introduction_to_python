# Instructions for exercise 6:

## PDB Chain Mean Minimum Distances

This script calculates, for each chain in a PDB structure, the mean of the minimum distances between each residue and its closest neighboring residue.

## Code

### Start importing the necessary modules

''' python
import sys #Standard libraries for system operations (like reading files) and math (like square roots).
import math
from typing import Dict, List, Tuple, Optional


### With a PDB file path

```bash
python script.py structure.pdb

cat structure.pdb | python script.py

