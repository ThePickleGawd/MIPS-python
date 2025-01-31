import numpy as np
from decode import decode
from cpu import cpu


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

while not cpu.finished():
    # Fetch
    instr = np.uint32(0x014B4820)

    # Decode
    data = decode(instr=instr)

    # Execute
    