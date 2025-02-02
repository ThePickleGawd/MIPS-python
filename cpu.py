import numpy as np
from decode import InstructionData

class CPUState():
    def __init__(self):
        self.PC = np.uint32(0) # Program counter
        self.RF = np.zeros(32, dtype=np.uint32) # Register File
        self.IMEM = np.zeros(32, dtype=np.uint32) # Instruction Memory
        self.DMEM = np.zeros(32, dtype=np.uint32) # Data Memory

    def load_data(self):
        instructions = [
            0x014B4820, # add $t1 $t2 $t3
            0x2062FFFF, # addi $v0 $v1 0xffff 
            0x014B4822 # sub t1 t2 t3
        ]

        for i in range(len(instructions)):
            self.IMEM[i] = instructions[i]

    def pc_idx(self):
        return self.PC >> 2
    
    def finished(self):
        return self.IMEM[self.pc_idx()] == 0
    
    def fetch(self):
        idx = self.pc_idx()
        self.PC += 4
        return self.IMEM[idx]
    

cpu = CPUState()
