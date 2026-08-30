# Java Bytecode Simulator

A lightweight Python simulator for executing a small subset of Java Virtual Machine (JVM) bytecode-style instructions.

The project models a stack-based virtual machine using an **operand stack**, **register/local-variable set**, and **program counter (PC)**. Bytecode programs are written as simple `.txt` files and executed instruction by instruction.

## Features

* Stack-based instruction execution
* Configurable operand stack size
* Configurable register set size
* Automatic discovery of `.txt` bytecode programs
* Support for custom instruction-file paths
* Arithmetic operations
* Conditional branching
* User input and output
* Stack overflow and underflow detection
* Invalid register detection
* Uninitialized register detection
* Division-by-zero detection
* Optional debug mode
* Final stack and register-state display

## Requirements

* Python 3.x
* No external libraries required

## Supported Instructions

| Instruction | Description                                                             |
| ----------- | ----------------------------------------------------------------------- |
| `ldc n`     | Push integer constant `n` onto the operand stack                        |
| `istore n`  | Pop the top stack value and store it in register `n`                    |
| `iload n`   | Push the value stored in register `n` onto the operand stack            |
| `iadd`      | Pop two values and push their sum                                       |
| `isub`      | Pop two values and push their difference                                |
| `imul`      | Pop two values and push their product                                   |
| `idiv`      | Pop two values and push their integer quotient                          |
| `ifeq n`    | Pop a value and jump to instruction index `n` if it equals `0`          |
| `iflt n`    | Pop a value and jump to instruction index `n` if it is less than `0`    |
| `ifgt n`    | Pop a value and jump to instruction index `n` if it is greater than `0` |
| `read`      | Read an integer from the user and push it onto the stack                |
| `print`     | Pop and display the top value of the operand stack                      |

## Architecture

The simulator contains four main components.

### Operand Stack

The operand stack stores temporary values used during calculations.

Its maximum size can be selected when the program starts.

Example:

```text
ldc 10
ldc 20
iadd
```

Stack changes:

```text
[] → [10] → [10, 20] → [30]
```

### Register Set

Registers store local values during execution.

The register-set size can also be selected when the simulator starts.

Example:

```text
ldc 25
istore 0
iload 0
```

Result:

```text
Register 0 = 25
Stack = [25]
```

### Program Counter

The program counter (`pc`) identifies the instruction currently being executed.

Normal instructions move to the next instruction.

Branch instructions can directly change the PC:

```text
ifeq
iflt
ifgt
```

Branch targets in this simulator are treated as **absolute instruction indexes**.

### Fetch-Decode-Execute Cycle

The `execute()` method repeatedly:

1. Fetches the instruction at the current PC
2. Identifies the opcode
3. Executes the appropriate instruction method
4. Updates the operand stack or registers
5. Updates the program counter
6. Continues until the program finishes or an error occurs

## Running the Simulator

Run:

```bash
python instruction.py
```

The simulator automatically finds `.txt` files in the current directory.

Example:

```text
Available instruction files:
  1. matrix2.txt
  2. minmax.txt
  3. sort.txt
  4. Enter a custom file path
```

Select a program by entering its number.

The simulator then asks for the operand stack size:

```text
Enter operand stack size (press Enter for default 10):
```

Press Enter to use `10`, or enter another positive integer.

Next, select the register-set size:

```text
Enter register set size (press Enter for default 10):
```

The selected bytecode program is then loaded and executed.

## Sample Programs

The repository contains three example bytecode programs.

### `minmax.txt`

Reads three integers from the user and determines their minimum and maximum values.

The program uses:

* `read`
* `istore`
* `iload`
* `isub`
* `iflt`
* `ifgt`
* `ifeq`
* `print`

Example input:

```text
10
5
20
```

Expected output:

```text
5
20
```

### `sort.txt`

Reads three integers and prints them in ascending order.

The program compares values using subtraction and conditional branch instructions, then swaps register values when required.

Example input:

```text
33
22
11
```

Expected output:

```text
11
22
33
```

### `matrix2.txt`

Reads two `2 × 2` matrices and performs element-wise matrix addition.

The eight input values represent:

```text
Matrix A

a b
c d

Matrix B

e f
g h
```

The program prints:

```text
a + e
b + f
c + g
d + h
```

Example input:

```text
1
2
3
4
5
6
7
8
```

Equivalent matrices:

```text
A = [1 2]
    [3 4]

B = [5 6]
    [7 8]
```

Output:

```text
6
8
10
12
```

## Debug Mode

The simulator supports optional debugging.

When enabled, it can display:

```text
Instruction: iadd
Next PC: 7
Stack: [30]
Registers: [10, 20, None, ...]
```

Debug mode can be enabled when creating the simulator:

```python
s = Simulator(
    instructions,
    stack_size=stack_size,
    register_size=register_size,
    debug=True
)
```

Set `debug=False` for normal execution.

## Error Handling

The simulator checks for:

* Stack Overflow
* Stack Underflow
* Invalid register index
* Uninitialized register
* Division by zero
* Unknown instructions

Execution stops when an error is encountered.

## Project Structure

```text
Java-bytecode-simulator/
│
├── instruction.py
├── minmax.txt
├── sort.txt
├── matrix2.txt
├── README.md
└── LICENSE
```

Additional `.txt` programs can be added to the same folder. They will automatically appear in the file-selection menu.

## Limitations

This project implements only a small subset of JVM-style bytecode.

It currently does not support:

* `long`
* `float`
* `double`
* Object references
* Method calls
* Real `.class` file parsing
* Full JVM bytecode verification

Programs are written using human-readable text instructions rather than binary JVM `.class` files.

## Purpose

This project is designed to demonstrate important JVM execution concepts, including:

* Operand stacks
* Local variables/registers
* Program counters
* Arithmetic instructions
* Conditional branching
* Stack-based computation
* Input and output operations

