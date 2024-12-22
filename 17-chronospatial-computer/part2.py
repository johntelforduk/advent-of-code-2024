# Advent of code day 17, Chronospatial Computer.
# https://adventofcode.com/2024/day/17

from icecream import ic

class Computer:

    def __init__(self, input_str: str):
        _, prog_str = input_str.split('\n\n')

        self.code = [int(n) for n in prog_str.replace('Program: ', '').split(',')]
        self.program = {}
        self.target = ''
        for a, c in enumerate(self.code):
            self.program[a] = c
            self.target += str(c)

        self.a = 0
        self.b = 0
        self.c = 0
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
        # # if self.output == '':
        #     self.output = new_result
        # else:
        self.output += new_result
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
        # self.render()
        # If the computer tries to read an opcode past the end of the program, it instead halts.
        while self.ip < len(self.program):
            self.tick()
            # self.render()

    def reset(self):
        self.a = 0
        self.b = 0
        self.c = 0
        self.ip = 0
        self.output = ''


def solution(c:Computer, current_target: str, already_found: str) -> list:
    # For example, curr_targ: '50330', found: '3033'.
    # ic(current_target, already_found)
    ic('start of function solution', current_target, already_found)

    solutions = []

    for s in range(8 ** (len(current_target) - len(already_found))):
        c.reset()  # Reset the computer.

        oct_s = oct(s)[2:]
        a = int(already_found + oct_s, 8)
        c.a = a
        c.run()

        if c.output == current_target:
            solutions.append(oct(s)[2:])
    return solutions


# ic(solution(c=c, current_target='330', already_found='30'))
# ic(solution(c=c, current_target='330', already_found=''))

def search(c:Computer, remaining_target: str, already_found: str) -> list:
    ic('start of search func', remaining_target, already_found)

    current_target = already_found + remaining_target[-1]  # Get the last character.
    found = solution(c, current_target, already_found)
    ic(found)
    if len(found) == 0:         # This is a dead-end, so give up.
        return []

    new_remaining_target = remaining_target[:-1]  # Remove the last character from the string.

    output = []
    for f in found:
        new_already_found = already_found + f
        ic('looping found', new_remaining_target, new_already_found)

        s = search(c, new_remaining_target, new_already_found)
        output.extend(s)
    return output


with open('input.txt', 'r') as file:
    input_str = file.read()

c = Computer(input_str)
s = search(c=c, remaining_target=c.target, already_found='')
ic(s)
for each in s:                  # TODO Find the lowest one in the list.
    ic(each, int(each, 8))

ic(solution(c, '30', '3'))

#
#     ic(c.target, remaining_target, already_found, current_target)
#
# for i in range(14):
#     ic(c.target, remaining_target, already_found, current_target)
#
#     s = solution(c, current_target, already_found)
#     ic(s)   # [3]
#
#     if len(s) != 0:
#         this = s[0]
#         already_found += this
#         int(already_found, 8)
#
#     from_end = remaining_target[-1]  # Get the last character.
#     remaining_target = remaining_target[:-1]  # Remove the last character from the string.
#     current_target = from_end + current_target
#
#     ic(already_found, int(already_found, 8))

# s = search(c, current_target, already_found)
# ic(s)
# s = search(c=c, current_target='30', already_found='3')
# ic(s)       # ic| s: [0, 1, 5, 7]

# s = search(c=c, current_target='330', already_found='30')
# ic(s)       # ic| s: [3, 5]
#
# s = search(c=c, current_target='0330', already_found='303')
# ic(s)       # ic| s: [3]
#
# s = search(c=c, current_target='50330', already_found='3033')
# ic(s)       # [0]
#
# s = search(c=c, current_target='550330', already_found='30330')
# ic(s)       # [0, 4, 6, 7]
#
# s = search(c=c, current_target='3550330', already_found='303300')
# ic(s)       # [0, 5]
#
# s = search(c=c, current_target='43550330', already_found='3033000')
# ic(s)       # []
#
# s = search(c=c, current_target='43550330', already_found='3033000')
# ic(s)       # []
#


# while len(target) > 12:                 # TODO Change back to 0!!!
#     from_end = target[-1]  # Get the last character
#     target = target[:-1]   # Remove the last character from the string
#     current_target = from_end + current_target
#
#     ic(target, current_target)
#
#     s = search(c, current_target, found)
#
#     if len(s) != 0:
#         low_s = oct(s[0])[2:]           # Convert denery int solution to octal and remove the prefix.
#         found = found + low_s
#
# ic(target, current_target, found, int(found, 8))
