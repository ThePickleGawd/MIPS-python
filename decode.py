import numpy as np
from typing import Optional, TypedDict

class InstructionData(TypedDict):
    instr_type: str
    opcode: np.uint8  # 6 bits
    rs: Optional[np.uint8]  # 5 bits
    rt: Optional[np.uint8]  # 5 bits
    rd: Optional[np.uint8]  # 5 bits
    shamt: Optional[np.uint8]  # 5 bits
    funct: Optional[np.uint8]  # 6 bits
    immediate: Optional[np.uint16]  # 16 bits
    address: Optional[np.uint32]  # 26 bits

OP_TO_INSTRUCTION = {
    """
    TODO:
    OP_CODE: { "func": function, "type": type } # add
    OP_CODE: { "func": function, "type": type } # addi
    ...
    """
}

R_TYPES = ["add", "addu", "sub", "subu", "and", "or", "xor", "nor", "sll", "srl", "sra", "slt", "sltu", "jr"]
I_TYPES = ["addi", "addiu", "andi", "ori", "xori", "beq", "bne", "slti", "lw", "sw"]
J_TYPES = ["j"]

def get_instr_type(opcode):
    print("Assuming Instruction is I type")
    return "I"

def decode(instr: np.uint32) -> InstructionData:
    data: InstructionData = {
        "instr_type": "J", 
        "opcode": None,
        "rs": None,
        "rt": None,
        "rd": None,
        "shamt": None,
        "funct": None,
        "immediate": None,
        "address": None
    }

    # Fetch opcode and instruction type
    data["opcode"] = instr >> 26
    data["instr_type"] = get_instr_type(data["opcode"])

    if data["instr_type"] == "J":
        # bits 0-25 are the address to jump to
        data["address"] = instr & 0x3FFFFFF
        return data
    
    # Get rs (21-25) and rt (16-20)
    data["rs"] = (instr >> 21) & 0x1F
    data["rt"] = (instr >> 16) & 0x1F

    if data["instr_type"] == "I":
        # bits 0-15 are the immediate
        data["immediate"] = instr & 0xFFFF
    else:
        # 11-14: rd
        # 6-10: shamt
        # 0-5: funct
        data["rd"] = (instr >> 11) & 0x1F
        data["shamt"] = (instr >> 6) & 0x1F
        data["funct"] = instr & 0x1F

    return data

def print_decoded_instr(data):
    print("opcode:   ", format(data["opcode"], "06b"))  # 6-bit opcode

    if data["instr_type"] == "J":
        print("address:  ", format(data["address"], "026b"))  # 26-bit address
    elif data["instr_type"] == "I":
        print("rs:       ", format(data["rs"], "05b"))  # 5-bit rs
        print("rt:       ", format(data["rt"], "05b"))  # 5-bit rt
        print("immediate:", format(data["immediate"], "016b"))  # 16-bit immediate
    else:  # R-type instruction
        print("rs:       ", format(data["rs"], "05b"))  # 5-bit rs
        print("rt:       ", format(data["rt"], "05b"))  # 5-bit rt
        print("rd:       ", format(data["rd"], "05b"))  # 5-bit rd
        print("shamt:    ", format(data["shamt"], "05b"))  # 5-bit shamt
        print("funct:    ", format(data["funct"], "06b"))  # 6-bit function code
