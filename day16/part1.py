from pathlib import Path
from dataclasses import dataclass


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
        self.beams = {Beam(Point(0, 0), Point(0, 1))}
        self.history = set()

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

    def update(self):
        new_beams = set()
        for beam in self.beams:
            for new_beam in self.update_beam(beam):
                if new_beam not in self.history:
                    new_beams.add(new_beam)
                    self.history.add(new_beam)
        self.beams = new_beams

    def compute_energised(self):
        while self.beams:
            self.update()

        energised = {beam.position for beam in self.history}
        return len(energised)


if __name__ == "__main__":
    map = Map("input.txt")
    energised = map.compute_energised()
    print(energised)