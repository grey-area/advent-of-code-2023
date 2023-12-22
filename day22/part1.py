from pathlib import Path
import re
import numpy as np


class Brick:
    def __init__(self, x_min, y_min, z_min, x_max, y_max, z_max):
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.z_min = z_min
        self.z_max = z_max
        self.supports = []
        self.supported_by = []

    def set_height(self, z_min):
        drop = self.z_min - z_min
        self.z_min = z_min
        self.z_max -= drop


class BrickCollection:
    def __init__(self, filename):
        lines = Path(filename).read_text().splitlines()
        self.bricks = [self.parse_brick(line) for line in lines]

    @staticmethod
    def parse_brick(line):
        match = re.match(r"(\d+),(\d+),(\d+)~(\d+),(\d+),(\d+)", line)
        return Brick(*[int(x) for x in match.groups()])

    def settle_brick(self, brick_id, highest_occupant, height):
        brick = self.bricks[brick_id]

        brick_slice = slice(brick.x_min, brick.x_max + 1), slice(brick.y_min, brick.y_max + 1)
        max_height = height[brick_slice].max()
        brick.set_height(max_height + 1)

        max_height_mask = height[brick_slice] == max_height
        supported_by = np.unique(highest_occupant[brick_slice][max_height_mask])

        highest_occupant[brick.x_min:brick.x_max + 1, brick.y_min:brick.y_max + 1] = brick_id
        height[brick.x_min:brick.x_max + 1, brick.y_min:brick.y_max + 1] = brick.z_max

        for support_id in supported_by:
            if support_id == -1:
                continue
            support = self.bricks[support_id]
            support.supports.append(brick_id)
            brick.supported_by.append(support_id)

    def settle(self):
        # Sort bricks by z_min
        self.bricks.sort(key=lambda brick: brick.z_min)

        max_x = 0
        max_y = 0
        for brick in self.bricks:
            max_x = max(max_x, brick.x_max)
            max_y = max(max_y, brick.y_max)

        # 2D arrays of highest occupant ID and height
        highest_occupant = -np.ones((max_x + 1, max_y + 1), dtype=np.int32)
        height = -np.ones((max_x + 1, max_y + 1), dtype=np.int32)

        for brick_id, brick in enumerate(self.bricks):
            self.settle_brick(brick_id, highest_occupant, height)

    def find_disintegratable_bricks(self):
        count = 0
        for brick in self.bricks:
            # If all the bricks it supports are supported by more than one brick
            if all(len(self.bricks[support_id].supported_by) > 1 for support_id in brick.supports):
                count += 1
        return count


if __name__ == "__main__":
    bc = BrickCollection("input.txt")
    bc.settle()
    print(bc.find_disintegratable_bricks())