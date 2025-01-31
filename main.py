import numpy as np
from decode import decode


"""

Plan:

Load all data to array
Load all instructions to array

PC = 0

While PC < len(arr)
    Fetch
    Decode
    Execute

"""


PC = np.uint32(0) # Program counter
RF = np.zeros(32, dtype=np.uint32) # Register File
IMEM = [] # Instruction Memory
DMEM = [] # Data Memory

