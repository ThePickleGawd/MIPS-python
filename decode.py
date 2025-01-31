
def get_instr_type(OP):
    return "R"

def decode(instr):
    data = {
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
        data["immediate"] = instr & 0x7FFF
    else:
        # 11-14: rd
        # 6-10: shamt
        # 0-5: funct
        data["rd"] = (instr >> 11) & 0x1F
        data["shamt"] = (instr >> 6) & 0x1F
        data["funct"] = instr & 0x1F

    return data