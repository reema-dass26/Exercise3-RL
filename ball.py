import pygame
from paddle import Paddle
from brick import Brick
from math import copysign
import random
import time
import movable
from typing import NamedTuple

BLACK = (0, 0, 0)


class Walls(NamedTuple):
    top: pygame.rect.RectType
    right: pygame.rect.RectType
    bottom: pygame.rect.RectType
    left: pygame.rect.RectType


class Ball(movable.Movable):
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        speed: tuple[int, int] | int | None,
        screen_width: int,
        screen_height: int,
        max_speed: int = 2,
        color: tuple[int, int, int] = (255, 0, 0),
        *groups
    ) -> None:
        if speed is None:
            speed = (random.randint(-2, 2), -1)
        super().__init__(
            x,
            y,
            width,
            height,
            speed,
            screen_width,
            screen_height,
            max_speed,
            color,
            *groups
        )
        self.center_x()
        self.center_y()

    # def collision_x(self):
    #     """
    #     Returns
    #     -1 if the paddle touches the left border of the screen,
    #      1 if it touches the right,
    #      0 if neither.
    #     """

    #     if self.rect.x

    # Other implementation provided
    def check_gameover(self):
        return self.wall_collision()[1] == 1

    def wall_collision(self):
        next_step = self.next_step()
        opposite_step = self.next_step([-v for v in self.speed])  # type: ignore

        x_collision = [False, False]  # next, opposite
        y_collision = [False, False]
        xy_collision = [False, False]

        walls: Walls = Walls(
            pygame.rect.Rect(0, 0, self.screen_width, -1),  # Top
            pygame.rect.Rect(
                self.screen_width, 0, self.screen_width + 1, self.screen_height
            ),  # Right
            pygame.rect.Rect(
                0, self.screen_height, self.screen_width, self.screen_height + 1
            ),  # Bottom
            pygame.rect.Rect(0, 0, -1, self.screen_height),  # Left
        )

        # If a ball bounces off of two opposite walls at the same time,
        # I'm giving up.
        x_collision[0] = (
            x_collision[0]
            or walls.left.collidelist(next_step.x) >= 0
            or walls.right.collidelist(next_step.x) >= 0
        )

        y_collision[0] = (
            y_collision[0]
            or walls.top.collidelist(next_step.y) >= 0
            or walls.bottom.collidelist(next_step.y) >= 0
        )

        xy_collision[0] = xy_collision[0] or (
            walls.top.collidelist(next_step.xy) >= 0
            or walls.right.collidelist(next_step.xy) >= 0
            or walls.bottom.collidelist(next_step.xy) >= 0
            or walls.left.collidelist(next_step.xy) >= 0
        )

        return x_collision, y_collision, xy_collision

    def paddle_collision(self, paddle: Paddle):
        # Describes collision logic with respect to the paddle
        if self.rect.y + self.rect.height >= paddle.rect.y:
            pixel_size = self.screen_width / 15
            if (
                paddle.rect.x - pixel_size
                <= self.rect.x
                < paddle.rect.x + pixel_size / 2
            ):
                self.set_speed((-2, -1))
                return True
            if (
                paddle.rect.x + pixel_size / 2
                <= self.rect.x
                < paddle.rect.x + pixel_size * 3 / 2
            ):
                self.set_speed((-1, -1))
                return True
            if (
                paddle.rect.x + pixel_size * 3 / 2
                <= self.rect.x
                < paddle.rect.x + pixel_size * 5 / 2
            ):
                self.set_speed((-0, -1))
                return True
            if (
                paddle.rect.x + pixel_size * 5 / 2
                <= self.rect.x
                < paddle.rect.x + pixel_size * 7 / 2
            ):
                self.set_speed((1, -1))
                return True
            if (
                paddle.rect.x + pixel_size * 7 / 2
                <= self.rect.x
                < paddle.rect.x + pixel_size * 5
            ):
                self.set_speed((2, -1))
                return True
        return False

    def brick_collision(
        self,
        objects: list[Brick],
        wall_collisions: tuple[list[bool], list[bool], list[bool]] = (
            [False, False],
            [False, False],
            [False, False],
        ),
    ):
        next_step = self.next_step()
        opposite_step = self.next_step([-v for v in self.speed])  # type: ignore

        x_collision, y_collision, xy_collision = wall_collisions

        for o in objects:
            if not o.alive():
                continue
            r = o.rect
            if r.collidelist([*next_step.x, *next_step.y, *next_step.xy]) >= 0:
                o.kill()
            x_collision[0] = x_collision[0] or r.collidelist(next_step.x) >= 0
            y_collision[0] = y_collision[0] or r.collidelist(next_step.y) >= 0
            xy_collision[0] = xy_collision[0] or r.collidelist(next_step.xy) >= 0

            x_collision[1] = x_collision[1] or r.collidelist(opposite_step.x) >= 0
            y_collision[1] = y_collision[1] or r.collidelist(opposite_step.y) >= 0
            xy_collision[1] = xy_collision[1] or r.collidelist(opposite_step.xy) >= 0

            # Kill opposite brick(s) if collision in speed direction occurred.
            if (
                (x_collision[0] and r.collidelist(opposite_step.x) >= 0)
                or (y_collision[0] and r.collidelist(opposite_step.y) >= 0)
                or (xy_collision[0] and r.collidelist(opposite_step.xy) >= 0)
            ):
                o.kill()

        return x_collision, y_collision, xy_collision

    def check_over(self, size_1, bricks):
        # print(f"Size_1 is {size_1} and self.rect.y is {self.rect.y + self.rect.height}")
        if self.rect.y + self.rect.height == size_1:
            print("Game is over!")
            return True
        # if len(bricks) == 0:
        #     print("Game is finished successfully!")
        #     # time.sleep(5000)
        #     return False
        else:
            return False

    def reflect(self, bricks):
        wall_collisions = self.wall_collision()
        brick_collisions = self.brick_collision(bricks, wall_collisions=wall_collisions)

        reflections = [1, 1]  # x y

        if brick_collisions[2][0] and not (
            brick_collisions[0][0] or brick_collisions[1][0]
        ):  # X Y collision
            reflections = [-1, -1]  # This overrides everything else
            # There can be no collision in the other direction, as the ball
            # came from there
        else:
            if brick_collisions[0][0]:  # X
                if brick_collisions[0][1]:  # Bounced on both sides
                    reflections[0] = 0
                else:  # Bounces off
                    reflections[0] = -1
            if brick_collisions[1][0]:  # Y
                if brick_collisions[1][1]:  # Bounced on both sides
                    reflections[1] = 0
                else:  # Bounces off
                    reflections[1] = -1

        self.set_speed((self.speed[0] * reflections[0], self.speed[1] * reflections[1]))
