import pygame
from paddle import Paddle
from ball import Ball
from brick import Brick

pygame.init()

# Define some colors
WHITE = (255, 255, 255)
DARKBLUE = (36, 90, 190)
LIGHTBLUE = (0, 176, 240)
RED = (255, 0, 0)
ORANGE = (255, 100, 0)
YELLOW = (255, 255, 0)

score = 0
lives = 3

# Open a new window
size = (900, 600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Breakout Game")

# This will be a list that will contain all the sprites we intend to use in our game.
all_sprites_list = pygame.sprite.Group()

# Create the Paddle
cell_width = size[0] // 15
cell_height = size[1] // 10
paddle = Paddle(LIGHTBLUE, cell_width - 20, cell_height // 2)
paddle.rect.x = (size[0] // 2) - (cell_width // 2)
paddle.rect.y = size[1] - cell_height

# Create the ball sprite
ball = Ball(WHITE, 10, 10)
ball.rect.x = (size[0] // 2) - (cell_width // 2)
ball.rect.y = (size[1] // 2) - (cell_height // 2)

all_bricks = pygame.sprite.Group()

for i in range(7):
    brick = Brick(RED, cell_width - 20, cell_height // 2)
    brick.rect.x = 60 + i * (cell_width + 20)
    brick.rect.y = 60
    all_sprites_list.add(brick)
    all_bricks.add(brick)
for i in range(7):
    brick = Brick(ORANGE, cell_width - 20, cell_height // 2)
    brick.rect.x = 60 + i * (cell_width + 20)
    brick.rect.y = 100
    all_sprites_list.add(brick)
    all_bricks.add(brick)
for i in range(7):
    brick = Brick(YELLOW, cell_width - 20, cell_height // 2)
    brick.rect.x = 60 + i * (cell_width + 20)
    brick.rect.y = 140
    all_sprites_list.add(brick)
    all_bricks.add(brick)

# Add the paddle and the ball to the list of sprites
all_sprites_list.add(paddle)
all_sprites_list.add(ball)

# The loop will carry on until the user exits the game (e.g. clicks the close button).
carryOn = True

# The clock will be used to control how fast the screen updates
clock = pygame.time.Clock()

# -------- Main Program Loop -----------
while carryOn:
    # --- Main event loop
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            carryOn = False  # Flag that we are done so we exit this loop

    # Moving the paddle when the user uses the arrow keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        paddle.moveLeft(5)
    if keys[pygame.K_RIGHT]:
        paddle.moveRight(5)

    # --- Game logic should go here
    all_sprites_list.update()

    # Check if the ball is bouncing against any of the 4 walls:
    if ball.rect.x >= size[0] - 10:
        ball.velocity[0] = -ball.velocity[0]
    if ball.rect.x <= 0:
        ball.velocity[0] = -ball.velocity[0]
    if ball.rect.y > size[1] - 10:
        ball.velocity[1] = -ball.velocity[1]
        lives -= 1
        if lives == 0:
            # Display Game Over Message for 3 seconds
            font = pygame.font.Font(None, 74)
            text = font.render("GAME OVER", 1, WHITE)
            screen.blit(text, (250, 300))
            pygame.display.flip()
            pygame.time.wait(3000)

            # Stop the Game
            carryOn = False

    if ball.rect.y < 40:
        ball.velocity[1] = -ball.velocity[1]

    # Detect collisions between the ball and the paddles
    if pygame.sprite.collide_mask(ball, paddle):
        ball.rect.x -= ball.velocity[0]
        ball.rect.y -= ball.velocity[1]
        ball.bounce()

    # Check if the ball collides with any bricks
    brick_collision_list = pygame.sprite.spritecollide(ball, all_bricks, False)
    for brick in brick_collision_list:
        ball.bounce()
        score += 1
        brick.kill()
        if len(all_bricks) == 0:
            # Display Level Complete Message for 3 seconds
            font = pygame.font.Font(None, 74)
            text = font.render("LEVEL COMPLETE", 1, WHITE)
            screen.blit(text, (200, 300))
            pygame.display.flip()
            pygame.time.wait(3000)

            # Stop the Game
            carryOn = False

    # --- Drawing code should go here
    # First, clear the screen to dark blue.
    screen.fill(DARKBLUE)
    pygame.draw.line(screen, WHITE, [0, 38], [size[0], 38], 2)

    # Get the current time in seconds
    time_seconds = pygame.time.get_ticks() // 1000
    # Display the score and the number of lives at the top of the screen
    font = pygame.font.Font(None, 34)
    time_to_print = font.render("The time is: " + str(time_seconds), 1, WHITE)
    screen.blit(time_to_print, (20, 10))
    
    # Now let's draw all the sprites in one go.
    all_sprites_list.draw(screen)

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)

# Once we have exited the main program loop, we can stop the game engine.
pygame.quit()
