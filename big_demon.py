import pygame
import math
import random
from demon_fire import DemonFire


class BigDemon:
    def __init__(self, x, y, get_player_position, on_player_body_entered):
        self.x = x
        self.y = y
        self._on_player_body_entered = on_player_body_entered
        self._get_player_position = get_player_position
        self.flip_dir = 0
        self.enemy_speed = 2
        self.enemy_size = (128, 144)
        self.enemy_walk = self._sprite_loader(path="assets/enemy/big_demon/walk/walk",
                                              length=4,
                                              size=self.enemy_size)
        self.enemy_hurt = self._sprite_loader(path="assets/enemy/big_demon/hurt/hurt_0.png",
                                              size=self.enemy_size)
        self.enemy_death = self._sprite_loader(path="assets/death/death",
                                               length=5,
                                               size=(128, 128))
        self.hurt_sound = pygame.mixer.Sound(
            "assets/audio/big_demon_sound.wav")
        self.moving = True
        self.hurt = False
        self.death = False
        self.death_animation_done = False
        self.animation_count = 0
        self.frames_per_image = 5
        self.hit_count = 0
        # Initial rect for collision
        self.enemy_rect = None
        # DemonFire related variables
        # self.last_shot_time = 0

        # DemonFire related variables for RANDOM shoots
        # Define a range for random shoot intervals (e.g., between 2 and 7 seconds)
        self.min_shoot_interval = 2000  # 2 seconds
        self.max_shoot_interval = 7000  # 5 seconds
        # Initial random interval for the first shot
        self.shoot_interval = random.randint(self.min_shoot_interval,
                                             self.max_shoot_interval)
        # Randomize initial last_shot_time to offset firing
        # Each demon will start its firing countdown at a different point
        self.last_shot_time = pygame.time.get_ticks() + self.shoot_interval

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

    def draw(self, screen):
        self._enemy(screen)

    def _animation_frame_counter(self, length):
        if self.animation_count + 1 >= length * self.frames_per_image:
            self.animation_count = 0
        self.animation_count += 1

    def _enemy(self, screen):
        if not self.death:
            self._chase_player()
            if self.moving:
                self._enemy_walk_anim(screen, self.enemy_walk)
            elif self.hurt:
                self.moving = True
                self.hurt_sound.play()
                self._enemy_hit_anim(screen, self.enemy_hurt)

        if self.hit_count >= 3 and not self.death_animation_done:
            self._enemy_death_anim(screen, self.enemy_death)

        # self._on_player_body_entered(self.enemy_rect)

    def _blit_enemy_anim(self, screen, sprite_list):
        sprite_len = len(sprite_list)
        self._animation_frame_counter(sprite_len)
        frame_index = self.animation_count // self.frames_per_image
        current_sprite = self._flip_sprite(sprite_list[frame_index],
                                           self.flip_dir)
        self.enemy_rect = current_sprite.get_rect(center=(self.x, self.y))
        screen.blit(current_sprite, self.enemy_rect)
        # self.debug_enemy(screen, self.enemy_rect)

    def _flip_sprite(self, sprite, direction):
        fliped = pygame.transform.flip(sprite,
                                       True, False) if direction < 0 else sprite
        return fliped

    def _enemy_walk_anim(self, screen, sprite_list):
        self._blit_enemy_anim(screen, sprite_list)

    def _enemy_death_anim(self, screen, sprite_list):
        print("big demon death")
        self._blit_enemy_anim(screen, sprite_list)
        self.death = True
        self.moving = False
        self.hurt = False
        self._check_death_animation_done(sprite_list)

    def _enemy_hit_anim(self, screen, sprite):
        if self.hurt:
            print('hurt')
            self.enemy_rect = sprite.get_rect(center=(self.x, self.y))
            screen.blit(sprite, self.enemy_rect)
            # self.debug_enemy(screen, self.enemy_rect)
            self.hurt = False

    def _check_death_animation_done(self, sprite_list):
        frame_index = self.animation_count // self.frames_per_image
        if frame_index >= len(sprite_list) - 1:
            print(self.death_animation_done, "death animation done")
            self.death_animation_done = True

    def fire_projectile(self, player_position):
        # Only fire if not dead and not currently hurting/dying
        if self.death_animation_done or self.hit_count >= 3:
            return None

        current_time = pygame.time.get_ticks()

        if current_time - self.last_shot_time >= self.shoot_interval:
            enemy_x, enemy_y = self.get_center()
            # change it,Get actual player position from main.py
            player_x, player_y = player_position

            dir_x = player_x - enemy_x
            dir_y = player_y - enemy_y
            distance = math.hypot(dir_x, dir_y)
            if distance == 0:
                return None  # Avoid division by zero

            dir_x /= distance
            dir_y /= distance

            # Create a new DemonFire projectile and return it
            # DemonFire no longer needs on_player_body_entered here as main.py handles it
            new_projectile = DemonFire(
                start_x=enemy_x,
                start_y=enemy_y,
                dir_x=dir_x,
                dir_y=dir_y)
            # Reset last_shot_time to current_time for the next shot
            self.last_shot_time = current_time
            # Randomize the shoot_interval for the NEXT shot from this demon
            self.shoot_interval = random.randint(self.min_shoot_interval,
                                                 self.max_shoot_interval)
            return new_projectile

        return None  # No projectile fired this frame

    def _chase_player(self):
        player_pos_x, player_pos_y = self._get_player_position()
        enemy_dir_x = player_pos_x - self.x
        enemy_dir_y = player_pos_y - self.y
        distance = math.hypot(enemy_dir_x, enemy_dir_y)
        if distance == 0:
            return

        enemy_dir_x /= distance
        enemy_dir_y /= distance
        self.flip_dir = enemy_dir_x
        self.x += enemy_dir_x * self.enemy_speed
        self.y += enemy_dir_y * self.enemy_speed

    def is_bullet_hit(self):
        self.moving = False
        self.hurt = True
        self.hit_count += 1
        print(f"BigDemon hit! Current HP: {self.hit_count}")

    def get_enemy_collision_rect(self):
        return self.enemy_rect

    def get_center(self):
        return (self.x, self.y)

    def debug_enemy(self, screen, rect):
        pygame.draw.rect(screen, (255, 0, 0), rect, 2)
