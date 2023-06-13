import pygame

BLACK = (0, 0, 0)


class Paddle(pygame.sprite.Sprite):
    def __init__(self, width, height,size_width, size_heigth):
        #super().__init__()
        pygame.sprite.Sprite.__init__(self)

        #Cell 
        pixel_height= size_heigth/height
        pixel_width= size_width/width
        # Create an image of the paddle
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        # Scale the image to fit the grid cell size
        self.image = pygame.transform.scale(self.image, (pixel_width, pixel_height))
        pygame.draw.rect(self.image, BLACK, [0, 0, width, height])

        self.rect = self.image.get_rect()

    def move_left(self):
        if self.rect.x > 0:
            self.rect.x -= self.rect.width

    def move_right(self):
        if self.rect.x < (self.grid_width - 1) * self.rect.width:
            self.rect.x += self.rect.width

