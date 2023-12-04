from pathlib import Path
import re


class Card:
    def __init__(self, card_text):
        self.parse_text(card_text)

    @staticmethod
    def parse_numbers(number_text):
        return {int(number) for number in number_text.split()}

    def parse_text(self, card_text):
        match = re.match(r"Card\s+(\d+):\s+(.*)\s+\|\s+(.*)", card_text)
        self.id = int(match.group(1))
        self.winning_numbers = self.parse_numbers(match.group(2))
        self.card_numbers = self.parse_numbers(match.group(3))

    def compute_points(self):
        num_matches = len(self.winning_numbers & self.card_numbers)

        points = 0
        if num_matches > 0:
            points = 2 ** (num_matches - 1)

        return points


if __name__ == "__main__":
    lines = Path("input.txt").read_text().splitlines()
    cards = [Card(line) for line in lines]

    print(sum(card.compute_points() for card in cards))