import os
import glob


class Simulator:
    # Initialize simulator
    def __init__(self, instructions, stack_size=10, register_size=10, debug=False):
        self.stack_size = stack_size
        self.register_size = register_size
        self.operand_stack = []
        self.register_set = [None] * register_size
        self.pc = 0
        self.instructions = instructions
        self.debug = debug

    # Load constant
    def ldc(self, num):
        if len(self.operand_stack) >= self.stack_size:
            return "Stack Overflow"

        self.operand_stack.append(num)

    # Store in register
    def istore(self, num):
        if num < 0 or num >= self.register_size:
            return "Invalid register index"

        if not self.operand_stack:
            return "Stack Underflow"

        self.register_set[num] = self.operand_stack.pop()

    # Load from register
    def iload(self, num):
        if num < 0 or num >= self.register_size:
            return "Invalid register index"

        if len(self.operand_stack) >= self.stack_size:
            return "Stack Overflow"

        if self.register_set[num] is None:
            return "Register not initialized"

        self.operand_stack.append(self.register_set[num])

    # Addition
    def iadd(self):
        if len(self.operand_stack) < 2:
            return "Stack Underflow"

        a = self.operand_stack.pop()
        b = self.operand_stack.pop()
        self.operand_stack.append(b + a)

    # Subtraction
    def isub(self):
        if len(self.operand_stack) < 2:
            return "Stack Underflow"

        a = self.operand_stack.pop()
        b = self.operand_stack.pop()
        self.operand_stack.append(b - a)

    # Multiplication
    def imul(self):
        if len(self.operand_stack) < 2:
            return "Stack Underflow"

        a = self.operand_stack.pop()
        b = self.operand_stack.pop()
        self.operand_stack.append(b * a)

    # Division
    def idiv(self):
        if len(self.operand_stack) < 2:
            return "Stack Underflow"

        a = self.operand_stack.pop()
        b = self.operand_stack.pop()

        if a == 0:
            return "Division by zero"

        self.operand_stack.append(int(b / a))

    # Branch if equal to zero
    def ifeq(self, target):
        if not self.operand_stack:
            return "Stack Underflow"

        value = self.operand_stack.pop()

        if value == 0:
            self.pc = target
        else:
            self.pc += 1

    # Branch if less than zero
    def iflt(self, target):
        if not self.operand_stack:
            return "Stack Underflow"

        value = self.operand_stack.pop()

        if value < 0:
            self.pc = target
        else:
            self.pc += 1

    # Branch if greater than zero
    def ifgt(self, target):
        if not self.operand_stack:
            return "Stack Underflow"

        value = self.operand_stack.pop()

        if value > 0:
            self.pc = target
        else:
            self.pc += 1

    # Read input
    def read(self):
        if len(self.operand_stack) >= self.stack_size:
            return "Stack Overflow"

        value = int(input("Enter the number: "))
        self.operand_stack.append(value)

    # Print stack value
    def print_value(self):
        if not self.operand_stack:
            return "Stack Underflow"

        value = self.operand_stack.pop()
        print(value)

    # Execute instructions
    def execute(self):
        while self.pc < len(self.instructions):
            instruction = self.instructions[self.pc][0]

            if instruction == "ldc":
                result = self.ldc(int(self.instructions[self.pc][1]))

            elif instruction == "istore":
                result = self.istore(int(self.instructions[self.pc][1]))

            elif instruction == "iload":
                result = self.iload(int(self.instructions[self.pc][1]))

            elif instruction == "iadd":
                result = self.iadd()

            elif instruction == "isub":
                result = self.isub()

            elif instruction == "imul":
                result = self.imul()

            elif instruction == "idiv":
                result = self.idiv()

            elif instruction == "ifeq":
                result = self.ifeq(int(self.instructions[self.pc][1]))
                if result:
                    print(result)
                    break
                continue

            elif instruction == "iflt":
                result = self.iflt(int(self.instructions[self.pc][1]))
                if result:
                    print(result)
                    break
                continue

            elif instruction == "ifgt":
                result = self.ifgt(int(self.instructions[self.pc][1]))
                if result:
                    print(result)
                    break
                continue

            elif instruction == "read":
                result = self.read()

            elif instruction == "print":
                result = self.print_value()

            else:
                result = "Unknown instruction: " + instruction

            if result:
                print(result)
                break

            self.pc += 1

            if self.debug:
                print("Instruction:", instruction)
                print("Next PC:", self.pc)
                print("Stack:", self.operand_stack)
                print("Registers:", self.register_set)
                print()


# Choose instruction file
def choose_input_file():
    """
    Lets the user pick which bytecode program to run. Any .txt file in the
    current directory is offered as a choice, plus the option to type a
    custom path. This means multiple programs can live side by side
    (e.g. add.txt, subtract.txt, minmax.txt) and the user picks one per run.
    """
    txt_files = sorted(glob.glob("*.txt"))

    if txt_files:
        print("Available instruction files:")
        for i, filename in enumerate(txt_files, start=1):
            print(f"  {i}. {filename}")
        print(f"  {len(txt_files) + 1}. Enter a custom file path")

        while True:
            choice = input("Select a file by number: ").strip()

            if choice.isdigit():
                choice_num = int(choice)

                if 1 <= choice_num <= len(txt_files):
                    return txt_files[choice_num - 1]

                if choice_num == len(txt_files) + 1:
                    return prompt_for_custom_path()

            print("Invalid selection. Please try again.")
    else:
        print("No .txt files found in the current directory.")
        return prompt_for_custom_path()


# Get custom file path
def prompt_for_custom_path():
    while True:
        path = input("Enter the path to your instruction file: ").strip()

        if os.path.isfile(path):
            return path

        print(f"File not found: {path}")


# Choose stack size
def choose_stack_size():
    while True:
        raw = input("Enter operand stack size (press Enter for default 10): ").strip()

        if raw == "":
            return 10

        if raw.isdigit() and int(raw) > 0:
            return int(raw)

        print("Please enter a positive whole number.")


# Choose register size
def choose_register_size():
    while True:
        raw = input("Enter register set size (press Enter for default 10): ").strip()

        if raw == "":
            return 10

        if raw.isdigit() and int(raw) > 0:
            return int(raw)

        print("Please enter a positive whole number.")


# Load instructions
def load_instructions(filepath):
    instructions = []

    with open(filepath, "r") as file:
        for line in file:
            line = line.strip()
            if line:
                instructions.append(line.split())

    return instructions


if __name__ == "__main__":
    input_file = choose_input_file()
    stack_size = choose_stack_size()
    register_size = choose_register_size()

    instructions = load_instructions(input_file)

    s = Simulator(instructions, stack_size=stack_size, register_size=register_size, debug=False)

    print(f"\nLoaded {len(instructions)} instruction(s) from '{input_file}'")
    print(f"Stack size: {stack_size}")
    print(f"Register set size: {register_size}")
    print(s.instructions)
    print()

    s.execute()

    print("Final Stack:", s.operand_stack)
    print("Final Registers:", s.register_set)
