import pygame
import math


class DemonFire:
    def __init__(self, start_x, start_y, dir_x, dir_y):
        self.x = start_x
        self.y = start_y
        self.dir_x = dir_x
        self.dir_y = dir_y
        self.fire_speed = 3
        self.has_hit = False

        # Load bullet animation frames
        self.fire_sprite = self._sprite_loader(
            "assets/extras/demon_fire/fire", length=4, size=(52, 52))
        self.frame_index = 0
        self.frame_counter = 0

    def _sprite_loader(self, path, length=1, size=None):
        sprites = []
        for i in range(length):
            image = pygame.image.load(f"{path}_{i}.png").convert_alpha()
            if size:
                image = pygame.transform.scale(image, size)
            sprites.append(image)
        return sprites

    def update(self, screen):
        if self.has_hit:
            return
        self._update_fire(screen)

    def _update_fire(self, screen):
        # Move bullet
        self.x += self.dir_x * self.fire_speed
        self.y += self.dir_y * self.fire_speed

        # Update animation frame
        self.frame_counter += 1
        if self.frame_counter >= 5:  # Adjust frame rate as needed
            self.frame_counter = 0
            self.frame_index = (self.frame_index + 1) % len(self.fire_sprite)

        # Calculate rotation angle
        angle = math.degrees(math.atan2(-self.dir_y, self.dir_x))
        rotated_sprite = pygame.transform.rotate(self.fire_sprite[self.frame_index],
                                                 angle)
        fire_rect = rotated_sprite.get_rect(center=(int(self.x),
                                                    int(self.y)))
        screen.blit(rotated_sprite, fire_rect.topleft)
        self.debug_bullet(screen, fire_rect)  # For debugging collision box

    # Method to get its own collision rect for checks in main.py
    def get_collision_rect(self):
        # A simple rect for collision, assuming the sprite's current size is sufficient
        # Offset to center the collision rect on the bullet's x,y
        return pygame.Rect(0, 0, 52, 52).copy().move(self.x - 26, self.y - 26)

    def debug_bullet(self, screen, rect):
        # Yellow border for demon fire
        pygame.draw.rect(screen, (255, 255, 0), rect, 1)
