from pathlib import Path
import re
import numpy as np
from copy import deepcopy
from tqdm import tqdm


class Brick:
    def __init__(self, line):
        match = re.match(r"(\d+),(\d+),(\d+)~(\d+),(\d+),(\d+)", line)
        self.x_min = int(match.group(1))
        self.y_min = int(match.group(2))
        self.z_min = int(match.group(3))
        self.x_max = int(match.group(4))
        self.y_max = int(match.group(5))
        self.z_max = int(match.group(6))
        self.supports = []
        self.supported_by = []

    def set_height(self, z_min):
        drop = self.z_min - z_min
        self.z_min = z_min
        self.z_max -= drop


class BrickCollection:
    def __init__(self, bricks):
        self.bricks = [deepcopy(brick) for brick in bricks]
        self.settle()

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


if __name__ == "__main__":
    lines = Path("input.txt").read_text().splitlines()
    bricks = [Brick(line) for line in lines]
    bricks.sort(key=lambda brick: brick.z_min)

    """
    Slow and lazy solution: just try removing each brick and see how many bricks change height.
    """

    bc = BrickCollection(bricks)

    change_count = 0
    for missing_brick_id in range(len(bricks)):
        new_bc = BrickCollection(bricks[:missing_brick_id] + bricks[missing_brick_id + 1:])

        old_bricks = bc.bricks[:missing_brick_id] + bc.bricks[missing_brick_id + 1:]
        new_bricks = new_bc.bricks

        for old_brick, new_brick in zip(old_bricks, new_bricks):
            if old_brick.z_min != new_brick.z_min:
                change_count += 1

    print(change_count)