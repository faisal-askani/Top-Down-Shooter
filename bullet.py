import pygame
import math


class Bullet:
    def __init__(self, get_player_center, get_gun_radian):
        self._get_player_center = get_player_center
        self._get_gun_radian = get_gun_radian
        self.nozzle_offset_distance = 90
        self.bullet_speed = 10
        self.bullets = []
        self.bullet_sprite = pygame.transform.scale(pygame.image.load("assets/extras/bullet.png").convert_alpha(),
                                                    (52, 52))
        self.nozzle_flash = pygame.transform.scale(pygame.image.load("assets/extras/muzzle.png").convert_alpha(),
                                                   (52, 52))
        self.gun_sound = pygame.mixer.Sound(
            "assets/audio/20 Gauge/WAV/20_Gauge_Single_Isolated.wav")

        self.last_shot_time = 0  # To control firing rate
        self.fire_rate_delay = 150  # milliseconds between shots

    def handle_input(self, screen):
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0]:  # [0] is the left mouse button
            current_time = pygame.time.get_ticks()
            if current_time - self.last_shot_time > self.fire_rate_delay:
                self.gun_sound.play()
                self._nozzle_flash_calculation(screen)
                self._bullet_calculation()
                self.last_shot_time = current_time

    def draw(self, screen, all_enemies):
        self._update_bullet_position(screen, all_enemies)

    def _nozzle_flash_calculation(self, screen):
        mouse_x, _ = pygame.mouse.get_pos()
        gun_pivot_x, gun_pivot_y = self._get_player_center()
        angle_rad = self._get_gun_radian()
        cos_angle = math.cos(angle_rad)
        sin_angle = math.sin(angle_rad)
        flash_offset_distance = 65
        flash_center_x = gun_pivot_x + cos_angle * flash_offset_distance
        flash_center_y = gun_pivot_y - sin_angle * flash_offset_distance

        dx_to_mouse = mouse_x - gun_pivot_x

        if dx_to_mouse < 0:
            current_flash_sprite = pygame.transform.flip(self.nozzle_flash,
                                                         False, True)
            flash_center_x = int(flash_center_x) - 8
        else:
            current_flash_sprite = self.nozzle_flash
            flash_center_x = int(flash_center_x) + 8

        rotated_flash = pygame.transform.rotate(
            current_flash_sprite, math.degrees(angle_rad))

        flash_rect = rotated_flash.get_rect(center=(int(flash_center_x),
                                                    int(flash_center_y) - 3))
        screen.blit(rotated_flash, flash_rect.topleft)

    def _bullet_calculation(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        gun_pivot_x, gun_pivot_y = self._get_player_center()
        angle_rad = self._get_gun_radian()
        gun_facing_x = math.cos(angle_rad)
        gun_facing_y = math.sin(angle_rad)
        bullet_start_x = gun_pivot_x + gun_facing_x * self.nozzle_offset_distance
        bullet_start_y = gun_pivot_y - gun_facing_y * self.nozzle_offset_distance

        bullet_dir_x = mouse_x - bullet_start_x
        bullet_dir_y = mouse_y - bullet_start_y
        distance = math.hypot(bullet_dir_x, bullet_dir_y)
        if distance == 0:
            return

        bullet_dir_x /= distance
        bullet_dir_y /= distance
        self.bullets.append({"start_x": bullet_start_x,
                             "start_y": bullet_start_y,
                             "dir_x": bullet_dir_x,
                             "dir_y": bullet_dir_y,
                             "has_hit": False
                             })

    def _update_bullet_position(self, screen, all_enemies):
        for bullet in self.bullets[:]:
            if bullet["has_hit"]:
                self.bullets.remove(bullet)
                continue

            bullet["start_x"] += bullet["dir_x"] * self.bullet_speed
            bullet["start_y"] += bullet["dir_y"] * self.bullet_speed

            collision_size = 20
            bullet_center = (int(bullet["start_x"]), int(bullet["start_y"]))
            bullet_collision_rect = pygame.Rect(
                0, 0, collision_size, collision_size)
            bullet_collision_rect.center = bullet_center

            self._check_collision(bullet, all_enemies, bullet_collision_rect)

            bullet_draw_rect = self.bullet_sprite.get_rect(
                center=bullet_center)

            # self._on_body_entered(bullet_collision, bullet)
            screen.blit(self.bullet_sprite, bullet_draw_rect)
            self.debug_bullets(screen, bullet_collision_rect)

            if (bullet["start_x"] < 0 or
                bullet["start_x"] > 1920 or
                bullet["start_y"] < 0 or
                    bullet["start_y"] > 1080):
                self.bullets.remove(bullet)

    def _check_collision(self, bullet, all_enemies, bullet_collision_rect):
        for enemy in all_enemies:
            enemy_rect = enemy.get_enemy_collision_rect()
            if enemy_rect and bullet_collision_rect.colliderect(enemy_rect):
                bullet["has_hit"] = True  # Mark bullet for removal
                enemy.is_bullet_hit()  # Call enemy's hit method (Point 2)
                break  # Bullet hit one enemy, so stop checking and move to next bullet

    def debug_bullets(self, screen, bullet_rect):
        pygame.draw.rect(screen, (0, 255, 0), bullet_rect, 2)
