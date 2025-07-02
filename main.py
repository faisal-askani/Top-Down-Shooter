import pygame
from player import Player
from enemy import Enemy
from bullet import Bullet


# Size of your game window in pixels.
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
TITLE = "COMMANDO"
BACKGROUND_COLOR = (109, 105, 135)

# Initialize pygame modules(display, sound, input)
pygame.init()
pygame.mixer.init()
# pygame.mouse.set_visible(False)  # Hide system cursor
# Creates the game window with the specified width and height.
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# Sets the title of the game window
pygame.display.set_caption(title=TITLE)
clock = pygame.time.Clock()
pygame.mixer.music.load("assets/audio/retro_future.mp3")
pygame.mixer.music.set_volume(0.0)  # Volume: 0.0 to 1.0
pygame.mixer.music.play(-1)  # -1 = loop forever

running = True

background_image = pygame.transform.scale(pygame.image.load("assets/environment/background2.png"),
                                          (1920, 1080))

player = Player(900, 400)
enemy = Enemy(100, 100, player.get_center)
bullet = Bullet(player.get_center,
                player.get_radian,
                enemy.get_enemy_collision_rect,
                enemy.is_bullet_hit)

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
    bullet.handle_input(events, screen)
    bullet.draw(screen)
    enemy.draw(screen)

    #######################################################################

    # flip() the display to put your work on screen
    pygame.display.flip()
    # limits FPS to 60
    clock.tick(60)

# Close the library and quit the screen
pygame.quit()
