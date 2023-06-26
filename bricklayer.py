import pygame
from brick import Brick


def create_bricks(shape: list[list[int]], brick_size: tuple[int, int] = (3, 1)):
    bricks = []
    for r_index, row in enumerate(shape):
        for c_index, set_brick in enumerate(row):
            if set_brick:
                x = c_index * brick_size[0]
                y = r_index * brick_size[1]
                brick = Brick(x, y, *brick_size)
                bricks.append(brick)
    return pygame.sprite.Group(bricks)

if __name__ == "__main__":
    shape: list[list[int]] = [
        [1, 1, 1, 1, 1,],
        [0, 1, 1, 1, 0],
        [0, 0, 1, 0, 0],
    ]
    test = create_bricks(shape)