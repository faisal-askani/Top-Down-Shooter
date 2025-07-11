import pygame
import random
from player import Player
from bullet import Bullet
from big_demon import BigDemon
from suicide_bomber import Suicide_Bomber
from orc import Orc


# Size of your game window in pixels.
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
TITLE = "Shapatar Londa"
BACKGROUND_COLOR = (109, 105, 135)

# Initialize pygame modules(display, sound, input)
pygame.init()
pygame.mixer.init()
# Sets the number of simultaneous sound channels for the mixer.
pygame.mixer.set_num_channels(32)
# pygame.mouse.set_visible(False)  # Hide system cdursor
# Creates the game window with the specified width and height.
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# Sets the title of the game window
pygame.display.set_caption(title=TITLE)
clock = pygame.time.Clock()
pygame.mixer.music.load("assets/audio/retro_future.mp3")
pygame.mixer.music.set_volume(0.2)  # Volume: 0.0 to 1.0
pygame.mixer.music.play(-1)  # -1 = loop forever
# ------------------------------------------------------------------------------------------------
num_big_demons = 4  # Number of Demons
num_suicide_bombers = 4  # Number of Bombers
num_orc = 4
spawn_margin = 300  # How far outside the screen enemies can spawn


# --- Function to get random off-screen position ---
def get_random_offscreen_position(margin):
    side = random.choice(['top', 'bottom', 'left', 'right'])

    if side == 'left':
        rand_x = random.randint(-margin, -1)
        rand_y = random.randint(0, SCREEN_HEIGHT)
    elif side == 'right':
        rand_x = random.randint(SCREEN_WIDTH + 1, SCREEN_WIDTH + margin)
        rand_y = random.randint(0, SCREEN_HEIGHT)
    elif side == 'top':
        rand_x = random.randint(0, SCREEN_WIDTH)
        rand_y = random.randint(-margin, -1)
    elif side == 'bottom':
        rand_x = random.randint(0, SCREEN_WIDTH)
        rand_y = random.randint(SCREEN_HEIGHT + 1, SCREEN_HEIGHT + margin)

    return rand_x, rand_y


# --- spawn_enemies ---
def spawn_enemies(enemy_class, num_of_enemies):
    enemies = []
    for _ in range(num_of_enemies):
        rand_x, rand_y = get_random_offscreen_position(spawn_margin)
        enemies.append(enemy_class(rand_x, rand_y,
                                   player.get_center,
                                   player.on_player_body_entered))
    return enemies


background_image = pygame.transform.scale(pygame.image.load("assets/environment/background2.png"),
                                          (1920, 1080))

# A combined list of all active enemies for player bullet collision checks
all_enemies = []
# List to hold all active DemonFire projectiles
demon_fire_projectiles = []
player = Player(900, 400)


orcs = spawn_enemies(Orc, num_orc)
big_demons = spawn_enemies(BigDemon, num_big_demons)
suicide_bombers = spawn_enemies(Suicide_Bomber, num_suicide_bombers)

# Player's bullet no longer takes specific enemy functions, but expects a list of enemies later
bullet = Bullet(player.get_center, player.get_radian)
# ------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------
first_wave = True
second_wave = False
third_wave = False
final_wave = False


# --- Update and populate all_enemies list for bullet collision ---
def clear_and_append_enemies():
    all_enemies.clear()  # Clear it each frame
    for demon in big_demons:
        if not demon.death_animation_done:  # Only add if not dead
            all_enemies.append(demon)
    for bomber in suicide_bombers:
        if not bomber.death_animation_done:  # Only add if not dead
            all_enemies.append(bomber)
    for orc in orcs:
        if not orc.death_animation_done:  # Only add if not dead
            all_enemies.append(orc)


# ---------------------- Update and draw Orcs ---------------------
def update_and_draw_orc():
    global first_wave, second_wave, third_wave, final_wave
    for orc in orcs[:]:  # Iterate over a slice
        orc.draw(screen)
        if orc.enemy_rect and orc.enemy_rect.colliderect(player.get_collision_rect()):
            player.on_player_body_entered()
        # Remove dead orc
        if orc.death_animation_done:
            orcs.remove(orc)
    if not orcs:
        first_wave = False
        second_wave = True
    print("second wave: ", second_wave)

# ------ Update and draw BigDemons and Independent DemonFire ------
def update_and_draw_demon_and_fire():
    global first_wave, second_wave, third_wave, final_wave
    for demon in big_demons[:]:
        # BigDemon now handles its own movement and animation
        demon.draw(screen)

        # --- BigDemon fires independent DemonFire projectiles ---
        new_fire_projectile = demon.fire_projectile(player.get_center())
        if new_fire_projectile:
            demon_fire_projectiles.append(new_fire_projectile)

        # --- Player takes damage from BigDemon (direct contact) ---
        if demon.enemy_rect and demon.enemy_rect.colliderect(player.get_collision_rect()):
            # Direct contact damage: 1 hit point
            player.on_player_body_entered()

        # Remove dead demons (Point 2)
        if demon.death_animation_done:
            big_demons.remove(demon)

    if not big_demons:
        second_wave = False
        third_wave = True
    print("third wave: ", third_wave)


def demon_fire_generation():
    # DemonFire: Iterate over a copy for safe removal
    for fire_bullet in demon_fire_projectiles[:]:
        fire_bullet.update(screen)
        # Check collision with player for DemonFire projectiles
        if fire_bullet.get_collision_rect().colliderect(player.get_collision_rect()):
            # Projectile hit damage: 1 hit point
            player.on_player_body_entered()
            fire_bullet.has_hit = True  # Mark for removal

        # Remove if off-screen or has hit
        if (fire_bullet.has_hit or
            fire_bullet.x < -100 or
            fire_bullet.x > SCREEN_WIDTH + 100 or
            fire_bullet.y < -100 or
                fire_bullet.y > SCREEN_HEIGHT + 100):
            demon_fire_projectiles.remove(fire_bullet)


# ----------------- Update and draw SuicideBombers ----------------
def update_and_draw_suicide_bomber():
    for bomber in suicide_bombers[:]:  # Iterate over a slice
        bomber.draw(screen)
        if bomber.enemy_rect and bomber.enemy_rect.colliderect(player.get_collision_rect()):
            player.on_player_body_entered(bomber=True)
        # Remove dead bombers
        if bomber.death_animation_done:
            suicide_bombers.remove(bomber)


running = True
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

    # --- Update and populate all_enemies list for bullet collision ---
    clear_and_append_enemies()
    # Pass all active enemies to the player's bullet manager for collision checks
    bullet.handle_input(screen)
    bullet.draw(screen, all_enemies)

    # --------------------- Update and draw Ocrs ----------------------
    if first_wave:
        update_and_draw_orc()

    # ------ Update and draw BigDemons and Independent DemonFire ------
    if second_wave:
        update_and_draw_demon_and_fire()
    demon_fire_generation()

    # ----------------- Update and draw SuicideBombers ----------------
    if third_wave:
        update_and_draw_suicide_bomber()

    # -----------------------------------------------------------------

    #######################################################################

    # flip() the display to put your work on screen
    pygame.display.flip()
    # limits FPS to 60
    clock.tick(60)

# Close the library and quit the screen
pygame.quit()
