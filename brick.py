import pygame
import object

BLACK = (0, 0, 0)


class Brick(object.Object):
    def __init__(self, x, y, width, height, color=(0, 0, 0)):
        # super().__init__()
        pygame.sprite.Sprite.__init__(self)

        # Create an image of the paddle
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        # Scale the image to fit the grid cell size
        # self.image = pygame.transform.scale(self.image, (pixel_scale, pixel_scale))

        pygame.draw.rect(self.image, color, [0, 0, width, height])
        self.rect = self.image.get_rect()

        self.speed = 0

        self.rect.x = x
        self.rect.y = y

    # def collision_x(self):
    #     """
    #     Returns
    #     -1 if the paddle touches the left border of the screen,
    #      1 if it touches the right,
    #      0 if neither.
    #     """

    #     if self.rect.x
