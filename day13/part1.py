from pathlib import Path
import numpy as np


class Map:
    def __init__(self, map_text):
        lines = map_text.splitlines()
        self.map = np.array([[1 if c == '#' else 0 for c in line] for line in lines])

    @staticmethod
    def find_horizontal_reflection(map):
        # check if reflection comes before y
        for y in range(1, map.shape[0]):
            map_before = map[:y]
            map_before = np.flip(map_before, axis=0)
            map_after = map[y:]
            min_len = min(map_before.shape[0], map_after.shape[0])
            map_before = map_before[:min_len]
            map_after = map_after[:min_len]
            if np.array_equal(map_before, map_after):
                return y
        return 0

    def find_score(self):
        score = 100 * self.find_horizontal_reflection(self.map)
        if score == 0:
            score = self.find_horizontal_reflection(self.map.T)
        return score


def parse_input(filename):
    map_texts = Path(filename).read_text().split("\n\n")
    return [Map(map_text) for map_text in map_texts]


if __name__ == "__main__":
    maps = parse_input("input.txt")
    score = sum(map.find_score() for map in maps)
    print(score)
