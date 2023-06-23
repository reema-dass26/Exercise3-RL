import pygame
import copy
from typing import Tuple


class Board:
    def __init__(self, size: Tuple[int, int] = (15, 10), pixel_scale: int = 45) -> None:
        self.size = size
        self.render_size = [pixel_scale * dimension for dimension in size]
        self.display = pygame.display
        self.screen = pygame.display.set_mode(self.render_size)
        self.surface: pygame.Surface = pygame.Surface(size)

    def render(self):
        upscaled = pygame.transform.scale(self.surface.copy(), self.render_size)
        self.screen.blit(upscaled, (0, 0))
