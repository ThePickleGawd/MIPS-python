import numpy as np
from decode import decode, print_decoded_instr


def test_decode():
    """
    add $t1 $t2 $t3
    Binary: 00000001010010110100100000100000
    Hex: 0x014B4820
    """
    add = np.uint32(0x2062FFFF)
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

test_decode()