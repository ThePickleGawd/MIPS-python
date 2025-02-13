import numpy as np
from decode import decode
from cpu import cpu
from functions import execute

cpu.load_data("input/minimum.asm.out")
cpu.verbose = False

while not cpu.finished():
    # Fetch
    instr = cpu.fetch()

    # Decode
    data = decode(instr=instr)

    # Execute
    execute(data=data)

if cpu.verbose:
    cpu.print_registers()