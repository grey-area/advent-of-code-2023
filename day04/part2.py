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

    def compute_number_of_matches(self):
        return len(self.winning_numbers & self.card_numbers)


class Game:
    def __init__(self, cards_texts):
        self.cards = [Card(card_text) for card_text in cards_texts]

    def play(self):
        counts = {}

        for card in self.cards[::-1]:
            card_count = 1
            matches = card.compute_number_of_matches()
            for card_id in range(card.id + 1, card.id + matches + 1):
                if card_id in counts:
                    card_count += counts[card_id]
            counts[card.id] = card_count

        return sum(counts.values())


if __name__ == "__main__":
    game = Game(Path("input.txt").read_text().splitlines())
    print(game.play())