import pygame
import math


class DemonFire:
    def __init__(self, get_enemy_center, get_player_collision, on_player_body_entered):
        self._get_enemy_center = get_enemy_center
        self._get_player_collision = get_player_collision
        self._on_player_body_entered = on_player_body_entered

        self.bullet_speed = 2
        self.bullets = []

        # Load bullet animation frames
        self.bullet_frames = self._sprite_loader(
            "assets/extras/demon_fire/fire", length=4, size=(52, 52))

        self.last_shot_time = 0
        self.shoot_interval = 5000  # milliseconds (5 seconds)

    def _sprite_loader(self, path, length=1, size=None):
        sprites = []
        for i in range(length):
            image = pygame.image.load(f"{path}_{i}.png").convert_alpha()
            if size:
                image = pygame.transform.scale(image, size)
            sprites.append(image)
        return sprites

    def update(self, screen):
        self._auto_fire()
        self._update_bullets(screen)

    def _auto_fire(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time >= self.shoot_interval:
            self._fire_bullet()
            self.last_shot_time = current_time

    def _fire_bullet(self):
        enemy_x, enemy_y = self._get_enemy_center()
        player_rect = self._get_player_collision()
        player_x, player_y = player_rect.center

        dir_x = player_x - enemy_x
        dir_y = player_y - enemy_y
        distance = math.hypot(dir_x, dir_y)
        if distance == 0:
            return
        dir_x /= distance
        dir_y /= distance

        self.bullets.append({
            "x": enemy_x,
            "y": enemy_y,
            "dir_x": dir_x,
            "dir_y": dir_y,
            "has_hit": False,
            "frame_index": 0,
            "frame_counter": 0
        })

    def _update_bullets(self, screen):
        player_rect = self._get_player_collision()

        for bullet in self.bullets[:]:
            if bullet["has_hit"]:
                self.bullets.remove(bullet)
                continue

            # Move bullet
            bullet["x"] += bullet["dir_x"] * self.bullet_speed
            bullet["y"] += bullet["dir_y"] * self.bullet_speed

            # Update animation frame
            bullet["frame_counter"] += 1
            if bullet["frame_counter"] >= 5:
                bullet["frame_counter"] = 0
                bullet["frame_index"] = (
                    bullet["frame_index"] + 1) % len(self.bullet_frames)

            # Calculate rotation angle
            angle = math.degrees(math.atan2(-bullet["dir_y"], bullet["dir_x"]))
            rotated_sprite = pygame.transform.rotate(
                self.bullet_frames[bullet["frame_index"]], angle)

            bullet_rect = rotated_sprite.get_rect(
                center=(int(bullet["x"]), int(bullet["y"])))
            screen.blit(rotated_sprite, bullet_rect.topleft)

            # Check collision with player
            if bullet_rect.colliderect(player_rect):
                bullet["has_hit"] = True
                self._on_player_body_entered(player_rect)

            # Remove if off-screen
            if (bullet["x"] < 0 or bullet["x"] > 1920 or
                    bullet["y"] < 0 or bullet["y"] > 1080):
                self.bullets.remove(bullet)
