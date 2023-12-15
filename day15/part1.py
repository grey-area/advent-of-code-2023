from pathlib import Path


def hash(text):
    current_value = 0
    for character in text:
        current_value += ord(character)
        current_value *= 17
        current_value %= 256
    return current_value


if __name__ == "__main__":
    instructions = Path("input.txt").read_text().split(",")
    answer = sum(hash(instruction) for instruction in instructions)
    print(answer)