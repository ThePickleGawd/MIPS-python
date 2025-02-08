from typing import Callable
import numpy as np
from decode import InstructionData
from cpu import cpu

# R types

def add(data: InstructionData):
    # R[rd] = R[rs] + R[rt]
    cpu.set_rf(data["rd"], cpu.RF[data["rs"]] + cpu.RF[data["rt"]])

def addu(data: InstructionData):
    # R[rd] = R[rs] + R[rt]
    cpu.set_rf(data["rd"], cpu.RF[data["rs"]] + cpu.RF[data["rt"]])

def sub(data: InstructionData):
    # R[rd] = R[rs] - R[rt]
    cpu.set_rf(data["rd"], cpu.RF[data["rs"]] - cpu.RF[data["rt"]])

def subu(data: InstructionData):
    # R[rd] = R[rs] - R[rt]
    cpu.set_rf(data["rd"], cpu.RF[data["rs"]] - cpu.RF[data["rt"]])

def and_(data: InstructionData):
    # R[rd] = R[rs] & R[rt]
    cpu.set_rf(data["rd"], cpu.RF[data["rs"]] & cpu.RF[data["rt"]])

def or_(data: InstructionData):
    # R[rd] = R[rs] | R[rt]
    cpu.set_rf(data["rd"], cpu.RF[data["rs"]] | cpu.RF[data["rt"]])

def xor(data: InstructionData):
    # R[rd] = R[rs] ^ R[rt]
    cpu.set_rf(data["rd"], cpu.RF[data["rs"]] ^ cpu.RF[data["rt"]])
    
def nor(data: InstructionData):
    # R[rd] = ~(R[rs] | R[rt])
    cpu.set_rf(data["rd"], ~(cpu.RF[data["rs"]] | cpu.RF[data["rt"]]))

def sll(data: InstructionData):
    # R[rd] = R[rt] << shamt
    cpu.set_rf(data["rd"], cpu.RF[data["rt"]] << data["shamt"])

def srl(data: InstructionData):
    # R[rd] = R[rt] >> shamt
    # Note: Python does arithmetic shift, so we need to simulat logical shift
    value = cpu.RF[data["rt"]]
    if value < 0:
        value += 2**32
    cpu.set_rf(data["rd"], (value >> data["shamt"]))

def sra(data: InstructionData):
    # R[rd] = R[rt] >> shamt (preserve original sign)
    cpu.set_rf(data["rd"], (cpu.RF[data["rt"]] >> data["shamt"]))


def slt(data: InstructionData):
    # R[rd] = (R[rs] < R[rt]) ? 1 : 0
    signed_rs = cpu.RF[data["rs"]].astype(np.int32)
    signed_rt = cpu.RF[data["rt"]].astype(np.int32)

    cpu.set_rf(data["rd"], 1 if (signed_rs < signed_rt) else 0)

def sltu(data: InstructionData):
    # R[rd] = (R[rs] < R[rt]) ? 1 : 0
    cpu.set_rf(data["rd"], 1 if (cpu.RF[data["rs"]] < cpu.RF[data["rt"]]) else 0)

def jr(data: InstructionData):
    # PC=R[rs]
    cpu.PC = cpu.RF[data["rs"]]

def syscall(data): 
    v0 = cpu.RF[2]
    a0 = cpu.RF[4]

    match v0:
        case 1:
            print(a0)
            return

        case 4:
            # Print string
            # Get word from DMEM. Read char one by one until 0x00
            mem_idx = cpu.addr_to_dmem_idx(a0)
            printStr = ""
            done = False
            while not done and mem_idx < len(cpu.DMEM):
                word = cpu.DMEM[mem_idx]
                for i in range(4):
                    byte = (word >> (i * 8)) & 0xFF  # Extract byte i

                    if byte == 0x00:
                        done = True
                        break

                    printStr += chr(byte)

                mem_idx += 1

            print(printStr)
            
            return

        case 5:
            cpu.RF[2] = int(input())
            return

        case 10:
            # Hack that may work??
            cpu.finished = lambda: True
            return

# I types

def addi(data: InstructionData):
    # R[rt] = R[rs] + SignExtImm
    cpu.set_rf(data["rt"], cpu.RF[data["rs"]] + np.int16(data["immediate"]))

def addiu(data: InstructionData):
    # R[rt] = R[rs] + SignExtImm
    cpu.set_rf(data["rt"], cpu.RF[data["rs"]] + data["immediate"])

def andi(data: InstructionData):
    # R[rt] = R[rs] & ZeroExtImm
    cpu.set_rf(data["rt"], cpu.RF[data["rs"]] & data["immediate"])

def ori(data: InstructionData):
    # R[rt] = R[rs] | ZeroExtImm
    cpu.set_rf(data["rt"], cpu.RF[data["rs"]] | data["immediate"])

def xori(data: InstructionData):
    # R[rt] = R[rs] ^ ZeroExtImm
    cpu.set_rf(data["rt"], cpu.RF[data["rs"]] ^ data["immediate"])

def lui(data: InstructionData):
    # R[rt] = Immediate << 16
    cpu.set_rf(data["rt"], data["immediate"] << 16)


def beq(data: InstructionData):
    # if(R[rs]==R[rt]) PC=PC+4+BranchAddr
    # BranchAddr = { 14{immediate[15]}, immediate, 2’b0 }
    if cpu.RF[data["rs"]] == cpu.RF[data["rt"]]:
        signExtended = data["immediate"]
        if data["immediate"] & (1 << 15):
            signExtended = (data["immediate"] | 0xFFFF000)
        
        branchAddr = signExtended << 2
        cpu.PC = cpu.PC + 4 + branchAddr
        

def bne(data: InstructionData):
    # if(R[rs]!=R[rt]) PC=PC+4+BranchAddr
    # BranchAddr = { 14{immediate[15]}, immediate, 2’b0 }
    if cpu.RF[data["rs"]] != cpu.RF[data["rt"]]:
        signExtended = data["immediate"]
        if data["immediate"] & (1 << 15):
            signExtended = (data["immediate"] | 0xFFFF000)
        
        branchAddr = signExtended << 2
        cpu.PC = cpu.PC + 4 + branchAddr
        print("Branching to ", cpu.PC, cpu.pc_idx())

def slti(data: InstructionData): 
    #  R[rt] = (R[rs] < SignExtImm)? 1 : 0
    cpu.set_rf(data["rt"], 1 if (cpu.RF[data["rs"]] < np.int32(data["immediate"])) else 0)

def lw(data: InstructionData):
    # R[rt] = M[R[rs]+SignExtImm]
    RF_rs = cpu.RF[data['rs']]
    signExtImm = np.int32(data["immediate"])
    cpu.set_rf(data["rt"], cpu.DMEM[cpu.addr_to_dmem_idx(RF_rs + signExtImm)])

def sw(data: InstructionData):
    # M[R[rs]+SignExtImm] = R[rt]
    RF_rs = cpu.RF[data['rs']]
    signExtImm = np.int32(data["immediate"])
    cpu.DMEM[cpu.addr_to_dmem_idx(RF_rs + signExtImm)] = cpu.RF[data["rt"]]

# J types

def j(data: InstructionData):
    # PC=JumpAddr= { PC+4[31:28], address, 2’b0 }
    cpu.PC = (cpu.PC & 0xf0000000) | (data["address"] << 2)
    

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