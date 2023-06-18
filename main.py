import pygame
from paddle import Paddle
from ball import Ball
from brick import Brick
import os
import sys
import time

def create_bricks(layers, brick_size, bricks_per_layer):
    bricks = []
    for layer in range(layers):
        for brick in range(bricks_per_layer):
            bricks.append(Brick(brick_size[0] * brick, brick_size[1] * layer, brick_size[0], brick_size[1]))

    return bricks

pygame.init()

# Define some colors
WHITE = (255,255,255)
BLUE = (36,90,190)
YELLOW = (255,255,0)
RED = (255,0,0)
ORANGE = (255,100,0)

pixel_scale = 45
pixel_size = (15, 10)
size = [pixel_scale * dimension for dimension in pixel_size]

# Open a new window

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Breakout Game")

#List with all sprite objects
all_sprites_list = pygame.sprite.Group()

#Code for putting in the paddle
paddle=Paddle(5*pixel_scale,1*pixel_scale,size[0],size[1]) 
ball = Ball(1 * pixel_scale, 1*pixel_scale, size[0],size[1])

bricks = create_bricks(3, (3*pixel_scale, 1*pixel_scale), 5)

all_sprites_list.add(paddle)
all_sprites_list.add(ball)
all_sprites_list.add(bricks)
#We want to play
play=True


# Variables for time tracking
start_time = time.time()
last_time = start_time

#Function for restarting if game ends
def restart_program():
    python = sys.executable
    os.execl(python, python, *sys.argv)

#Define a clock
clock = pygame.time.Clock()
fps = 120
while(play):
    
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                paddle.speed-=1
            if keys[pygame.K_RIGHT]:
                paddle.speed+=1
            paddle.update_speed()
        if event.type == pygame.QUIT:
            play=False
    
    # --- Drawing code should go here
    # First, clear the screen be white 
    screen.fill(WHITE)


    #Recognizes break successfully
    tobreak=False
    tobreak=ball.check_over(size[1],bricks)
    if tobreak:
        elapsed_time = int(current_time - start_time)
        print(f"The game took {elapsed_time} seconds to complete!")
        pygame.time.delay(3000)
        #Restarts the program after time delay
        restart_program()

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
    #Return only bricks 
    bricks = all_sprites_list.sprites()[2:]
    ball.collision_paddle(paddle)
    ball.move(ball.speed)
    paddle.move_x(paddle.speed)
    if paddle.collision_x():
        paddle.speed = 0
    
    #if ball.check_gameover():
    #    play = False
    #    break

    all_sprites_list.update()

    #Now let's draw all the sprites in one go. (For now we only have 2 sprites!)
    all_sprites_list.draw(screen)

     # Draw the grid lines
    for x in range(0, size[0], pixel_scale):
        pygame.draw.line(screen, ORANGE, (x, 0), (x, size[1]))
    for y in range(0, size[1], pixel_scale):
        pygame.draw.line(screen, ORANGE, (0, y), (size[0], y))

    #pygame.draw.line(screen, ORANGE, [0, 38], [800, 38], 2)
    
    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
     
    # --- Limit to 60 frames per second
    clock.tick(fps)



pygame.quit()