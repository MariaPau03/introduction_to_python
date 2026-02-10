# 1. Create a new ValueError exception subclass named IncorrectSequenceLetter:

class IncorrectSequenceLetter(ValueError):
    pass

e = IncorrectSequenceLetter("B", protein)
