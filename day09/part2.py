from pathlib import Path
import numpy as np


class Row:
    def __init__(self, array):
        self.array = array

    @classmethod
    def from_text(cls, row_text):
        return cls(np.array(row_text.split(" "), dtype=int))

    def compute_prev_value(self):
        difference_row = Row(self.array[1:] - self.array[:-1])

        prev_value = self.array[0]
        if not np.all(difference_row.array == 0):
            prev_value -= difference_row.compute_prev_value()

        return prev_value


if __name__ == "__main__":
    rows = [Row.from_text(line) for line in Path("input.txt").read_text().splitlines()]

    answer = sum(row.compute_prev_value() for row in rows)
    print(answer)