# Advent of code day 17, Chronospatial Computer.
# https://adventofcode.com/2024/day/17

from icecream import ic

class Computer:

    def __init__(self, input_str: str):
        data_str, prog_str = input_str.split('\n\n')

        for pos, line in enumerate(data_str.split('\n')):
            pieces = line.split(' ')
            v = int(pieces[2])

            if 'A' in pieces[1]:
                self.a = v
            elif 'B' in pieces[1]:
                self.b = v
            else:
                self.c = v

        self.code = [int(n) for n in prog_str.replace('Program: ', '').split(',')]
        self.program = {}
        for a, c in enumerate(self.code):
            self.program[a] = c

        self.ip = 0
        self.output = ''

    def opcode_to_inst(self, op: int) -> tuple:
        instruction = {0: ('adv', 'combo', self.adv),
                       1: ('bxl', 'literal', self.bxl),
                       2: ('bst', 'combo', self.bst),
                       3: ('jnz', 'literal', self.jnz),
                       4: ('bxc', '-', self.bxc),
                       5: ('out', 'combo', self.out),
                       6: ('bdv', 'combo', self.bdv),
                       7: ('cdv', 'combo', self.cdv)}
        return instruction[op]

    def render(self):
        print('-' * 20)
        print(f'A: {self.a}, B:{self.b}, C:{self.c}')
        print(f'ip: {self.ip}')
        print(f'output: {self.output}')

        op = 0
        for i in range(len(self.program)):
            if i == self.ip + 1:
                ip_label = '> '
            else:
                ip_label = '  '

            if i % 2 == 0:
                op = self.program[i]
            else:
                opcode, _, _ = self.opcode_to_inst(op)
                print(f'{ip_label}{i}: {op}, {self.program[i]}, {opcode}')

    def operand_val(self, operand_type: str, operand: int) -> int:
        if operand_type == 'literal':
            return operand

        # Not a literal, so must be a combo operand.

        # Combo operands 0 through 3 represent literal values 0 through 3.
        if operand <= 3:
            return operand

        # Combo operand 4 represents the value of register A.
        # Combo operand 5 represents the value of register B.
        # Combo operand 6 represents the value of register C.
        lookup = {4: self.a,
                  5: self.b,
                  6: self.c}
        return lookup[operand]

    def adv(self, operand: int):
        # The adv instruction (opcode 0) performs division. The numerator is the value in the A register. The
        # denominator is found by raising 2 to the power of the instruction's combo operand. (So, an operand of 2 would
        # divide A by 4 (2^2); an operand of 5 would divide A by 2^B.) The result of the division operation is
        # truncated to an integer and then written to the A register.
        self.a = int(self.a / (2 ** operand))
        return False

    def bdv(self, operand: int):
        # The bdv instruction (opcode 6) works exactly like the adv instruction except that the result is stored in the
        # B register. (The numerator is still read from the A register.)
        self.b = int(self.a / (2 ** operand))
        return False

    def cdv(self, operand: int):
        # The cdv instruction (opcode 7) works exactly like the adv instruction except that the result is stored in the
        # C register. (The numerator is still read from the A register.)
        self.c = int(self.a / (2 ** operand))
        return False

    def bxl(self, operand: int):
        # The bxl instruction (opcode 1) calculates the bitwise XOR of register B and the instruction's literal operand,
        # then stores the result in register B.
        self.b = self.b ^ operand
        return False

    def bst(self, operand: int):
        # The bst instruction (opcode 2) calculates the value of its combo operand modulo 8 (thereby keeping only its
        # lowest 3 bits), then writes that value to the B register.
        self.b = operand % 8
        return False

    def jnz(self, operand: int) -> bool:
        # The jnz instruction (opcode 3) does nothing if the A register is 0. However, if the A register is not zero, it
        # jumps by setting the instruction pointer to the value of its literal operand; if this instruction jumps, the
        # instruction pointer is not increased by 2 after this instruction.
        if self.a == 0:
            return False                # No jump.
        self.ip = operand
        return True                     # Did a jump.

    def bxc(self, operand: int):
        # The bxc instruction (opcode 4) calculates the bitwise XOR of register B and register C, then stores the
        # result in register B. (For legacy reasons, this instruction reads an operand but ignores it.)
        self.b = self.b ^ self.c
        return False

    def out(self, operand: int):
        # The out instruction (opcode 5) calculates the value of its combo operand modulo 8, then outputs that value.
        # (If a program outputs multiple values, they are separated by commas.)
        new_result = str(operand % 8)
        if self.output == '':
            self.output = new_result
        else:
            self.output = self.output + ',' + new_result
        return False

    def tick(self):
        operator = self.program[self.ip]
        encoded_operand = self.program[self.ip + 1]
        opcode, operand_type, method = self.opcode_to_inst(operator)
        operand = self.operand_val(operand_type, encoded_operand)
        # ic(operator, encoded_operand, opcode, operand_type, operand)
        jumped = method(operand)
        if not jumped:
            self.ip += 2

    def run(self):
        self.render()
        # If the computer tries to read an opcode past the end of the program, it instead halts.
        while self.ip <= len(self.program):
            self.tick()
            self.render()

with open('input.txt', 'r') as file:
    input_str = file.read()

c = Computer(input_str)
c.run()
# c.render()
# c.tick()
# c.render()