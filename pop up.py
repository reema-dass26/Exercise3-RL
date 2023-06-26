import pygame
import pygame_menu

# Initialize Pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Game Layout Selector")

# Create the menu
menu = pygame_menu.Menu("Select Game Layout", 400, 300, theme=pygame_menu.themes.THEME_BLUE)
# Define layout selection functions
def layout1_function():
    print("Layout 1 selected")
    # Add code to set up game with layout 1

def layout2_function():
    print("Layout 2 selected")
    # Add code to set up game with layout 2

def layout3_function():
    print("Layout 3 selected")
    # Add code to set up game with layout 3
# Add layout options
menu.add.button("Layout 1", layout1_function)
menu.add.button("Layout 2", layout2_function)
menu.add.button("Layout 3", layout3_function)
menu.add.button("Exit", pygame_menu.events.EXIT)



# Main game loop
running = True
while running:
    # Process events
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    # Update menu
    menu.mainloop(screen, disable_loop=True)

    # Update screen
    pygame.display.flip()

# Quit Pygame

pygame.quit()
