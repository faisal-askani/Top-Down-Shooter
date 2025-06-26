import pygame
import math


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.player_speed = 5
        self.player_size = (120, 120)
        self.player_idle = self.sprite_loader("assets/idle/idle", 6)
        self.player_walk = self.sprite_loader("assets/walk/walk", 9)
        self.gun_sprite = pygame.transform.scale(pygame.image.load("assets/weapon/shotgun.png").convert_alpha(),
                                                 (92, 29))
        self.crosshair_sprite = pygame.transform.scale(pygame.image.load("assets/extras/crosshair.png").convert_alpha(),
                                                       (32, 32))
        self.moving = False
        self.animation_count = 0
        self.frames_per_image = 2

    def sprite_loader(self, path, length):
        sprite = []
        for i in range(length):
            sprite.append(pygame.transform.scale(pygame.image.load(f"{path}_{i}.png").convert_alpha(),
                                                 self.player_size))
        return sprite

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
        self.player(screen)
        self.gun(screen)
        self.cross_hair(screen)

    def animation_frame_counter(self, length):
        if self.animation_count + 1 >= length * self.frames_per_image:
            self.animation_count = 0
        self.animation_count += 1

    def player(self, screen):
        if self.moving:
            sprite_list = self.player_walk
        else:
            sprite_list = self.player_idle

        sprite_len = len(sprite_list)
        self.animation_frame_counter(sprite_len)
        frame_index = self.animation_count // self.frames_per_image
        current_sprite = sprite_list[frame_index]
        screen.blit(current_sprite, (self.x, self.y))

    def gun(self, screen):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        player_center_x = (self.x + self.player_size[0] // 2)
        player_center_y = (self.y + self.player_size[1] // 2) + 35

        dx = mouse_x - player_center_x
        dy = mouse_y - player_center_y
        angle = math.degrees(math.atan2(-dy, dx))

        # Flip the gun if aiming to the left
        gun = pygame.transform.flip(self.gun_sprite,
                                    False, True) if dx < 0 else self.gun_sprite

        # Rotate the (possibly flipped) gun
        rotated_gun = pygame.transform.rotate(gun, angle)
        gun_rect = rotated_gun.get_rect(center=(player_center_x,
                                                player_center_y))

        screen.blit(rotated_gun, gun_rect.topleft)

    def cross_hair(self, screen):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        crosshair_rect = self.crosshair_sprite.get_rect(
            center=(mouse_x, mouse_y))
        screen.blit(self.crosshair_sprite, crosshair_rect.topleft)
