import pygame
import math


class Bullet:
    def __init__(self, player_size, get_player_position):
        self._get_player_position = get_player_position
        self.player_size = player_size
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
        x, y = self._get_player_position()
        player_center_x = x + self.player_size[0] // 2
        player_center_y = y + self.player_size[1] // 2
        diretion_x = mouse_x - player_center_x
        direction_y = mouse_y - player_center_y
        distance = math.hypot(diretion_x, direction_y)

        if distance == 0:
            return  # Prevent divide by zero

        diretion_x /= distance
        direction_y /= distance

        bullet = {
            "start_x": player_center_x,
            "start_y": player_center_y,
            "dir_x": diretion_x,
            "dir_y": direction_y
        }
        self.bullets.append(bullet)

    def _update_bullet_position(self, screen):
        for bullet in self.bullets[:]:
            bullet["start_x"] += bullet["dir_x"] * self.bullet_speed
            bullet["start_y"] += bullet["dir_y"] * self.bullet_speed
            screen.blit(self.bullet_sprite,
                        (bullet["start_x"], bullet["start_y"]))

            # Remove bullets that go off screen
            if (bullet["start_x"] < 0 or bullet["start_x"] > 1280 or bullet["start_y"] < 0 or bullet["start_y"] > 720):
                self.bullets.remove(bullet)
