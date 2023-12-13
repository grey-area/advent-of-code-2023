from pathlib import Path
import numpy as np
from itertools import product


class Map:
    def __init__(self, map_text):
        lines = map_text.splitlines()
        self.map = np.array([[1 if c == '#' else 0 for c in line] for line in lines])

    @staticmethod
    def find_horizontal_reflection(map):
        reflection_scores = []
        for y in range(1, map.shape[0]):
            map_before = map[:y]
            map_before = np.flip(map_before, axis=0)
            map_after = map[y:]
            min_len = min(map_before.shape[0], map_after.shape[0])
            map_before = map_before[:min_len]
            map_after = map_after[:min_len]
            if np.array_equal(map_before, map_after):
                reflection_scores.append(y)
        return reflection_scores

    def find_reflection_score(self):
        scores = [100 * score for score in self.find_horizontal_reflection(self.map)]
        scores += self.find_horizontal_reflection(self.map.T)
        return scores

    def find_smudge_score(self):
        original_reflection_score = self.find_reflection_score()[0]

        for i, j in product(range(self.map.shape[0]), range(self.map.shape[1])):
            self.map[i, j] = 1 - self.map[i, j]

            new_reflection_scores = set(self.find_reflection_score()) - {original_reflection_score}
            if len(new_reflection_scores) > 0:
                new_reflection_score = new_reflection_scores.pop()
                return new_reflection_score

            self.map[i, j] = 1 - self.map[i, j]


def parse_input(filename):
    map_texts = Path(filename).read_text().split("\n\n")
    return [Map(map_text) for map_text in map_texts]


if __name__ == "__main__":
    maps = parse_input("input.txt")
    score = sum(map.find_smudge_score() for map in maps)
    print(score)