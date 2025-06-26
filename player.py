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
        self.shotgun = pygame.transform.scale(pygame.image.load("assets/weapon/shotgun.png"),
                                              (92, 29))
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
        self.player_sprite(screen)
        self.gun_sprite(screen)

    def animation_frame_counter(self, length):
        if self.animation_count + 1 >= length * self.frames_per_image:
            self.animation_count = 0
        self.animation_count += 1

    def player_sprite(self, screen):
        if self.moving:
            sprite_list = self.player_walk
        else:
            sprite_list = self.player_idle

        sprite_len = len(sprite_list)
        self.animation_frame_counter(sprite_len)
        frame_index = self.animation_count // self.frames_per_image
        current_sprite = sprite_list[frame_index]
        screen.blit(current_sprite, (self.x, self.y))

    def gun_sprite(self, screen):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        player_center_x = (self.x + self.player_size[0] // 2)
        player_center_y = (self.y + self.player_size[1] // 2) + 35

        dx = mouse_x - player_center_x
        dy = mouse_y - player_center_y
        angle = math.degrees(math.atan2(-dy, dx))

        # Flip the gun if aiming to the left
        gun = pygame.transform.flip(self.shotgun,
                                    False, True) if dx < 0 else self.shotgun

        # Rotate the (possibly flipped) gun
        rotated_gun = pygame.transform.rotate(gun, angle)
        gun_rect = rotated_gun.get_rect(center=(player_center_x,
                                                player_center_y))

        screen.blit(rotated_gun, gun_rect.topleft)
