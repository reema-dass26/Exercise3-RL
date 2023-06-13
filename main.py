import pygame
from paddle import Paddle
pygame.init()

# Define some colors
WHITE = (255,255,255)
BLUE = (36,90,190)
YELLOW = (255,255,0)
RED = (255,0,0)
ORANGE = (255,100,0)


# Open a new window
size = (600, 400)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Breakout Game")

# Define the grid dimensions
grid_width = 15
grid_height = 10

# Calculate the width and height of each grid cell
cell_width = size[0] // grid_width
cell_height = size[1] // grid_height


#List with all sprite objects
all_sprites_list = pygame.sprite.Group()

#Code for putting in the paddle
paddle=Paddle(1,5,size[0],size[1])
paddle.rect.x=300
paddle.rect.y=200

all_sprites_list.add(paddle)

#We want to play
play=True

#Define a clock
clock = pygame.time.Clock()

while(play):
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play=False
    
    # --- Drawing code should go here
    # First, clear the screen be white 
    screen.fill(WHITE)

    # Draw the grid lines
    for x in range(0, size[0], cell_width):
        pygame.draw.line(screen, ORANGE, (x, 0), (x, size[1]))
    for y in range(0, size[1], cell_height):
        pygame.draw.line(screen, ORANGE, (0, y), (size[0], y))

    

    all_sprites_list.update()

    #Now let's draw all the sprites in one go. (For now we only have 2 sprites!)
    all_sprites_list.draw(screen)

    #pygame.draw.line(screen, ORANGE, [0, 38], [800, 38], 2)
    
    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
     
    # --- Limit to 60 frames per second
    clock.tick(60)



pygame.quit()