from pathlib import Path
import numpy as np


class Map:
    def __init__(self, map_file):
        map_text = Path(map_file).read_text()
        self.map = self.map_text_to_array(map_text)

    @staticmethod
    def map_text_to_array(map_text):
        map_lines = map_text.splitlines()
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

    def __str__(self):
        map_text = ""
        for i in range(self.map.shape[0]):
            for j in range(self.map.shape[1]):
                if self.map[i, j] == 0:
                    map_text += "."
                elif self.map[i, j] == 1:
                    map_text += "O"
                elif self.map[i, j] == 2:
                    map_text += "#"
            map_text += "\n"
        return map_text

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
        for j in range(self.map.shape[1]):
            self.tilt_column_north(j)

    def tilt_south(self):
        self.map = np.flip(self.map, axis=0)
        self.tilt_north()
        self.map = np.flip(self.map, axis=0)

    def tilt_west(self):
        self.map = self.map.T
        self.tilt_north()
        self.map = self.map.T

    def tilt_east(self):
        self.map = self.map.T
        self.tilt_south()
        self.map = self.map.T

    def spin(self):
        self.tilt_north()
        self.tilt_west()
        self.tilt_south()
        self.tilt_east()

    def spin_n_times(self, n): # where n is assumed greater than the cycle length
        state_dict = {}
        state_list = []
        for i in range(n):
            state_string = str(self)
            if state_string in state_dict:
                cycle_length = i - state_dict[state_string]
                cycle_start = state_dict[state_string]
                break
            state_dict[state_string] = i
            state_list.append(state_string)
            self.spin()

        final_state_number = (n - cycle_start) % cycle_length + cycle_start
        final_state_string = state_list[final_state_number]
        self.map = self.map_text_to_array(final_state_string)

    def compute_north_load(self):
        round_rock_ys, _ = np.where(self.map == 1)
        height = self.map.shape[0]
        score = np.sum(height - round_rock_ys)
        return score


if __name__ == "__main__":
    map = Map("input.txt")
    map.spin_n_times(1_000_000_000)
    north_load = map.compute_north_load()
    print(north_load)