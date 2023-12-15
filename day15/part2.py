from pathlib import Path
import re
from dataclasses import dataclass


def hash(text):
    current_value = 0
    for character in text:
        current_value += ord(character)
        current_value *= 17
        current_value %= 256
    return current_value


@dataclass
class Lens:
    focal_length: int
    index: int


class Box:
    def __init__(self):
        self.lenses = {}
        self.index = 0

    def remove_lens(self, name):
        if name in self.lenses:
            del self.lenses[name]

    def add_lens(self, name, focal_length):
        if name in self.lenses:
            self.lenses[name].focal_length = focal_length
        else:
            self.lenses[name] = Lens(focal_length, self.index)
            self.index += 1

    def apply_instruction(self, name, instruction):
        inst_type, arg = instruction[0], instruction[1:]
        if inst_type == "-":
            self.remove_lens(name)
        else:
            self.add_lens(name, int(arg))

    @property
    def focusing_power(self):
        focusing_power = 0
        sorted_lenses = sorted(self.lenses.values(), key=lambda lens: lens.index)
        for i, lens in enumerate(sorted_lenses):
            focusing_power += lens.focal_length * (i + 1)
        return focusing_power


class HashMap:
    def __init__(self):
        self.boxes = [Box() for _ in range(256)]

    def parse_instruction(self, instruction):
        match = re.match(r"([a-z]+)(.*)", instruction)
        instruction, rest = match.groups()
        return instruction, rest

    def apply_instruction(self, instruction):
        label, rest = self.parse_instruction(instruction)
        box_id = hash(label)
        box = self.boxes[box_id]
        box.apply_instruction(label, rest)

    @property
    def focusing_power(self):
        focusing_power = 0
        for i, box in enumerate(self.boxes):
            focusing_power += box.focusing_power * (i + 1)
        return focusing_power


if __name__ == "__main__":
    hashmap = HashMap()
    instructions = Path("input.txt").read_text().split(",")
    for instruction in instructions:
        hashmap.apply_instruction(instruction)
    print(hashmap.focusing_power)