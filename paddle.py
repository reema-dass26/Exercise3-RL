import pygame
import object


class Paddle(object.Object):
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        screen_height: int,
        screen_width: int,
        color=(0, 0, 0),
        *groups,
    ) -> None:
        super().__init__(
            x, y, width, height, screen_height, screen_width, color, *groups
        )
