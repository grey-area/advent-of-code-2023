from pathlib import Path
import re


def parse_line(line):
    digits = re.findall(r"\d", line)
    number = int(digits[0] + digits[-1])
    return number


if __name__ == "__main__":
    lines = Path("input.txt").read_text().splitlines()

    total = sum(parse_line(line) for line in lines)
    print(total)