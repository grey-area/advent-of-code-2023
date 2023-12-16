from pathlib import Path
from dataclasses import dataclass
from tqdm import tqdm


@dataclass(frozen=True)
class Point:
    y: int
    x: int

    def __add__(self, other):
        return Point(self.y + other.y, self.x + other.x)


@dataclass(frozen=True)
class Beam:
    position: Point
    direction: Point

    def update(self):
        return Beam(self.position + self.direction, self.direction)


class Map:
    dirs = {
        "up": Point(-1, 0),
        "down": Point(1, 0),
        "left": Point(0, -1),
        "right": Point(0, 1),
    }

    dir_update_dict = {
        ".": {dir: [dir] for dir in dirs.values()},
        "/": {
            dirs["up"]: [dirs["right"]],
            dirs["right"]: [dirs["up"]],
            dirs["down"]: [dirs["left"]],
            dirs["left"]: [dirs["down"]],
        },
        "\\": {
            dirs["up"]: [dirs["left"]],
            dirs["left"]: [dirs["up"]],
            dirs["down"]: [dirs["right"]],
            dirs["right"]: [dirs["down"]],
        },
        "|": {
            dirs["up"]: [dirs["up"]],
            dirs["down"]: [dirs["down"]],
            dirs["left"]: [dirs["up"], dirs["down"]],
            dirs["right"]: [dirs["up"], dirs["down"]],
        },
        "-": {
            dirs["up"]: [dirs["left"], dirs["right"]],
            dirs["down"]: [dirs["left"], dirs["right"]],
            dirs["left"]: [dirs["left"]],
            dirs["right"]: [dirs["right"]],
        },
    }

    def __init__(self, filename):
        self.map = Path(filename).read_text().splitlines()

    @property
    def potential_start_beams(self):
        start_beams = set()

        for x in range(len(self.map[0])):
            start_beams.add(Beam(Point(-1, x), self.dirs["down"]))
            start_beams.add(Beam(Point(len(self.map), x), self.dirs["up"]))
        for y in range(len(self.map)):
            start_beams.add(Beam(Point(y, -1), self.dirs["right"]))
            start_beams.add(Beam(Point(y, len(self.map[0])), self.dirs["left"]))

        return start_beams


    def update_beam(self, beam):
        new_beams = set()
        beam = beam.update()

        if beam.position.y < 0 or beam.position.y >= len(self.map):
            return new_beams
        if beam.position.x < 0 or beam.position.x >= len(self.map[0]):
            return new_beams
        map_contents = self.map[beam.position.y][beam.position.x]

        new_directions = self.dir_update_dict[map_contents][beam.direction]
        for direction in new_directions:
            new_beams.add(Beam(beam.position, direction))
        return new_beams

    def update(self, beams, history):
        new_beams = set()
        for beam in beams:
            for new_beam in self.update_beam(beam):
                if new_beam not in history:
                    new_beams.add(new_beam)
                    history.add(new_beam)
        return new_beams, history

    def compute_energised(self, beams, history):
        while beams:
            beams, history = self.update(beams, history)

        energised = {beam.position for beam in history}
        return len(energised)

    def compute_max_energised(self):
        max_energised = 0
        for beam in tqdm(self.potential_start_beams):
            energised = self.compute_energised({beam}, set())
            max_energised = max(max_energised, energised)
        return max_energised


if __name__ == "__main__":
    map = Map("input.txt")
    energised = map.compute_max_energised()
    print(energised)