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

# test_decode()
test_add()