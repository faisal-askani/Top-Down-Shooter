import pygame


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.player_speed = 5
        self.player_size = (250, 250)
        self.player_idle = self.sprite_loader("assets/idle/idle", 6)
        self.player_walk = self.sprite_loader("assets/walk/walk", 9)
        self.moving = False
        self.animation_count = 0
        self.frames_per_image = 3

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


#         self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
#         self.shoot_cooldown = 0

#     def update(self, keys):
#         # Handle movement based on key presses
#         if keys[pygame.K_LEFT]:
#             self.x -= self.speed
#         if keys[pygame.K_RIGHT]:
#             self.x += self.speed
#         if keys[pygame.K_UP]:
#             self.y -= self.speed
#         if keys[pygame.K_DOWN]:
#             self.y += self.speed

#         # Limit movement to window boundaries
#         self.x = max(0, min(self.x, WIDTH - self.width))
#         self.y = max(0, min(self.y, HEIGHT - self.height))

#         # Update rectangle position
#         self.rect.x = self.x
#         self.rect.y = self.y


# class Player(pg.sprite.Sprite):
#     """Representing the player as a moon buggy type car."""

#     speed = 10
#     bounce = 24
#     gun_offset = -11
#     images: List[pg.Surface] = []

#     def __init__(self, *groups):
#         pg.sprite.Sprite.__init__(self, *groups)
#         self.image = self.images[0]
#         self.rect = self.image.get_rect(midbottom=SCREENRECT.midbottom)
#         self.reloading = 0
#         self.origtop = self.rect.top
#         self.facing = -1

#     def move(self, direction):
#         if direction:
#             self.facing = direction
#         self.rect.move_ip(direction * self.speed, 0)
#         self.rect = self.rect.clamp(SCREENRECT)
#         if direction < 0:
#             self.image = self.images[0]
#         elif direction > 0:
#             self.image = self.images[1]
#         self.rect.top = self.origtop - (self.rect.left // self.bounce % 2)

#     def gunpos(self):
#         pos = self.facing * self.gun_offset + self.rect.centerx
#         return pos, self.rect.top


# # Player class
# class Player:
#     def __init__(self):
#         # Start at the center-bottom of the screen
#         self.x = WIDTH // 2 - PLAYER_SIZE // 2
#         self.y = HEIGHT - PLAYER_SIZE - 50
#         self.width = PLAYER_SIZE
#         self.height = PLAYER_SIZE
#         self.speed = PLAYER_SPEED
#         self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
#         self.shoot_cooldown = 0

#     def update(self, keys):
#         # Handle movement based on key presses
#         if keys[pygame.K_LEFT]:
#             self.x -= self.speed
#         if keys[pygame.K_RIGHT]:
#             self.x += self.speed
#         if keys[pygame.K_UP]:
#             self.y -= self.speed
#         if keys[pygame.K_DOWN]:
#             self.y += self.speed

#         # Limit movement to window boundaries
#         self.x = max(0, min(self.x, WIDTH - self.width))
#         self.y = max(0, min(self.y, HEIGHT - self.height))

#         # Update rectangle position
#         self.rect.x = self.x
#         self.rect.y = self.y

#         # Update cooldown
#         if self.shoot_cooldown > 0:
#             self.shoot_cooldown -= 1

#     def shoot(self):
#         if self.shoot_cooldown == 0:
#             # Create a bullet at the center-top of the player
#             bullet_x = self.x + (self.width // 2) - (BULLET_WIDTH // 2)
#             bullet_y = self.y
#             self.shoot_cooldown = 10  # Add a small cooldown between shots
#             return Bullet(bullet_x, bullet_y)
#         return None

#     def draw(self, surface):
#         pygame.draw.rect(surface, BLUE, self.rect)
