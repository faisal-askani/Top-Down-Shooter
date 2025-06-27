import pygame
from player import Player
from bullet import Bullet


# Size of your game window in pixels.
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
TITLE = "COMMANDO"
BACKGROUND_COLOR = (109, 105, 135)

# Initialize pygame modules(display, sound, input)
pygame.init()
pygame.mouse.set_visible(False)  # Hide system cursor
# Creates the game window with the specified width and height.
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# Sets the title of the game window
pygame.display.set_caption(title=TITLE)
clock = pygame.time.Clock()
running = True

background_image = pygame.transform.scale(pygame.image.load("assets/environment/background2.png"),
                                          (1920, 1080))

player = Player(900, 400)
bullet = Bullet(player.player_size, player.get_position)

while running:
    # Poll for events
    events = pygame.event.get()
    for event in events:
        # pygame.QUIT event means the user clicked X to close your window
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with a color to wipe away anything from last frame
    screen.fill(BACKGROUND_COLOR)
    screen.blit(background_image, (0, 0))
    ######################## RENDER YOUR GAME HERE ########################

    player.handle_input()
    player.draw(screen)
    bullet.handle_input(events)
    bullet.draw(screen)

    #######################################################################

    # flip() the display to put your work on screen
    pygame.display.flip()
    # limits FPS to 60
    clock.tick(60)

# Close the library and quit the screen
pygame.quit()
