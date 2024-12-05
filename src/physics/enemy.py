import pygame
import os
from constants import PROJECT_ROOT


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, end):
        super().__init__()

        # Load the move sprite sheet
        self.move_sprites = self.load_sprites(
            os.path.join(PROJECT_ROOT, 'assets', 'sprites', 'male', 'cole', 'base', 'move.png'),
            frame_width=24,
            frame_height=24
        )

        # Initialize animation state
        self.current_frame = 0
        self.image = self.move_sprites[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect = self.rect.inflate(-20, -10)
        self.rect.topleft = (x, y)

        # Enemy properties
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.path = [x, end]
        self.walkCount = 0
        self.vel = 1
        self.hp = 3  # Example health value

        # Animation timing
        self.animation_delay = 10
        self.animation_counter = 0
        self.is_facing_right = True

    def load_sprites(self, sprite_sheet_path, frame_width, frame_height):
        # Load the sprite sheet
        sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
        sheet_width, _ = sprite_sheet.get_size()
        num_frames = sheet_width // frame_width
        frames = []

        for i in range(num_frames):
            frame = sprite_sheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
            frame = pygame.transform.scale(frame, (100, 100))
            frames.append(frame)
        return frames

    def Draw(self, surface, camera, show_debug_rects=False):
        self.move()

        # Update sprite animation
        self.animation_counter += 1
        if self.animation_counter >= self.animation_delay:
            self.current_frame = (self.current_frame + 1) % len(self.move_sprites)
            self.animation_counter = 0

        # Flip sprite if facing left
        self.image = self.move_sprites[self.current_frame]
        if not self.is_facing_right:
            self.image = pygame.transform.flip(self.image, True, False)

        # Render the enemy
        surface.blit(self.image, camera.apply(self.rect))

        if show_debug_rects:
            pygame.draw.rect(surface, (255, 0, 0), camera.apply(self.rect), 2)

    def move(self):
        # Handle back-and-forth movement along the path
        if self.vel > 0:  # Moving right
            if self.rect.x + self.vel < self.path[1]:
                self.rect.x += self.vel
            else:
                self.vel = -self.vel
                self.is_facing_right = False
        else:  # Moving left
            if self.rect.x + self.vel > self.path[0]:
                self.rect.x += self.vel
            else:
                self.vel = -self.vel
                self.is_facing_right = True

    def Check_Collision(self, player, SCREEN_HEIGHT):
        if self.rect.colliderect(player.rect):
            player.rect.center = (160, SCREEN_HEIGHT - 300)
            player.Take_Damage()
            self.take_damage()

    def take_damage(self):
        self.hp -= 1
        if self.hp <= 0:
            self.kill()  # Remove the enemy from the game
