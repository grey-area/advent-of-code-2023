from pathlib import Path
import re


def parse_digit(digit):
    words = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

    if digit.isdigit():
        return digit
    else:
        return str(words.index(digit) + 1)


def parse_line(line):
    # A capturing group inside a lookahead group as a hacky way to get overlapping matches
    pattern = r"(?=(\d|one|two|three|four|five|six|seven|eight|nine))"
    digits = re.findall(pattern, line)

    number = int(parse_digit(digits[0]) + parse_digit(digits[-1]))
    return number


if __name__ == "__main__":
    lines = Path("input.txt").read_text().splitlines()

    total = sum(parse_line(line) for line in lines)
    print(total)