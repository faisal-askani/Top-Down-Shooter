import pygame

# Size of your game window in pixels.
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
TITLE = "COMMANDO"
BACKGROUND_COLOR = (109, 105, 135)

# Initialize pygame modules(display, sound, input)
pygame.init()
# Creates the game window with the specified width and height.
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# Sets the title of the game window
pygame.display.set_caption(title=TITLE)
clock = pygame.time.Clock()
running = True

background_image = pygame.image.load("assets/Environment/background.png")
# image = pygame.transform.scale(image, (44, 44))

while running:
    # Poll for events
    for event in pygame.event.get():
        # pygame.QUIT event means the user clicked X to close your window
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with a color to wipe away anything from last frame
    screen.fill(BACKGROUND_COLOR)
    # pygame.draw.rect(screen, (255, 0, 0), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 2)

    ######################## RENDER YOUR GAME HERE ########################

    screen.blit(background_image,(0,0))

    #######################################################################

    # flip() the display to put your work on screen
    pygame.display.flip()
    # limits FPS to 60
    clock.tick(60)

# Close the library and quit the screen
pygame.quit()
