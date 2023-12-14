from pathlib import Path
import numpy as np


class Map:
    def __init__(self, map_file):
        map_text = Path(map_file).read_text()
        self.map = self.map_text_to_array(map_text)

    @staticmethod
    def map_text_to_array(map_text):
        map_lines = map_text.split("\n")
        map_array = np.zeros((len(map_lines), len(map_lines[0])))
        for i, line in enumerate(map_lines):
            for j, char in enumerate(line):
                if char == ".":
                    map_array[i, j] = 0
                elif char == "O":
                    map_array[i, j] = 1
                elif char == "#":
                    map_array[i, j] = 2
        return map_array

    @staticmethod
    def map_array_to_text(map_array):
        map_text = ""
        for i in range(map_array.shape[0]):
            for j in range(map_array.shape[1]):
                if map_array[i, j] == 0:
                    map_text += "."
                elif map_array[i, j] == 1:
                    map_text += "O"
                elif map_array[i, j] == 2:
                    map_text += "#"
            map_text += "\n"
        return map_text

    def __str__(self):
        return self.map_array_to_text(self.map)

    def tilt_column_north(self, j):
        column = self.map[:, j]
        cubic_rock_locations = np.where(column == 2)[0]
        cubic_rock_locations = np.insert(cubic_rock_locations, 0, -1)
        cubic_rock_locations = np.append(cubic_rock_locations, len(column))

        for start, end in zip(cubic_rock_locations[:-1], cubic_rock_locations[1:]):
            sub_column = column[start + 1:end]
            round_rock_count = np.sum(sub_column == 1)
            sub_column[:round_rock_count] = 1
            sub_column[round_rock_count:] = 0

    def tilt_north(self):
        # for each column
        for j in range(self.map.shape[1]):
            self.tilt_column_north(j)

    def compute_score(self):
        round_rock_ys, _ = np.where(self.map == 1)
        height = self.map.shape[0]
        score = np.sum(height - round_rock_ys)
        return score


if __name__ == "__main__":
    map = Map("input.txt")
    map.tilt_north()
    score = map.compute_score()
    print(score)