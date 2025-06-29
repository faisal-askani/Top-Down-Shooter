import pygame
import math


class Bullet:
    def __init__(self, player_size, get_player_center, get_gun_radian):
        self._get_player_center = get_player_center
        self._get_gun_radian = get_gun_radian
        self.player_size = player_size
        self.nozzle_offset_distance = 40
        self.bullet_speed = 12
        self.bullets = []
        self.bullet_sprite = pygame.transform.scale(pygame.image.load("assets/extras/bullet.png").convert_alpha(),
                                                    (52, 52))

    def handle_input(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self._bullet_calculation()

    def draw(self, screen):
        self._update_bullet_position(screen)

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
                             "dir_y": bullet_dir_y
                             })

    def _update_bullet_position(self, screen):
        for bullet in self.bullets[:]:
            bullet["start_x"] += bullet["dir_x"] * self.bullet_speed
            bullet["start_y"] += bullet["dir_y"] * self.bullet_speed
            bullet_rect = self.bullet_sprite.get_rect(center=(int(bullet["start_x"]),
                                                              int(bullet["start_y"])))
            screen.blit(self.bullet_sprite, bullet_rect)

            if (bullet["start_x"] < 0 or bullet["start_x"] > 1920 or bullet["start_y"] < 0 or bullet["start_y"] > 1080):
                self.bullets.remove(bullet)
