import pygame

BLACK = (0, 0, 0)


class Paddle(pygame.sprite.Sprite):
    def __init__(self, width, height, size_width, size_heigth):
        # super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.screen_width = size_width
        self.screen_height = size_heigth
        self.speed=0
        
        # Cell
        pixel_height = size_heigth / height
        pixel_width = size_width / width
        # Create an image of the paddle
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        # Scale the image to fit the grid cell size
        self.image = pygame.transform.scale(self.image, (pixel_width, pixel_height))
        pygame.draw.rect(self.image, BLACK, [0, 0, width, height])

        self.rect = self.image.get_rect()

    # def collision_x(self):
    #     """
    #     Returns 
    #     -1 if the paddle touches the left border of the screen, 
    #      1 if it touches the right, 
    #      0 if neither.
    #     """

    #     if self.rect.x 

    def move_x(self, distance):
        to_move = 0
        if distance < 0:
            to_move = -min(-distance, self.rect.x)
        else:
            to_move = min(distance, self.screen_width - (self.rect.x + self.rect.width))
        self.rect.x += to_move

    def move_left(self):
        if self.rect.x > 0:
            self.rect.x -= self.rect.width

    def move_right(self):
        if self.rect.x < (self.grid_width - 1) * self.rect.width:
            self.rect.x += self.rect.width
    def update_speed(self):
        if self.speed>2:
            self.speed=2
        if self.speed<-2:
            self.speed=-2
    
