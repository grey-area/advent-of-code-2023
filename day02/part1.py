from pathlib import Path
import re


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

    def sample_possible(self, other):
        return all(self.counts[colour] >= other.counts[colour] for colour in self.colours)


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

    def all_samples_possible(self, sample):
        return all(sample.sample_possible(other) for other in self.samples)


if __name__ == "__main__":
    game_lines = Path("input.txt").read_text().splitlines()

    comparison_sample = Sample(12, 13, 14)

    possible_game_ids = []
    for game_text in game_lines:
        game = Game(game_text)
        if game.all_samples_possible(comparison_sample):
            possible_game_ids.append(game.id)

    print(sum(possible_game_ids))