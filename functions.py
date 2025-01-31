from typing import Callable
import numpy as np
from decode import InstructionData
from cpu import cpu


# R types

def add(data: InstructionData):
    # R[rd] = R[rs] + R[rt]
    cpu.RF[data["rd"]] = cpu.RF[data["rs"]] + cpu.RF[data["rt"]]

def addu(data: InstructionData): pass

def sub(data: InstructionData): pass

def subu(data: InstructionData): pass

def and_(data: InstructionData): pass

def or_(data: InstructionData): pass

def xor(data: InstructionData): pass

def nor(data: InstructionData): pass

def sll(data: InstructionData): pass

def srl(data: InstructionData): pass

def sra(data: InstructionData): pass

def slt(data: InstructionData): pass

def sltu(data: InstructionData): pass

def jr(data: InstructionData): pass

# I types

def addi(data: InstructionData): pass

def addiu(data: InstructionData): pass

def andi(data: InstructionData): pass

def ori(data: InstructionData): pass

def xori(data: InstructionData): pass

def beq(data: InstructionData): pass

def bne(data: InstructionData): pass

def slti(data: InstructionData): pass

def lw(data: InstructionData): pass

def sw(data: InstructionData): pass


FUNCT_TO_R_TYPE: dict[np.uint32, Callable[[InstructionData], None]] = {
    0x20: add,   # add
    0x21: addu,  # addu
    0x22: sub,   # sub
    0x23: subu,  # subu
    0x24: and_,  # and
    0x25: or_,   # or
    0x26: xor,   # xor
    0x27: nor,   # nor
    0x00: sll,   # sll
    0x02: srl,   # srl
    0x03: sra,   # sra
    0x2a: slt,   # slt
    0x2b: sltu,  # sltu
    0x08: jr,    # jr
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
}

def execute(data: InstructionData):
    if data["instr_type"] == "R":
        FUNCT_TO_R_TYPE[data["funct"]]()
    elif data["instr_type"] == "I":
        OP_TO_I_TYPE[data["opcode"]]()
    else:
        # TODO: Jump PC to data["immediate"]
        pass

R_TYPES = ["add", "addu", "sub", "subu", "and", "or", "xor", "nor", "sll", "srl", "sra", "slt", "sltu", "jr"]
I_TYPES = ["addi", "addiu", "andi", "ori", "xori", "beq", "bne", "slti", "lw", "sw"]
J_TYPES = ["j"]