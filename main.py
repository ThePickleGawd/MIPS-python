import numpy as np
from decode import decode
from cpu import cpu
from functions import execute


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

cpu.load_data("input/simpleAdd.asm.out")

while not cpu.finished():
    # Fetch
    instr = cpu.fetch()
    # Decode
    data = decode(instr=instr)

    # Execute
    execute(data=data)