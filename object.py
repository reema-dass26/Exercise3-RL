import pygame
import copy
import math


class Object(pygame.sprite.Sprite):
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        screen_width: int = 0,
        screen_height: int = 0,
        color=(0, 0, 0),
        speed: tuple[int, int] = [0, 0],
        max_speed: int = 2,
        *groups,
    ) -> None:
        super().__init__(*groups)

        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.screen_height: int = screen_height
        self.screen_width: int = screen_width
        self.max_speed = max_speed
        self.speed = []
        self.set_speed(speed)

    @property
    def width(self):
        return self.rect.width

    @property
    def height(self):
        return self.rect.height

    def get_shape(self, hitbox: bool = False):
        w = 1 if hitbox else 0
        return pygame.Rect(
            (self.x - w, self.y - w, self.x + self.width + w, self.y + self.height + w)
        )

    def top(self, hitbox: bool = False):
        w = -1 if hitbox else 1
        return pygame.Rect((self.x, self.y, self.x + self.width, self.y + w))

    def bottom(self, hitbox: bool = False):
        w = -1 if hitbox else 1
        return pygame.Rect(
            (
                self.x,
                self.y + self.height,
                self.x + self.width,
                self.y + self.height - w,
            )
        )

    def left(self, hitbox: bool = False, edges: bool = False):
        edges = edges and hitbox  # Only enable together with hitbox
        w = -1 if hitbox else 1
        return pygame.Rect((self.x, self.y, self.x + w, self.y + self.height))

    def right(self, hitbox: bool = False):
        w = -1 if hitbox else 1
        return pygame.Rect(
            (
                self.x + self.width,
                self.y,
                self.x + self.width - w,
                self.y + self.height,
            )
        )

    def get_speed(self):
        return copy.copy(self.speed)

    def set_speed(self, speed: tuple[int, int] | tuple[int]):
        if len(speed) == 1:
            speed = list(speed)
            speed.append(self.speed[1])
        if len(speed) != 2:
            raise ValueError("Invalid speed")
        capped_speed = [
            int(math.copysign(min(abs(v), self.max_speed), v)) for v in speed
        ]
        self.speed: int = capped_speed

    def move(self):
        self.x += self.speed[0]
        self.y += self.speed[1]

        self.rect.x = self.x
        self.rect.y = self.y

    def out_of_bounds(self, hitbox: bool = False):
        bounding_box = pygame.Rect((0, 0, self.screen_width, self.screen_height))
        return not bounding_box.contains(self.get_shape(hitbox=hitbox))

    def oob_directions(self, hitbox: bool = False):
        """
        Returns a collision indicator for [top, right, bottom, left].
        """
        bounding_box = pygame.Rect((0, 0, self.screen_width, self.screen_height))

        oob = [
            not bounding_box.contains(self.top(hitbox=hitbox)),
            not bounding_box.contains(self.right(hitbox=hitbox)),
            not bounding_box.contains(self.bottom(hitbox=hitbox)),
            not bounding_box.contains(self.left(hitbox=hitbox)),
        ]
        return oob
