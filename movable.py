import pygame
import math
from brick import Brick
from collections import namedtuple
from typing import NamedTuple


class Step(NamedTuple):
    x: list[pygame.rect.Rect]
    y: list[pygame.rect.Rect]
    xy: list[pygame.rect.Rect]


class Movable(pygame.sprite.Sprite):
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        speed: tuple[int, int] | int,
        screen_width: int,
        screen_height: int,
        max_speed: int = 2,
        color: tuple[int, int, int] = (0, 0, 0),
        *groups
    ) -> None:
        super().__init__(*groups)
        self.speed: tuple[int, int] = (0, 0)
        self.screen_width: int = screen_width
        self.screen_height: int = screen_height

        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.max_speed = max_speed
        self.set_speed(speed)

    def next_step(self, speed: tuple[int, int] | None = None) -> Step:
        if speed is None:
            speed = self.speed

        x_movements: list[pygame.rect.RectType] = []
        x_dir = -1 if speed[0] < 0 else 1
        for x_distance in range(1, abs(speed[0]) + 1):
            x_movements.append(
                pygame.rect.Rect(
                    self.rect.x + x_distance * x_dir,
                    self.rect.y,
                    self.rect.width,
                    self.rect.height,
                )
            )

        y_movements: list[pygame.rect.RectType] = []
        y_dir = -1 if speed[1] < 0 else 1
        for y_distance in range(1, abs(speed[1]) + 1):
            y_movements.append(
                pygame.rect.Rect(
                    self.rect.x,
                    self.rect.y + y_distance * y_dir,
                    self.rect.width,
                    self.rect.height,
                )
            )

        xy_movements = []
        for x_distance in range(abs(speed[0]) + 1):
            for y_distance in range(abs(speed[1]) + 1):
                xy_movements.append(
                    pygame.rect.Rect(
                        self.rect.x + x_distance * x_dir,
                        self.rect.y + y_distance * y_dir,
                        self.rect.width,
                        self.rect.height,
                    )
                )

        return Step(x_movements, y_movements, xy_movements)

    def out_of_bounds(
        self,
        rect: pygame.rect.RectType | None = None,
        bounds: pygame.rect.RectType | None = None,
    ) -> bool:
        if bounds is None:
            bounds = pygame.rect.Rect(0, 0, self.screen_width, self.screen_height)

        if rect is None:
            rect = self.rect
        return not bounds.contains(rect)

    def set_speed(self, speed: int | tuple[int, int]) -> tuple[int, int]:
        actual_speed: tuple | list

        if type(speed) == int:
            actual_speed = [speed]

        actual_speed = list(speed)  # type: ignore
        if len(actual_speed) < 2:
            actual_speed[1] = 0

        actual_speed = tuple(
            [int(math.copysign(min(abs(v), self.max_speed), v)) for v in actual_speed]
        )

        self.speed = actual_speed  # type: ignore
        return actual_speed  # type: ignore

    def move(self):
        self.rect.x, self.rect.y = [
            sum(s_v) for s_v in zip(self.rect.topleft, self.speed)
        ]

    def center_x(self):
        self.rect.x = (self.screen_width - self.rect.width) // 2

    def center_y(self):
        self.rect.y = (self.screen_height - self.rect.height) // 2
