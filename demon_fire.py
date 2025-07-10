import pygame
import math


class Bullet:
    def __init__(self, get_player_center, get_gun_radian, get_enemy_collision, is_bullet_hit):
        self._get_player_center = get_player_center
        self._get_gun_radian = get_gun_radian
        self._get_enemy_collision = get_enemy_collision
        self.is_bullet_hit = is_bullet_hit
        self.nozzle_offset_distance = 90
        self.bullet_speed = 1
        self.bullets = []
        self.bullet_sprite = pygame.transform.scale(pygame.image.load("assets/extras/bullet.png").convert_alpha(),
                                                    (52, 52))
        self.nozzle_flash = pygame.transform.scale(pygame.image.load("assets/extras/muzzle.png").convert_alpha(),
                                                   (52, 52))

    def handle_input(self, events, screen):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self._nozzle_flash_calculation(screen)
                self._bullet_calculation()

    def draw(self, screen):
        self._update_bullet_position(screen)

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

    def _update_bullet_position(self, screen):
        for bullet in self.bullets[:]:
            if bullet["has_hit"]:
                self.bullets.remove(bullet)
                continue

            bullet["start_x"] += bullet["dir_x"] * self.bullet_speed
            bullet["start_y"] += bullet["dir_y"] * self.bullet_speed

            collision_size = 20
            bullet_center = (int(bullet["start_x"]), int(bullet["start_y"]))
            bullet_collision = pygame.Rect(
                0, 0, collision_size, collision_size)
            bullet_collision.center = bullet_center
            bullet_draw_rect = self.bullet_sprite.get_rect(
                center=bullet_center)

            self._on_body_entered(bullet_collision, bullet)
            screen.blit(self.bullet_sprite, bullet_draw_rect)
            self.debug_bullets(screen, bullet_collision)

            if (bullet["start_x"] < 0 or
                bullet["start_x"] > 1920 or
                bullet["start_y"] < 0 or
                    bullet["start_y"] > 1080):
                self.bullets.remove(bullet)

    def _on_body_entered(self, bullet_rect, bullet):
        if bullet_rect.colliderect(self._get_enemy_collision()):
            bullet["has_hit"] = True
            self.is_bullet_hit(True)

    def debug_bullets(self, screen, bullet_rect):
        pygame.draw.rect(screen, (0, 255, 0), bullet_rect, 2)
