import numpy as np
import functions
from decode import decode, print_decoded_instr
from cpu import cpu


def test_decode():
    """
    add $t1 $t2 $t3
    Binary: 00000001010010110100100000100000
    Hex: 0x014B4820
    """
    add = np.uint32(0x014B4820)
    add_data = decode(add)
    print("====== add =====")
    print_decoded_instr(data=add_data)

    """
    addi $v0 $v1 0xffff
    Binary: 00100000011000101111111111111111
    Hex: 0x2062FFFF
    """
    addi = np.uint32(0x2062FFFF)
    addi_data = decode(addi)
    print("====== addi =====")
    print_decoded_instr(data=addi_data)

    """
    j 0xf00f
    Binary: 00001000000000001111000000001111
    Hex: 0x0800F00F
    """
    jump = np.uint32(0x0800F00F)
    jump_data = decode(jump)
    print("====== j =====")
    print_decoded_instr(data=jump_data)

def test_add():
    cpu.RF[7] = 0x00000000
    cpu.RF[8] = 0xFFFFFFFF
    cpu.RF[9] = 0x00000003
    functions.add({"rd": 7, "rs": 8, "rt": 9})
    print(format(cpu.RF[7], "08x"))

# Helper to reset registers before each test
def reset_registers():
    cpu.RF = np.zeros(32, dtype=np.uint32)
    
# R-Type Tests

def test_add():
    reset_registers()
    cpu.RF[8] = 0x7FFFFFFF  # Max positive int
    cpu.RF[9] = 0x00000001
    try:
        functions.add({"rd": 7, "rs": 8, "rt": 9})
        print("ADD: FAIL")
    except OverflowError:
        print("ADD: PASS")

def test_addu():
    reset_registers()
    cpu.RF[8] = 0xFFFFFFFF
    cpu.RF[9] = 0x00000003
    functions.addu({"rd": 7, "rs": 8, "rt": 9})
    print("ADDU: PASS" if cpu.RF[7] == 0x00000002 else "ADDU: FAIL")

def test_sub():
    reset_registers()
    cpu.RF[8] = 0x00000005
    cpu.RF[9] = 0x00000003
    functions.sub({"rd": 7, "rs": 8, "rt": 9})
    print("SUB: PASS" if cpu.RF[7] == 0x00000002 else "SUB: FAIL")

def test_and():
    reset_registers()
    cpu.RF[8] = 0b1100
    cpu.RF[9] = 0b1010
    functions.and_({"rd": 7, "rs": 8, "rt": 9})
    print("AND: PASS" if cpu.RF[7] == 0x00000008 else "AND: FAIL")

def test_or():
    reset_registers()
    cpu.RF[8] = 0b1100
    cpu.RF[9] = 0b1010
    functions.or_({"rd": 7, "rs": 8, "rt": 9})
    print("OR: PASS" if cpu.RF[7] == 0x0000000E else "OR: FAIL")

def test_xor():
    reset_registers()
    cpu.RF[8] = 0b1100
    cpu.RF[9] = 0b1010
    functions.xor({"rd": 7, "rs": 8, "rt": 9})
    print("XOR: PASS" if cpu.RF[7] == 0x00000006 else "XOR: FAIL")

def test_nor():
    reset_registers()
    cpu.RF[8] = 0b1100
    cpu.RF[9] = 0b1010
    functions.nor({"rd": 7, "rs": 8, "rt": 9})
    print("NOR: PASS" if cpu.RF[7] == 0xFFFFFFF1 else "NOR: FAIL")

def test_sll():
    reset_registers()
    cpu.RF[9] = 0b0001
    functions.sll({"rd": 7, "rt": 9, "shamt": 2})
    print("SLL: PASS" if cpu.RF[7] == 0x00000004 else "SLL: FAIL")

def test_srl():
    reset_registers()
    cpu.RF[9] = 0b1000
    functions.srl({"rd": 7, "rt": 9, "shamt": 3})
    print("SRL: PASS" if cpu.RF[7] == 0x00000001 else "SRL: FAIL")

def test_sra():
    reset_registers()
    cpu.RF[9] = 0xFFFFFFFF  # -1 in signed 32-bit
    functions.sra({"rd": 7, "rt": 9, "shamt": 1})
    print("SRA: PASS" if cpu.RF[7] == 0xFFFFFFFF else "SRA: FAIL")

def test_slt():
    reset_registers()
    cpu.RF[8] = -1 & 0xFFFFFFFF  # signed -1
    cpu.RF[9] = 1
    functions.slt({"rd": 7, "rs": 8, "rt": 9})
    print("SLT: PASS" if cpu.RF[7] == 1 else "SLT: FAIL")

def test_sltu():
    reset_registers()
    cpu.RF[8] = 0xFFFFFFFF  # Large unsigned value
    cpu.RF[9] = 1
    functions.sltu({"rd": 7, "rs": 8, "rt": 9})
    print("SLTU: PASS" if cpu.RF[7] == 0 else "SLTU: FAIL")

# I-Type Tests

def test_addi():
    reset_registers()
    cpu.RF[8] = 5
    functions.addi({"rt": 7, "rs": 8, "immediate": 3})
    print("ADDI: PASS" if cpu.RF[7] == 8 else "ADDI: FAIL")

def test_addiu():
    reset_registers()
    cpu.RF[8] = 0xFFFFFFFF
    functions.addiu({"rt": 7, "rs": 8, "immediate": 1})
    print("ADDIU: PASS" if cpu.RF[7] == 0x00000000 else "ADDIU: FAIL")

def test_andi():
    reset_registers()
    cpu.RF[8] = 0b1100
    functions.andi({"rt": 7, "rs": 8, "immediate": 0b1010})
    print("ANDI: PASS" if cpu.RF[7] == 0x00000008 else "ANDI: FAIL")

def test_ori():
    reset_registers()
    cpu.RF[8] = 0b1100
    functions.ori({"rt": 7, "rs": 8, "immediate": 0b1010})
    print("ORI: PASS" if cpu.RF[7] == 0x0000000E else "ORI: FAIL")

def test_xori():
    reset_registers()
    cpu.RF[8] = 0b1100
    functions.xori({"rt": 7, "rs": 8, "immediate": 0b1010})
    print("XORI: PASS" if cpu.RF[7] == 0x00000006 else "XORI: FAIL")

def test_beq():
    reset_registers()
    cpu.RF[8] = 5
    cpu.RF[9] = 5
    functions.beq({"rs": 8, "rt": 9, "immediate": 4})
    print("BEQ: PASS" if cpu.PC == 20 else "BEQ: FAIL")

def test_bne():
    reset_registers()
    cpu.RF[8] = 5
    cpu.RF[9] = 3
    functions.bne({"rs": 8, "rt": 9, "immediate": 4})
    print("BNE: PASS" if cpu.PC == 20 else "BNE: FAIL")

def test_slti():
    reset_registers()
    cpu.RF[8] = -1 & 0xFFFFFFFF
    functions.slti({"rt": 7, "rs": 8, "immediate": 1})
    print("SLTI: PASS" if cpu.RF[7] == 1 else "SLTI: FAIL")

def test_lw_sw():
    reset_registers()
    # Set up initial values
    base_address = 100
    value_to_store = 42

    cpu.RF[8] = base_address  # Base address
    cpu.RF[9] = value_to_store  # Value to store

    # Store word
    functions.sw({"rs": 8, "rt": 9, "immediate": 0})

    # Verify the value in DMEM
    dmem_index = cpu.addr_to_dmem_idx(base_address)
    if cpu.DMEM[dmem_index] == value_to_store:
        print("SW: PASS")
    else:
        print("SW: FAIL")

    # Load word
    functions.lw({"rs": 8, "rt": 7, "immediate": 0})

    # Verify the loaded value
    print("LW: PASS" if cpu.RF[7] == value_to_store else "LW: FAIL")

def test_lui():
    reset_registers()
    functions.lui({"rt": 7, "immediate": 0x1234})
    print("LUI: PASS" if cpu.RF[7] == 0x12340000 else "LUI: FAIL")

# J-Type Tests

def test_j():
    reset_registers()
    functions.j({"address": 0x0000000F})
    print("J: PASS" if cpu.PC == 0x0000003C else "J: FAIL")

def test_jal():
    reset_registers()
    functions.jal({"address": 0x0000000F})
    print("JAL: PASS" if cpu.PC == 0x0000003C and cpu.RF[31] == 8 else "JAL: FAIL")

# Run all tests
test_add()
test_addu()
test_sub()
test_and()
test_or()
test_xor()
test_nor()
test_sll()
test_srl()
test_sra()
test_slt()
test_sltu()

test_addi()
test_addiu()
test_andi()
test_ori()
test_xori()
test_beq()
test_bne()
test_slti()
test_lw_sw()
test_lui()

test_j()
test_jal()
