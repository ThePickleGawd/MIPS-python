import numpy as np
from decode import InstructionData

class CPUState():
    def __init__(self):
        self.PC = np.uint32(0) # Program counter
        self.RF = np.zeros(32, dtype=np.uint32) # Register File
        self.IMEM = [] # Instruction Memory
        self.DMEM = [] # Data Memory

    def pc_idx(self):
        return self.PC >> 2
    
    def finished(self):
        return False
    
    def fetch(self):
        # TODO: self.IMEM[PC]
        return np.uint32(0x014B4820)
    

cpu = CPUState()
