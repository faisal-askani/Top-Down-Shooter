import pygame
import random
import math
import sys
from player import Player
from bullet import Bullet
from big_demon import BigDemon
from suicide_bomber import Suicide_Bomber
from orc import Orc


class GameManager:
    def __init__(self, SCREEN_WIDTH=1920, SCREEN_HEIGHT=1080, num_orc=2, num_big_demons=2, num_suicide_bombers=2):
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.screen = None
        self.clock = None

        self._pygame_init(title="shapatar",
                          load_music='assets/audio/retro_future.mp3',
                          num_audio_channels=100)

        self.player = Player(900, 400)
        self.bullet = Bullet(self.player.get_center, self.player.get_radian)

        self.num_orc = num_orc
        self.num_big_demons = num_big_demons
        self.num_suicide_bombers = num_suicide_bombers
        self.orcs = self.spawn_enemies(Orc, self.num_orc)
        self.big_demons = self.spawn_enemies(BigDemon, self.num_big_demons)
        self.suicide_bombers = self.spawn_enemies(Suicide_Bomber,
                                                  self.num_suicide_bombers)

        self.all_enemies = []  # List of all active enemies for player bullet collision checks
        self.demon_fire_projectiles = []  # List to hold all active DemonFire projectiles

        self.state = "MENU"
        self.running = True
        self.first_wave = True
        self.second_wave = False
        self.third_wave = False
        # self.final_wave = False
        self.reset = False
        self.show_text = True
        self.blink_interval = 500  # milliseconds
        self.last_blink_time = 0

        font_path = "assets/font/Early GameBoy.ttf"  # replace with actual filename
        self.mm_font = pygame.font.Font(font_path, 18)
        self.g_font = pygame.font.Font(font_path, 72)
        self.p_font = pygame.font.Font(font_path, 32)

        self.intro_image = pygame.transform.scale(pygame.image.load("assets/extras/monster_hunter_intro_red.png"),
                                                  (1920, 1080))
        self.background_image = pygame.transform.scale(pygame.image.load("assets/environment/background2.png"),
                                                       (1920, 1080))

        self.is_state_shifting_timer_started = False
        self.state_shifting_timer_start_time = 0

    # ----------------------------- Init pygame -----------------------------

    def _pygame_init(self, title, load_music, num_audio_channels=32, set_audio_vol=0.3):
        pygame.init()
        pygame.mixer.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH,
                                               self.SCREEN_HEIGHT))
        pygame.display.set_caption(title=title)
        pygame.mouse.set_visible(False)
        pygame.mixer.music.load(load_music)
        pygame.mixer.set_num_channels(num_audio_channels)
        pygame.mixer.music.set_volume(set_audio_vol)  # Volume: 0.0 to 1.0
        pygame.mixer.music.play(-1)  # -d1 = loop forever
        # return (self.clock, self.screen)

    def reset_game(self):
        self.first_wave = True
        self.second_wave = False
        self.third_wave = False
        self.final_wave = False
        self.is_state_shifting_timer_started = False
        self.player = Player(900, 400)
        self.bullet = Bullet(self.player.get_center, self.player.get_radian)
        self.orcs = self.spawn_enemies(Orc, self.num_orc)
        self.big_demons = self.spawn_enemies(BigDemon, self.num_big_demons)
        self.suicide_bombers = self.spawn_enemies(Suicide_Bomber,
                                                  self.num_suicide_bombers)
        self.all_enemies = []
        self.demon_fire_projectiles = []

    # -------------- Function To Get Random off-screen Position --------------

    def get_random_offscreen_position(self, margin):
        side = random.choice(['top', 'bottom', 'left', 'right'])

        if side == 'left':
            rand_x = random.randint(-margin, -1)
            rand_y = random.randint(0, self.SCREEN_HEIGHT)
        elif side == 'right':
            rand_x = random.randint(self.SCREEN_WIDTH + 1,
                                    self.SCREEN_WIDTH + margin)
            rand_y = random.randint(0, self.SCREEN_HEIGHT)
        elif side == 'top':
            rand_x = random.randint(0, self.SCREEN_WIDTH)
            rand_y = random.randint(-margin, -1)
        elif side == 'bottom':
            rand_x = random.randint(0, self.SCREEN_WIDTH)
            rand_y = random.randint(self.SCREEN_HEIGHT + 1,
                                    self.SCREEN_HEIGHT + margin)
        return rand_x, rand_y

    # ----------------------------- Spawn Enemies -----------------------------

    def spawn_enemies(self, enemy_class, num_of_enemies):
        enemies = []
        # unique (x, y) positions of enemies
        used_positions = set()
        # minimum distance between spawned enemies
        minimum_distance = 600
        spawn_margin = 700  # How far outside the screen enemies can spawn

        for _ in range(num_of_enemies):
            position_found = False
            while not position_found:
                rand_x, rand_y = self.get_random_offscreen_position(
                    spawn_margin)
                new_position = (rand_x, rand_y)

                if new_position in used_positions:
                    continue

                # if position is too close existing position
                too_close = False
                for existing_x, existing_y in used_positions:
                    distance = math.hypot(
                        rand_x - existing_x, rand_y - existing_y)
                    if distance < minimum_distance:
                        too_close = True
                        break

                if not too_close:
                    used_positions.add(new_position)
                    position_found = True            # Mark as found to exit the loop

            enemies.append(enemy_class(rand_x, rand_y,
                                       self.player.get_center,
                                       self.player.on_player_body_entered))
        return enemies

   # --- Update And Populate all_enemies List For Bullet Collision ---

    def clear_and_append_enemies(self):
        self.all_enemies.clear()  # Clear it each frame
        for demon in self.big_demons:
            if not demon.death_animation_done:  # Only add if not dead
                self.all_enemies.append(demon)
        for bomber in self.suicide_bombers:
            if not bomber.death_animation_done:  # Only add if not dead
                self.all_enemies.append(bomber)
        for orc in self.orcs:
            if not orc.death_animation_done:  # Only add if not dead
                self.all_enemies.append(orc)

    # ---------------------- Update And Draw Orcs ---------------------

    def update_and_draw_orc(self):
        for orc in self.orcs[:]:
            orc.draw(self.screen)
            if orc.enemy_rect and orc.enemy_rect.colliderect(self.player.get_collision_rect()):
                self.player.on_player_body_entered()
            # Remove dead orc
            if orc.death_animation_done:
                self.orcs.remove(orc)
        if not self.orcs:
            self.first_wave = False
            self.second_wave = True
            print("second wave: ", self.second_wave)

    # ------ Update And Draw BigDemons And Independent DemonFire ------

    def update_and_draw_demon_and_fire(self):
        global first_wave, second_wave, third_wave, final_wave
        for demon in self.big_demons[:]:
            demon.draw(self.screen)

            # --- BigDemon fires independent DemonFire projectiles ---
            new_fire_projectile = demon.fire_projectile(
                self.player.get_center())
            if new_fire_projectile:
                self.demon_fire_projectiles.append(new_fire_projectile)

            # --- Player takes damage from BigDemon (direct contact) ---
            if demon.enemy_rect and demon.enemy_rect.colliderect(self.player.get_collision_rect()):
                # Direct contact damage: 1 hit point
                self.player.on_player_body_entered()

            # Remove dead demons (Point 2)
            if demon.death_animation_done:
                self.big_demons.remove(demon)

        if not self.big_demons:
            self.second_wave = False
            self.third_wave = True
            print("third wave: ", self.third_wave)

    def demon_fire_generation(self):
        # DemonFire: Iterate over a copy for safe removal
        for fire_bullet in self.demon_fire_projectiles[:]:
            fire_bullet.update(self.screen)
            # Check collision with player for DemonFire projectiles
            if fire_bullet.get_collision_rect().colliderect(self.player.get_collision_rect()):
                # Projectile hit damage: 1 hit point
                self.player.on_player_body_entered()
                fire_bullet.has_hit = True  # Mark for removal

            # Remove if off-screen or has hit
            if (fire_bullet.has_hit or
                fire_bullet.x < -100 or
                fire_bullet.x > self.SCREEN_WIDTH + 100 or
                fire_bullet.y < -100 or
                    fire_bullet.y > self.SCREEN_HEIGHT + 100):
                self.demon_fire_projectiles.remove(fire_bullet)

    # ----------------- Update And Draw SuicideBombers ----------------

    def update_and_draw_suicide_bomber(self):
        for bomber in self.suicide_bombers[:]:  # Iterate over a slice
            bomber.draw(self.screen)
            if bomber.enemy_rect and bomber.enemy_rect.colliderect(self.player.get_collision_rect()):
                self.player.on_player_body_entered(bomber=True)
            # Remove dead bombers
            if bomber.death_animation_done:
                self.suicide_bombers.remove(bomber)

    # ------------------------ Text Blink Logic ----------------------

    def text_blink(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_blink_time >= self.blink_interval:
            self.show_text = not self.show_text
            self.last_blink_time = current_time
        return self.show_text

    # ---------------------- State Shifter Delay ---------------------

    def dely_State_shifting(self):
        if not self.is_state_shifting_timer_started:
            self.is_state_shifting_timer_started = True
            self.state_shifting_timer_start_time = pygame.time.get_ticks()

        if pygame.time.get_ticks() - self.state_shifting_timer_start_time >= 500:
            return True

    # ------------------- You Win and Game Over Logic ------------------

    def win_and_game_over(self):
        if self.player.death:
            if self.third_wave:
                if len(self.suicide_bombers) <= 1:
                    print('ok')
                    self.reset = True
                    self.state = "GAME_OVER"
            else:
                if self.dely_State_shifting():
                    self.reset = True
                    self.state = "GAME_OVER"

        elif not self.suicide_bombers and not self.player.death_animation_done:
            if self.dely_State_shifting():
                self.reset = True
                self.state = "WIN"

    # ------------- Game Manger State Managing Functions -------------

    def run(self):
        self.running
        while self.running:
            if self.state == "MENU":
                self.main_menu()
            elif self.state == "PLAY":
                self.play()
            elif self.state == "WIN":
                if self.reset:
                    print("reset")
                    self.reset_game()
                self.win()
            elif self.state == "GAME_OVER":
                if self.reset:
                    print("reset")
                    self.reset_game()
                self.game_over()

    def main_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                self.state = "PLAY"

        self.screen.blit(self.intro_image, (0, 0))
        show_text = self.text_blink()

        if show_text:
            p_text_surface = self.mm_font.render(
                "Press any key to play", True, (255, 255, 255))
            press_text_rect = p_text_surface.get_rect(center=(930, 1010))
            self.screen.blit(p_text_surface, press_text_rect)

        d_text_surface = self.mm_font.render(
            "Developer: Faisal Askani", True, (255, 255, 255))
        d_text_rect = d_text_surface.get_rect(center=(930, 1050))
        self.screen.blit(d_text_surface, d_text_rect)

        pygame.display.update()
        self.clock.tick(60)

    def play(self):
        # Poll for events
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        ######################## RENDER YOUR GAME HERE ########################

        # Render background image at x=0 and y=0
        self.screen.blit(self.background_image, (0, 0))
        self.player.handle_input()
        self.player.draw(self.screen)

        # --- Update and populate all_enemies list for bullet collision ---
        self.clear_and_append_enemies()
        # Pass all active enemies to the player's bullet manager for collision checks
        self.bullet.handle_input(self.screen)
        self.bullet.draw(self.screen, self.all_enemies)

        # --------------------- Update and draw Ocrs ----------------------
        if self.first_wave:
            self.update_and_draw_orc()

        # ------ Update and draw BigDemons and Independent DemonFire ------
        if self.second_wave:
            self.update_and_draw_demon_and_fire()
        self.demon_fire_generation()

        # ----------------- Update and draw SuicideBombers ----------------
        if self.third_wave:
            self.update_and_draw_suicide_bomber()

        # ------------------- You Win and Game Over Logic ------------------

        self.win_and_game_over()

        #######################################################################

        # flip() the display to put your work on screen
        pygame.display.flip()
        # limits FPS to 60
        self.clock.tick(60)

    def win(self):
        self.reset = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                self.state = "MENU"

        # screen.fill(background)
        self.screen.blit(self.background_image, (0, 0))
        g_text_surface = self.g_font.render(
            "You Win", True, (255, 255, 255))
        g_text_rect = g_text_surface.get_rect(center=(930, 540))
        self.screen.blit(g_text_surface, g_text_rect)

        show_text = self.text_blink()

        if show_text:
            p_text_surface = self.p_font.render(
                "Press any key to Restart", True, (255, 255, 255))
            press_text_rect = p_text_surface.get_rect(center=(930, 650))
            self.screen.blit(p_text_surface, press_text_rect)

        pygame.display.update()
        self.clock.tick(60)

    def game_over(self):
        self.reset = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                self.state = "MENU"

        # screen.fill(background)
        self.screen.blit(self.background_image, (0, 0))
        g_text_surface = self.g_font.render(
            "Game Over", True, (255, 255, 255))
        g_text_rect = g_text_surface.get_rect(center=(930, 540))
        self.screen.blit(g_text_surface, g_text_rect)

        show_text = self.text_blink()

        if show_text:
            p_text_surface = self.p_font.render(
                "Press any key to Restart", True, (255, 255, 255))
            press_text_rect = p_text_surface.get_rect(center=(930, 650))
            self.screen.blit(p_text_surface, press_text_rect)

        pygame.display.update()
        self.clock.tick(60)
