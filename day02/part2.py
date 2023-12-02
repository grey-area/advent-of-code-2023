from pathlib import Path
import re


def product(iterable):
    from functools import reduce
    from operator import mul
    return reduce(mul, iterable, 1)


class Sample:
    colours = ["red", "green", "blue"]

    def __init__(self, *colour_values):
        self.counts = {colour: value for colour, value in zip(self.colours, colour_values)}

    @classmethod
    def from_text(cls, sample_text):
        colour_values = []
        for colour in cls.colours:
            num = cls.parse_colour(colour, sample_text)
            colour_values.append(num)
        return cls(*colour_values)

    @staticmethod
    def parse_colour(colour, sample_text):
        match = re.search(r"(\d+) {}".format(colour), sample_text)
        num = 0
        if match:
            num = int(match.group(1))
        return num


class Game:
    def __init__(self, game_text):
        self.samples = []
        self.parse(game_text)

    def parse(self, game_text):
        match = re.match(r"Game (\d+): (.*)", game_text)
        game_id, game_text = match.groups()
        self.id = int(game_id)

        samples_text = game_text.split("; ")
        for sample_text in samples_text:
            sample = Sample.from_text(sample_text)
            self.samples.append(sample)

    def maximums(self):
        return {colour: max(sample.counts[colour] for sample in self.samples) for colour in Sample.colours}


if __name__ == "__main__":
    game_lines = Path("input.txt").read_text().splitlines()

    sum_of_powers = 0
    for game_text in game_lines:
        game = Game(game_text)
        maximums = game.maximums()
        sum_of_powers += product(maximums.values())

    print(sum_of_powers)