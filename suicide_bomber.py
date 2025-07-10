import pygame
import math


class Suicide_Bomber:
    def __init__(self, x, y, get_player_position, on_player_body_entered):
        self.x = x
        self.y = y
        self._on_player_body_entered = on_player_body_entered
        self._get_player_position = get_player_position
        self.flip_dir = 0
        self.enemy_speed = 1
        self.enemy_size = (176, 198)
        self.enemy_walk = self._sprite_loader(path="assets/enemy/suicide_bomber/walk/walk",
                                              length=4,
                                              size=self.enemy_size)
        self.enemy_hurt = self._sprite_loader(path="assets/enemy/suicide_bomber/hurt/hurt_0.png",
                                              size=self.enemy_size)
        self.enemy_death = self._sprite_loader(path="assets/death/death",
                                               length=5,
                                               size=(128, 128))
        self.enemy_boom = self._sprite_loader(path="assets/enemy/suicide_bomber/boom/boom",
                                              length=4,
                                              size=(300, 300))
        self.moving = True
        self.death = False
        self.hurt = False
        self.death_animation_done = False
        self.animation_count = 0
        self.frames_per_image = 5
        self.hit_count = 0
        # Initial rect for collision
        self.enemy_rect = None
        self.distance = None

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
                self._enemy_hit_anim(screen, self.enemy_hurt)

        if self.hit_count >= 3 and not self.death_animation_done:
            self._enemy_death_anim(screen, self.enemy_death)

        if self.distance <= 400 and not self.death_animation_done:
            self._enemy_blast_anim(screen, self.enemy_boom)

        self._on_player_body_entered(self.enemy_rect, True)

    def _blit_enemy_anim(self, screen, sprite_list, blast=False):
        sprite_len = len(sprite_list)
        self._animation_frame_counter(sprite_len)
        frame_index = self.animation_count // self.frames_per_image
        current_sprite = self._flip_sprite(
            sprite_list[frame_index], self.flip_dir)
        rect = current_sprite.get_rect(center=(self.x, self.y))

        if blast:
            self.enemy_rect = rect.copy().inflate(600, 600)  # Bigger collision for blast
        else:
            self.enemy_rect = rect  # Normal collision for enemy

        screen.blit(current_sprite, rect)
        self.debug_enemy(screen, self.enemy_rect)

    def _flip_sprite(self, sprite, direction):
        fliped = pygame.transform.flip(sprite,
                                       True, False) if direction < 0 else sprite
        return fliped

    def _enemy_walk_anim(self, screen, sprite_list):
        self._blit_enemy_anim(screen, sprite_list)

    def _enemy_death_anim(self, screen, sprite_list):
        print("enemy death")
        self._blit_enemy_anim(screen, sprite_list)
        self.death = True
        self.moving = False
        self.hurt = False
        self._check_death_animation_done(sprite_list)

    def _enemy_hit_anim(self, screen, sprite):
        print('hurt')
        self.enemy_rect = sprite.get_rect(center=(self.x, self.y))
        screen.blit(sprite, self.enemy_rect)
        self.debug_enemy(screen, self.enemy_rect)
        self.moving = True
        self.hurt = False

    def _enemy_blast_anim(self, screen, sprite_list):
        print(f"distance: {self.distance}", ", Blast!!!!")
        self.frames_per_image = 10
        self._blit_enemy_anim(screen, sprite_list, blast=True)
        self._check_death_animation_done(sprite_list)
        self.death = True

    def _check_death_animation_done(self, sprite_list):
        frame_index = self.animation_count // self.frames_per_image
        if frame_index >= len(sprite_list) - 1:
            print(self.death_animation_done, "death animation done")
            self.death_animation_done = True

    def _chase_player(self):
        player_pos_x, player_pos_y = self._get_player_position()
        enemy_dir_x = player_pos_x - self.x
        enemy_dir_y = player_pos_y - self.y
        self.distance = math.hypot(enemy_dir_x, enemy_dir_y)
        if self.distance == 0:
            return

        enemy_dir_x /= self.distance
        enemy_dir_y /= self.distance
        self.flip_dir = enemy_dir_x
        self.x += enemy_dir_x * self.enemy_speed
        self.y += enemy_dir_y * self.enemy_speed

    def is_bullet_hit(self, hit):
        self.moving = False
        self.hurt = hit
        self.hit_count += 1
        print("count: ", self.hit_count)
        print("Confirm Hit: ", hit)

    def get_enemy_collision_rect(self):
        return self.enemy_rect

    def debug_enemy(self, screen, rect):
        pygame.draw.rect(screen, (255, 0, 0), rect, 2)
