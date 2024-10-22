import pygame
class Camera:
    def __init__(self, player, screen_width):
        self.player = player
        self.offset_x = 0
        self.screen_width = screen_width

    def update(self):
        # Center the camera on the player’s x position
        self.offset_x = -(self.player.rect.centerx - self.screen_width // 2)

    def apply(self, obj_rect):
        # Apply the offset to objects' rect
        return obj_rect.move(self.offset_x, 0)
