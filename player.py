import pygame


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.player_speed = 5
        self.player_size = (120, 120)
        self.player_idle = self.sprite_loader("assets/idle/idle", 6)
        self.player_walk = self.sprite_loader("assets/walk/walk", 9)
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
        self.moving = self.moving = keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_a] or keys[pygame.K_d]

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

        if self.moving:
            sprite_list = self.player_walk
        else:
            sprite_list = self.player_idle

        sprite_len = len(sprite_list)
        self.animation_frame_counter(sprite_len)
        screen.blit(sprite_list[self.animation_count // self.frames_per_image],
                    (self.x, self.y))

    def animation_frame_counter(self, length):
        if self.animation_count + 1 >= length * self.frames_per_image:
            self.animation_count = 0
        self.animation_count += 1
