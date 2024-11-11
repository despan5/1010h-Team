import pygame
import os
from constants import PROJECT_ROOT


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        base_path = os.path.dirname(__file__)  # Get the directory where the script is located
        sprite_sheet_path = os.path.join(PROJECT_ROOT, 'assets', 'sprites', 'male', 'cole', 'base', 'move.png')

        sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
        
        frame_width = 24
        frame_height = 24

        frame = sprite_sheet.subsurface(pygame.Rect(1 * frame_width, 0, frame_width, frame_height))
        frame = pygame.transform.scale(frame, (100, 100))
        frame = pygame.transform.flip(frame, True, False)
        self.image = frame

        self.rect = self.image.get_rect()
        self.rect = self.rect.inflate(-20, -10)
        self.rect.center = (1150, 465)

    def Draw(self, surface, camera, show_debug_rects = False):
        surface.blit(self.image, camera.apply(self.rect))

        if show_debug_rects:
            pygame.draw.rect(surface, (0, 255, 0), camera.apply(self.rect), 2)

    def Check_Collision(self, player, SCREEN_HEIGHT):
        if self.rect.colliderect(player.rect):
            player.rect.center = (160, SCREEN_HEIGHT - 300)

            player.hp.Take_Damage()
