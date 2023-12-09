from pathlib import Path
import numpy as np


class Row:
    def __init__(self, array):
        self.array = array

    @classmethod
    def from_text(cls, row_text):
        return cls(np.array(row_text.split(" "), dtype=int))

    def compute_next_value(self):
        difference_row = Row(self.array[1:] - self.array[:-1])

        next_value = self.array[-1]
        if not np.all(difference_row.array == 0):
            next_value += difference_row.compute_next_value()

        return next_value


if __name__ == "__main__":
    rows = [Row.from_text(line) for line in Path("input.txt").read_text().splitlines()]

    answer = sum(row.compute_next_value() for row in rows)
    print(answer)