import numpy as np
from decode import InstructionData

class CPUState():
    def __init__(self):
        self.PC = np.uint32(0) # Program counter
        self.RF = np.zeros(32, dtype=np.uint32) # Register File
        self.IMEM = np.zeros(0, dtype=np.uint32) # Instruction Memory
        self.DMEM = np.zeros(0, dtype=np.uint32) # Data Memory

    def load_data(self, file):
        # spim -assemble [file]

        with open(file, 'r') as f:
            # Format:
            # .text # hexStart hexEnd
            # .word [comma separated hex instructions]
            # .data # hexStart hexEnd
            # .word [comma separated hex data]
            line1 = f.readline()
            line2 = f.readline()
            line3 = f.readline()
            line4 = f.readline()

            # Get hex range for instructions
            line1Arr = line1.split()
            instrHexStart, instrHexEnd = int(line1Arr[2],16), int(line1Arr[4], 16)
            
            # Get and load instructions
            instructions = line2.split(".word ")[1].split(", ")
            self.IMEM = np.array([np.uint32(int(instr,16)) for instr in instructions], dtype=np.uint32)

            # Get hex range for data
            line3Arr = line3.split()
            dataHexStart, dataHexEnd = int(line3Arr[2], 16), int(line3Arr[4], 16)

            # Get and load data
            self.DMEM = np.array([np.uint32(int(data, 16)) for data in line4.split(".word ")[1].split(", ")], dtype=np.uint32)

    def pc_idx(self):
        return self.PC >> 2
    
    def finished(self):
        return self.IMEM[self.pc_idx()] == 0
    
    def fetch(self):
        idx = self.pc_idx()
        self.PC += 4
        return self.IMEM[idx]
    

cpu = CPUState()
