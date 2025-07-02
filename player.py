import pygame
import math


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.player_speed = 5
        self.player_size = (150, 150)
        self.player_center = None
        self.gun_radian = None
        self.player_idle = self._sprite_loader("assets/player/idle/idle", 6)
        self.player_walk = self._sprite_loader("assets/player/walk//walk", 9)
        self.gun_sprite = self._sprite_loader(path="assets/weapon/rifle.png",
                                              size=(92, 46))
        self.crosshair_sprite = self._sprite_loader(path="assets/extras/crosshair.png",
                                                    size=(100, 100))
        self.moving = False
        self.animation_count = 0
        self.frames_per_image = 2

    def _sprite_loader(self, path, length=1, size=None):
        sprites = []
        if length == 1:
            image = pygame.image.load(path).convert_alpha()
            if size:
                image = pygame.transform.scale(image, size)
            sprites.append(image)
        else:
            for i in range(length):
                image = pygame.image.load(f"{path}_{i}.png").convert_alpha()
                image = pygame.transform.scale(image, self.player_size)
                sprites.append(image)

        return sprites if length > 1 else sprites[0]

    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.moving = keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_a] or keys[pygame.K_d]

        if keys[pygame.K_w]:
            self.y -= self.player_speed
            self.moving = True
        if keys[pygame.K_s]:
            self.y += self.player_speed
            self.moving = True
        if keys[pygame.K_d]:
            self.x += self.player_speed
            self.moving = True
        if keys[pygame.K_a]:
            self.x -= self.player_speed
            self.moving = True

    def draw(self, screen):
        self._player(screen)
        self._gun(screen)
        self._cross_hair(screen)

    def _animation_frame_counter(self, length):
        if self.animation_count + 1 >= length * self.frames_per_image:
            self.animation_count = 0
        self.animation_count += 1

    def _player(self, screen):
        if self.moving:
            sprite_list = self.player_walk
        else:
            sprite_list = self.player_idle

        sprite_len = len(sprite_list)
        self._animation_frame_counter(sprite_len)
        frame_index = self.animation_count // self.frames_per_image
        current_sprite = sprite_list[frame_index]
        screen.blit(current_sprite, (self.x, self.y))

    def _gun(self, screen):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        player_center_x = (self.x + self.player_size[0] // 2)
        player_center_y = (self.y + self.player_size[1] // 2) + 35
        self.player_center = (player_center_x, player_center_y)

        dx = mouse_x - player_center_x
        dy = mouse_y - player_center_y
        self.gun_radian = math.atan2(-dy, dx)
        angle = math.degrees(self.gun_radian)

        # Flip the gun if aiming to the left
        gun = pygame.transform.flip(self.gun_sprite,
                                    False, True) if dx < 0 else self.gun_sprite

        # Rotate the (possibly flipped) gun
        rotated_gun = pygame.transform.rotate(gun, angle)
        gun_rect = rotated_gun.get_rect(center=(player_center_x,
                                                player_center_y))

        screen.blit(rotated_gun, gun_rect.topleft)

    def _cross_hair(self, screen):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        crosshair_rect = self.crosshair_sprite.get_rect(
            center=(mouse_x, mouse_y))
        screen.blit(self.crosshair_sprite, crosshair_rect.topleft)

    def get_center(self):
        return self.player_center

    def get_radian(self):
        return self.gun_radian
    