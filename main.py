import pygame
from paddle import Paddle
from ball import Ball
from brick import Brick
from mc import Agent
from board import Board
import os
import sys
import time
import random
import debug

pygame.init()

WHITE = (255, 255, 255)

# Variables for time tracking
start_time = time.time()
last_time = start_time

board: Board = Board()
board.display.set_caption("Breakout Game")

won = False
while not won:
    # List with all sprite objects
    all_sprites_list = pygame.sprite.Group()

    # Code for putting in the paddle
    paddle_dims: tuple[int, int] = (5, 1)
    paddle = Paddle(
        0,
        board.surface.get_height() - paddle_dims[1] - 1,
        *paddle_dims,
        board.surface.get_width(),
        board.surface.get_height(),
        color=(0, 255, 0),
    )

    all_sprites_list.add(paddle)

    play = True

    # Define a clock
    clock = pygame.time.Clock()
    fps = 120
    agent_wait_time = 10
    iteration = 0
    paddle_bumps: int = 0
    current_time = time.time()
    while play:
        for event in pygame.event.get():
            # Manual control
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT]:
                    paddle.set_speed([paddle.get_speed()[0] - 1])
                if keys[pygame.K_RIGHT]:
                    paddle.set_speed([paddle.get_speed()[0] + 1])

            if event.type == pygame.QUIT:
                play = False
                won = True

        # Recognizes break successfully
        tobreak = False
        if tobreak:
            elapsed_time = int(current_time - start_time)
            print(f"The game took {elapsed_time} seconds to complete!")
            # pygame.time.delay(3000)
            play = False
            break
            # Restarts the program after time delay
            # restart_program()

        board.surface.fill((255, 0, 0))

        if paddle.out_of_bounds(hitbox=True):
            oob = paddle.oob_directions(hitbox=True)
            if oob[1]:  # right
                paddle.set_speed([min(paddle.get_speed()[0], 0)])
                if debug.DEBUG:
                    print(f"Bump right, {paddle.get_speed()}")

            if oob[3]:  # left
                paddle.set_speed([max(paddle.get_speed()[0], 0)])
                print(f"Bump left, {paddle.get_speed()}")
        paddle.move()
        all_sprites_list.draw(board.surface)

        board.render()
        board.display.flip()

        # --- Limit to 60 frames per second
        clock.tick(fps)


pygame.quit()
