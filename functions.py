from typing import Callable
import numpy as np
from decode import InstructionData
from cpu import cpu

# R types

def add(data: InstructionData):
    # R[rd] = R[rs] + R[rt]
    # TODO: Trap on overflow?? (Check if negative or positive overflow)
    cpu.RF[data["rd"]] = cpu.RF[data["rs"]] + cpu.RF[data["rt"]]

def addu(data: InstructionData):
    # R[rd] = R[rs] + R[rt]
    cpu.RF[data["rd"]] = cpu.RF[data["rs"]] + cpu.RF[data["rt"]]

def sub(data: InstructionData):
    # R[rd] = R[rs] - R[rt]
    # TODO: Trap on overflow??
    cpu.RF[data["rd"]] = cpu.RF[data["rs"]] - cpu.RF[data["rt"]]

def subu(data: InstructionData):
    # R[rd] = R[rs] - R[rt]
    cpu.RF[data["rd"]] = cpu.RF[data["rs"]] - cpu.RF[data["rt"]]

def and_(data: InstructionData):
    # R[rd] = R[rs] & R[rt]
    cpu.RF[data["rd"]] = cpu.RF[data["rs"]] & cpu.RF[data["rt"]]

def or_(data: InstructionData):
    # R[rd] = R[rs] | R[rt]
    cpu.RF[data["rd"]] = cpu.RF[data["rs"]] | cpu.RF[data["rt"]]

def xor(data: InstructionData):
    # R[rd] = R[rs] ^ R[rt]
    cpu.RF[data["rd"]] = cpu.RF[data["rs"]] ^ cpu.RF[data["rt"]]
    
def nor(data: InstructionData):
    # R[rd] = ~(R[rs] | R[rt])
    cpu.RF[data["rd"]] = ~(cpu.RF[data["rs"]] | cpu.RF[data["rt"]])

def sll(data: InstructionData):
    # R[rd] = R[rt] << shamt
    cpu.RF[data["rd"]] = cpu.RF[data["rt"]] << data["shamt"]

def srl(data: InstructionData):
    # R[rd] = R[rt] >> shamt
    cpu.RF[data["rd"]] = (cpu.RF[data["rt"]] >> data["shamt"])

def sra(data: InstructionData):
    # R[rd] = R[rt] >> shamt (keep original sign)
    sign_bit = (cpu.RF[data["rt"]] >> 31) & 1
    cpu.RF[data["rd"]] = (cpu.RF[data["rt"]] >> data["shamt"]) & (sign_bit << 31)

def slt(data: InstructionData):
    # R[rd] = (R[rs] < R[rt]) ? 1 : 0
    signed_rs = cpu.RF[data["rs"]].astype(np.int32)
    signed_rt = cpu.RF[data["rt"]].astype(np.int32)

    cpu.RF[data["rd"]] = 1 if (signed_rs < signed_rt) else 0

def sltu(data: InstructionData):
    # R[rd] = (R[rs] < R[rt]) ? 1 : 0
    cpu.RF[data["rd"]] = 1 if (cpu.RF[data["rs"]] < cpu.RF[data["rt"]]) else 0

def jr(data: InstructionData):
    # PC=R[rs]
    cpu.PC = cpu.RF[data["rs"]]

def syscall(data): 
    v0 = cpu.RF[2]
    a0 = cpu.RF[4]

    print("SYSCALL:", v0, a0)
    
    match v0:
        case 1:
            print(a0)
            return

        case 4:
            # Print string
            # TODO: a0 is the mem addr; string concat until null
            
            return

        case 5:
            cpu.RF[2] = input()
            return

        case 10:
            # Hack that may work??
            cpu.finished = lambda: True
            return

# I types

def addi(data: InstructionData):
    # R[rt] = R[rs] + SignExtImm
    cpu.RF[data["rt"]] = cpu.RF[data["rs"]] + data["immediate"].astype(np.int16)

def addiu(data: InstructionData):
    # R[rt] = R[rs] + SignExtImm
    cpu.RF[data["rt"]] = cpu.RF[data["rs"]] + data["immediate"]

def andi(data: InstructionData):
    # R[rt] = R[rs] & ZeroExtImm
    cpu.RF[data["rt"]] = cpu.RF[data["rs"]] & data["immediate"]

def ori(data: InstructionData):
    # R[rt] = R[rs] | ZeroExtImm
    cpu.RF[data["rt"]] = cpu.RF[data["rs"]] | data["immediate"]

def xori(data: InstructionData):
    # R[rt] = R[rs] ^ ZeroExtImm
    cpu.RF[data["rt"]] = cpu.RF[data["rs"]] ^ data["immediate"]

def lui(data: InstructionData):
    # R[rt] = Immediate << 16
    cpu.RF[data["rt"]] = data["immediate"] << 16


def beq(data: InstructionData): pass

def bne(data: InstructionData): pass

def slti(data: InstructionData): pass

def lw(data: InstructionData): pass

def sw(data: InstructionData): pass

# J types

def j(data: InstructionData):
    # PC=JumpAddr
    cpu.PC = data["address"]

def jal(data: InstructionData):
    # R[31]=PC+8;PC=JumpAddr
    cpu.RF[31] = cpu.PC + 8
    cpu.PC = data["address"]


FUNCT_TO_R_TYPE: dict[np.uint32, Callable[[InstructionData], None]] = {
    0x20: add,    # add
    0x21: addu,   # addu
    0x22: sub,    # sub
    0x23: subu,   # subu
    0x24: and_,   # and
    0x25: or_,    # or
    0x26: xor,    # xor
    0x27: nor,    # nor
    0x00: sll,    # sll
    0x02: srl,    # srl
    0x03: sra,    # sra
    0x2a: slt,    # slt
    0x2b: sltu,   # sltu
    0x08: jr,     # jr
    0x0c: syscall # syscall
}

OP_TO_I_TYPE: dict[np.uint32, Callable[[InstructionData], None]] = {
    0x08: addi,  # addi
    0x09: addiu, # addiu
    0x0c: andi,  # andi
    0x0d: ori,   # ori
    0x0e: xori,  # xori
    0x04: beq,   # beq
    0x05: bne,   # bne
    0x0b: slti,  # slti
    0x23: lw,    # lw
    0x2b: sw,    # sw
    0x0f: lui,   # lui
}

OP_TO_J_TYPE: dict[np.uint32, Callable[[InstructionData], None]] = {
    0x02: j,
    0x03: jal,
}

def execute(data: InstructionData):
    if data["instr_type"] == "R":
        FUNCT_TO_R_TYPE[data["funct"]](data=data)
    elif data["instr_type"] == "I":
        OP_TO_I_TYPE[data["opcode"]](data=data)
    else:
        OP_TO_J_TYPE[data["opcode"]](data=data)
        pass

R_TYPES = ["add", "addu", "sub", "subu", "and", "or", "xor", "nor", "sll", "srl", "sra", "slt", "sltu", "jr"]
I_TYPES = ["addi", "addiu", "andi", "ori", "xori", "beq", "bne", "slti", "lw", "sw"]
J_TYPES = ["j", "jal"]