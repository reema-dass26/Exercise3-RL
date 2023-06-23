import pygame
from paddle import Paddle
from brick import Brick
from math import copysign
import random
import time

BLACK = (0, 0, 0)


class Ball(pygame.sprite.Sprite):
    def __init__(self, width, height, screen_width, screen_height):
        # super().__init__()
        pygame.sprite.Sprite.__init__(self)

        # Create an image of the paddle
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        # Scale the image to fit the grid cell size
        # self.image = pygame.transform.scale(self.image, (pixel_scale, pixel_scale))

        pygame.draw.rect(self.image, BLACK, [0, 0, width, height])
        self.rect = self.image.get_rect()

        # Ball start in the middle of the screen
        self.rect.x = screen_width / 2

        self.screen_width = screen_width
        self.screen_height = screen_height
        self.speed = [random.randint(-2, 2), -1]
        #self.speed = [1, -1]

        self.center_x()
        self.rect.y = screen_height // 2

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
        return self.collision()[1] == 1

    def center_x(self):
        self.x = (self.screen_width - self.rect.width) // 2

    def collision(self):
        collides = [0, 0]

        if not self.rect.x:
            collides[0] = -1
        if not self.screen_width - (self.rect.x + self.rect.width):
            collides[0] = 1

        if not self.rect.y:
            collides[1] = -1
        if not self.screen_height - (self.rect.y + self.rect.height):
            collides[1] = 1

        return collides

    def collision_paddle(self, paddle: Paddle):
        ball_x_center = self.rect.x + self.rect.width / 2

        # Describes collision logic with respect to the paddle
        if self.rect.y + self.rect.height >= paddle.rect.y:
            pixel_size = self.screen_width / 15
            if (
                paddle.rect.x - pixel_size
                <= self.rect.x
                < paddle.rect.x + pixel_size / 2
            ):
                self.speed = [-2, -1]
                return True
            if (
                paddle.rect.x + pixel_size / 2
                <= self.rect.x
                < paddle.rect.x + pixel_size * 3 / 2
            ):
                self.speed = [-1, -1]
                return True
            if (
                paddle.rect.x + pixel_size * 3 / 2
                <= self.rect.x
                < paddle.rect.x + pixel_size * 5 / 2
            ):
                self.speed = [-0, -1]
                return True
            if (
                paddle.rect.x + pixel_size * 5 / 2
                <= self.rect.x
                < paddle.rect.x + pixel_size * 7 / 2
            ):
                self.speed = [1, -1]
                return True
            if (
                paddle.rect.x + pixel_size * 7 / 2
                <= self.rect.x
                < paddle.rect.x + pixel_size * 5
            ):
                self.speed = [2, -1]
                return True
        return False

    def collision_bricks(self, bricks: list):
        collisions_x = [0, 0]  # left, right
        collisions_y = [0, 0]  # top, bottom
        for brick in bricks:
            if self.rect.colliderect(brick.rect):
                if self.rect.x == brick.rect.x + brick.rect.width:
                    collisions_x[0] += -1
                if self.rect.x + self.rect.width == brick.rect.x:
                    collisions_x[1] += 1

                if self.rect.y == brick.rect.y + brick.rect.height:
                    collisions_y[1] += 1
                if self.rect.y + self.rect.height == brick.rect.y:
                    collisions_y[0] += -1

                brick.kill()
                self.speed[1] *= -1
        direction_x = sum(collisions_x)
        direction_y = sum(collisions_y)
        if direction_x:
            self.speed[0] = copysign(self.speed[0], direction_x)
        if direction_y:
            self.speed[1] = copysign(self.speed[1], direction_y)
        # for brick in bricks:
        #     if self.rect.y == brick.rect.y + brick.rect.height:
        #         if brick.rect.x - brick.rect.width/2 <= self.rect.x < brick.rect.x + brick.rect.width/2:
        #             brick.kill()
        #             self.speed[1]*=-1

    def check_over(self, size_1, bricks):
        # print(f"Size_1 is {size_1} and self.rect.y is {self.rect.y + self.rect.height}")
        if self.rect.y + self.rect.height == size_1:
            print("Game is over!")
            return True
        if len(bricks) == 0:
            print("Game is finished successfully!")
            time.sleep(5000)
            return False
        else:
            return False

    def reflect(self):
        collisions = self.collision()
        if collisions[0]:
            self.speed[0] *= -1

        if collisions[1]:
            self.speed[1] *= -1

    def move_generic(self, distance, element_pos, element_size, screen_size) -> int:
        to_move = 0
        if distance < 0:
            to_move = -min(-distance, element_pos)
        else:
            to_move = min(distance, screen_size - (element_pos + element_size))
        return to_move

    def move_x(self, distance):
        self.rect.x += self.move_generic(
            distance, self.rect.x, self.rect.width, self.screen_width
        )

    def move_y(self, distance):
        self.rect.y += self.move_generic(
            distance, self.rect.y, self.rect.height, self.screen_height
        )

    def move(self, speed):
        self.move_x(speed[0])
        self.move_y(speed[1])
