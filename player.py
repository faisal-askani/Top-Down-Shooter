import pygame
import math


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.player_speed = 5
        self.player_size = (150, 150)
        self.flip_dir = 0
        self.collision_size = (90, 150)
        self.player_center = None
        self.gun_radian = None
        self.player_idle = self._sprite_loader(path="assets/player/idle/idle",
                                               length=6,
                                               size=self.player_size)
        self.player_walk = self._sprite_loader(path="assets/player/walk//walk",
                                               length=9,
                                               size=self.player_size)
        self.player_hurt = self._sprite_loader(path="assets/player/hurt/hurt_0.png",
                                               size=self.player_size)
        self.player_death = self._sprite_loader(path="assets/death/death",
                                                length=5,
                                                size=self.player_size)
        self.gun_sprite = self._sprite_loader(path="assets/weapon/rifle.png",
                                              size=(92, 46))
        self.crosshair_sprite = self._sprite_loader(path="assets/extras/crosshair.png",
                                                    size=(100, 100))
        self.idle = True
        self.moving = False
        self.hurt = False
        self.death = False
        self.death_animation_done = False
        self.hit_count = 0
        self.animation_count = 0
        self.frames_per_image = 2
        self.player_collision = None

        # Time left in milliseconds where player is invincible after getting hit
        self.hurt_cooldown = 0
        self.last_hit_time = 0  # Store the time when the player was last hit
        self.hurt_duration = 300  # milliseconds (0.3 second flash/pause)

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
                image = pygame.transform.scale(image, size)
                sprites.append(image)

        return sprites if length > 1 else sprites[0]

    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.moving = keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_a] or keys[pygame.K_d]

        if not self.death:
            if keys[pygame.K_w]:
                self.y -= self.player_speed
            if keys[pygame.K_s]:
                self.y += self.player_speed
            if keys[pygame.K_d]:
                self.flip_dir = 1
                self.x += self.player_speed
            if keys[pygame.K_a]:
                self.flip_dir = -1
                self.x -= self.player_speed

    def draw(self, screen):
        if not self.death_animation_done:
            self._player(screen)
            if not self.death:
                self._gun(screen)
                self._cross_hair(screen)

    def _animation_frame_counter(self, length):
        if self.animation_count + 1 >= length * self.frames_per_image:
            self.animation_count = 0
        self.animation_count += 1

    def _player(self, screen):
        if self.hit_count > 3:
            self.frames_per_image = 6
            self._player_death_anim(screen, self.player_death)
        elif self.hurt:
            self._player_hurt_anim(screen, self.player_hurt)
        elif self.moving:
            self._player_walk_anim(screen, self.player_walk)
        else:
            self._player_idle_anim(screen, self.player_idle)

    def _blit_player_anim(self, screen, sprite_list):
        sprite_len = len(sprite_list)
        self._animation_frame_counter(sprite_len)
        frame_index = self.animation_count // self.frames_per_image
        current_sprite = self._flip_sprite(
            sprite_list[frame_index], self.flip_dir, False)

        player_center = self._player_center_calculation()
        self.player_collision = pygame.Rect(0, 0, *self.collision_size)
        self.player_collision.center = player_center
        player_rect = current_sprite.get_rect(center=player_center)

        screen.blit(current_sprite, player_rect)
        self.debug_player(screen, self.player_collision)

    def _player_walk_anim(self, screen, sprite_list):
        self._blit_player_anim(screen, sprite_list)

    def _player_idle_anim(self, screen, sprite_list):
        self._blit_player_anim(screen, sprite_list)

    def _player_death_anim(self, screen, sprite_list):
        self._blit_player_anim(screen, sprite_list)
        self.death = True
        frame_index = self.animation_count // self.frames_per_image
        print('frame: ', frame_index, " len of sprite: ", len(sprite_list))
        if frame_index >= len(sprite_list) - 1:
            print(self.death_animation_done, "hit animatiopn done")
            self.death_animation_done = True

    def _player_hurt_anim(self, screen, sprite):
        player_center = self._player_center_calculation()
        self.player_collision = pygame.Rect(0, 0, *self.collision_size)
        self.player_collision.center = player_center
        sprite = self._flip_sprite(sprite, self.flip_dir, False)
        player_rect = sprite.get_rect(center=player_center)
        screen.blit(sprite, player_rect)
        self.debug_player(screen, self.player_collision)
        self.hurt = False

    def _player_center_calculation(self):
        player_center_x = (self.x + self.player_size[0] // 2)
        player_center_y = (self.y + self.player_size[1] // 2)
        return (player_center_x, player_center_y)

    def _gun(self, screen):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        player_center = self._player_center_calculation()
        player_center_x, player_center_y = player_center[0], player_center[1] + 35
        self.player_center = (player_center_x, player_center_y)

        dx = mouse_x - player_center_x
        dy = mouse_y - player_center_y
        self.gun_radian = math.atan2(-dy, dx)
        angle = math.degrees(self.gun_radian)
        gun = self._flip_sprite(self.gun_sprite, dx)

        # Rotate the (possibly flipped) gun
        rotated_gun = pygame.transform.rotate(gun, angle)
        gun_rect = rotated_gun.get_rect(center=(player_center_x,
                                                player_center_y))
        screen.blit(rotated_gun, gun_rect.topleft)

    def _flip_sprite(self, sprite, direction, gun=True):
        if gun:
            fliped = pygame.transform.flip(sprite,
                                           False, True) if direction < 0 else sprite
        else:
            fliped = pygame.transform.flip(sprite,
                                           True, False) if direction < 0 else sprite
        return fliped

    def _cross_hair(self, screen):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        crosshair_rect = self.crosshair_sprite.get_rect(
            center=(mouse_x, mouse_y))
        screen.blit(self.crosshair_sprite, crosshair_rect.topleft)

    def on_player_body_entered(self, enemy_body, bomber=False):
        if self.player_collision.colliderect(enemy_body):
            if bomber:
                self.hit_count = 10
            self._handle_player_hit()

    def _handle_player_hit(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_hit_time > self.hurt_duration:
            self.moving = False
            self.hurt = True
            self.hit_count += 1
            self.last_hit_time = current_time
            print("Player hurt! Hit:", self.hit_count)

    def get_center(self):
        return self.player_center

    def get_radian(self):
        return self.gun_radian

    def get_collision_rect(self):
        return self.player_collision

    def debug_player(self, screen, rect):
        pygame.draw.rect(screen, (255, 0, 255), rect, 2)
