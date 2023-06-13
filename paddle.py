import pygame

BLACK = (0, 0, 0)


class Paddle(pygame.sprite.Sprite):
    def __init__(self, width, height, grid_width, grid_height):
        pygame.sprite.Sprite.__init__(self)
        # self.grid_width = grid_width
        # self.grid_height = grid_height

        # Calculate the width and height of each grid cell
        cell_width = width // grid_width
        cell_height = height // grid_height

        # Create an image of the paddle
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        pygame.draw.rect(self.image, BLACK, [0, 0, width, height])

        # Scale the image to fit the grid cell size
        self.image = pygame.transform.scale(self.image, (cell_width, cell_height))

        self.rect = self.image.get_rect()

    def move_left(self):
        if self.rect.x > 0:
            self.rect.x -= self.rect.width

    def move_right(self):
        if self.rect.x < (self.grid_width - 1) * self.rect.width:
            self.rect.x += self.rect.width

