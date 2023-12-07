from pathlib import Path
from collections import Counter


class Hand:
    card_values = {card: value for value, card in enumerate("23456789TJQKA")}

    def __init__(self, text):
        card_text, bid_text = text.split()
        self.bid = int(bid_text)
        self.card_values = [self.card_values[card] for card in card_text]
        self.sorted_card_counts = sorted(Counter(self.card_values).values(), reverse=True)

    # hands are sorted by their sorted card counts and then by their card values
    def __lt__(self, other):
        return (self.sorted_card_counts, self.card_values) < (other.sorted_card_counts, other.card_values)


if __name__ == "__main__":
    lines = Path("input.txt").read_text().splitlines()
    hands = [Hand(line) for line in lines]

    sorted_hands = sorted(hands)
    total = 0
    for rank, hand in enumerate(sorted_hands, 1):
        total += rank * hand.bid
    print(total)