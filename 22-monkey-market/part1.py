# Advent of code day 22, Monkey Market.
# https://adventofcode.com/2024/day/22

from icecream import ic


def mix(value: int, secret: int) -> int:
    # To mix a value into the secret number, calculate the bitwise XOR of the given value and the secret number.
    # Then, the secret number becomes the result of that operation.
    return value ^ secret

# If the secret number is 42 and you were to mix 15 into the secret number, the secret number would become 37.
assert mix(15, 42) == 37


def prune(secret: int) -> int:
    # To prune the secret number, calculate the value of the secret number modulo 16777216.
    # Then, the secret number becomes the result of that operation.
    return secret % 16777216

# If the secret number is 100000000 and you were to prune the secret number, the secret number would become 16113920.
assert prune(100000000) == 16113920


def iterate(secret: int) -> int:
    # Calculate the result of multiplying the secret number by 64. Then, mix this result into the secret number.
    # Finally, prune the secret number.
    mult64 = secret * 64
    secret = mix(mult64, secret)
    secret = prune(secret)

    # Calculate the result of dividing the secret number by 32. Round the result down to the nearest integer.
    # Then, mix this result into the secret number. Finally, prune the secret number.
    div32 = secret // 32
    secret = mix(div32, secret)
    secret = prune(secret)

    # Calculate the result of multiplying the secret number by 2048. Then, mix this result into the secret number.
    # Finally, prune the secret number.
    mult2048 = secret * 2048
    secret = mix(mult2048, secret)
    secret = prune(secret)

    return secret


assert iterate(123) == 15887950
assert iterate(15887950) == 16495136

with open('input.txt', 'r') as file:
    buyers_str = file.read()

total = 0
for buyer_seed in [int(line) for line in buyers_str.split('\n')]:
    output = buyer_seed
    for i in range(2000):
        output = iterate(output)
    ic(buyer_seed, output)
    total += output
ic(total)
