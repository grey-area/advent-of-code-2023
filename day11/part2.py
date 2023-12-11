from pathlib import Path
import numpy as np
from itertools import combinations


class Map:
    def __init__(self, filename):
        text = Path(filename).read_text()
        self.map = self.parse_map(text)

    @staticmethod
    def parse_map(text):
        return np.array([[1 if elem == "#" else 0 for elem in line] for line in text.splitlines()])

    @staticmethod
    def compute_expansion_on_dimension(map, dimension):
        return np.where(~map.any(axis=dimension))[0]

    def compute_galaxy_locations(self, map, expansion_factor):
        xs, ys = np.where(map)

        expanded_rows = self.compute_expansion_on_dimension(map, 0)
        expanded_cols = self.compute_expansion_on_dimension(map, 1)

        per_galaxy_row_expansion = (np.expand_dims(xs, 0) > np.expand_dims(expanded_cols, 1)).sum(axis=0)
        per_galaxy_col_expansion = (np.expand_dims(ys, 0) > np.expand_dims(expanded_rows, 1)).sum(axis=0)

        xs += per_galaxy_row_expansion * (expansion_factor - 1)
        ys += per_galaxy_col_expansion * (expansion_factor - 1)
        return np.stack((xs, ys), axis=1)

    def get_galaxy_location_pairs(self, expansion_factor):
        galaxy_locations = self.compute_galaxy_locations(self.map, expansion_factor)
        return np.array(list(combinations(galaxy_locations, 2)))

    def get_manhattan_distances(self, expansion_factor):
        pairs = self.get_galaxy_location_pairs(expansion_factor)
        return np.abs(pairs[:, 0] - pairs[:, 1]).sum(axis=1)


if __name__ == "__main__":
    map = Map("input.txt")
    sum_of_galaxy_distances = map.get_manhattan_distances(expansion_factor=1000000).sum()
    print(sum_of_galaxy_distances)