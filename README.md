# MIPS Python Interpreter

The first project of CCS 1B: Computer Programming and Organization.

## Overview

This is a simple MIPS interpreter written in Python that simulates a MIPS CPU by executing machine code instructions. The interpreter follows a fetch-decode-execute cycle and supports basic MIPS instructions.

```python
# List of supported instructions
R_TYPES = ["add", "addu", "sub", "subu", "and", "or", "xor", "nor", "sll", "srl", "sra", "slt", "sltu", "jr", "syscall"]
I_TYPES = ["addi", "addiu", "andi", "ori", "xori", "beq", "bne", "slti", "lw", "sw", "lui"]
J_TYPES = ["j", "jal"]
```

### Files and Responsibilities

- **`main.py`** - Implements the control loop that performs the fetch-decode-execute cycle.
- **`cpu.py`** - Stores the state of the CPU, including registers, program counter (PC), and instructions.
- **`functions.py`** - Defines execution functions and maps opcodes/function codes to the appropriate operations.
- **`decode.py`** - Converts hexadecimal instructions into an `InstructionData` type for processing.
- **`tests.py`** - Contains unit tests to verify correctness of the interpreter.

## Running the Interpreter

Install requirements:

```bash
pip install numpy
```

To execute a MIPS program:

1. Place a compiled MIPS binary (`.out` file) in `input/`. You can run `spim -assemble file.asm` to generate these.
2. Modify `main.py` to set input file path and verbosity.
3. Run:
   ```bash
   python main.py
   ```

## Tests

```bash
python tests.py
```
