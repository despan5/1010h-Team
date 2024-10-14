import pygame

class Camera:
    def __init__(self, player, screen_width):
        self.player = player
        self.offset_x = 0
        self.screen_width = screen_width
        self.scroll_speed = 6

    def update(self):
        # Only scroll if the player is moving and passes the center of the screen
        if self.player.is_moving:
            if self.player.rect.centerx > self.screen_width // 2 and self.player.is_facing_right:
                self.offset_x -= self.scroll_speed
            elif self.player.rect.centerx < self.screen_width // 2 and not self.player.is_facing_right:
                self.offset_x += self.scroll_speed

    def apply(self, obj_rect):
        return obj_rect.move(self.offset_x, 0)
