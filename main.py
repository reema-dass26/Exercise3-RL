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


def create_bricks(layers, brick_size, bricks_per_layer):
    bricks = []
    for layer in range(layers):
        for brick in range(bricks_per_layer):
            bricks.append(
                Brick(
                    brick_size[0] * brick,
                    brick_size[1] * layer,
                    brick_size[0],
                    brick_size[1],
                )
            )

    return pygame.sprite.Group(bricks)


pygame.init()

WHITE = (255, 255, 255)

# Variables for time tracking
start_time = time.time()
last_time = start_time


board: Board = Board()
board.display.set_caption("Breakout Game")
agent = Agent()

won = False
while not won:
    # List with all sprite objects
    all_sprites_list = pygame.sprite.Group()

    # Code for putting in the paddle
    paddle = Paddle(5, 1, *board.size)
    ball = Ball(1, 1, *board.size)

    bricks = create_bricks(3, (3, 1), 5)

    all_sprites_list.add(paddle)
    all_sprites_list.add(ball)
    all_sprites_list.add(bricks)
    # We want to play
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
            # if event.type == pygame.KEYDOWN:
            #     # keys = pygame.key.get_pressed()
            #     # if keys[pygame.K_LEFT]:
            #     #     paddle.speed-=1
            #     # if keys[pygame.K_RIGHT]:
            #     #     paddle.speed+=1
            #     # paddle.update_speed()
            #     paddle.speed += random.choice([-1, 0, 1])

            if event.type == pygame.QUIT:
                play = False
                won = True

        if not iteration % agent_wait_time:
            # Agent:

            state = (
                paddle.rect.x,  # Paddle position
                paddle.speed,  # Paddle speed
                (ball.rect.x, ball.rect.y),  # Ball position
                tuple(ball.speed),  # Ball speed
            )

            action = agent.policy(state)
            paddle.speed += action
            paddle.update_speed()

        # --- Drawing code should go here
        # First, clear the screen be white
        board.surface.fill(WHITE)

        # Recognizes break successfully
        tobreak = False
        tobreak = ball.check_over(board.size[1], bricks)
        if tobreak and False:
            elapsed_time = int(current_time - start_time)
            print(f"The game took {elapsed_time} seconds to complete!")
            # pygame.time.delay(3000)
            play = False
            break
            # Restarts the program after time delay
            # restart_program()

        # Calculate current time
        current_time = time.time()

        # Check if 10 seconds have passed since the last time print
        if current_time - last_time >= 10:
            print(f"The length of the bricks list is {len(bricks)}")
            elapsed_time = int(current_time - start_time)
            print("Elapsed time: ", elapsed_time, " seconds")
            last_time = current_time

        # Move paddle
        # Moving the paddle when the user uses the arrow keys

        ball.reflect()
        ball.collision_bricks(bricks)
        # Return only bricks
        # bricks = all_sprites_list.sprites()[2:]
        if ball.collision_paddle(paddle):
            paddle_bumps += 1
        ball.move(ball.speed)
        paddle.move_x(paddle.speed)
        if paddle.collision_x():
            paddle.speed = 0

        # if ball.check_gameover():
        #    play = False
        #    break

        all_sprites_list.update()

        # Now let's draw all the sprites in one go. (For now we only have 2 sprites!)
        all_sprites_list.draw(board.surface)

        # Draw the grid lines
        # for x in range(0, size[0], pixel_scale):
        #     pygame.draw.line(screen, ORANGE, (x, 0), (x, size[1]))
        # for y in range(0, size[1], pixel_scale):
        #     pygame.draw.line(screen, ORANGE, (0, y), (size[0], y))

        # pygame.draw.line(screen, ORANGE, [0, 38], [800, 38], 2)

        if not iteration % agent_wait_time:
            # Agent rewards
            reward = agent.get_score(bricks, paddle_bumps)
            paddle_bumps = 0
            agent.remember_reward(state, action, reward)
            print(
                f"""
                Agent:
                state:        {state}
                action:       {action}
                reward:       {reward}
                total_reward: {agent.total_reward}
                bricks:       {len(bricks)}
                """
            )

        # --- Go ahead and update the screen with what we've drawn.
        board.render()
        board.display.flip()

        # --- Limit to 60 frames per second
        iteration += 1
        # clock.tick(fps)


pygame.quit()
