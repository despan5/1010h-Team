import pygame
import sys
import random
from pygame.locals import *
import os

pygame.init()

FPS = 60
FramePerSec = pygame.time.Clock()

# Predefined some colors
WHITE = (255, 255, 255)

# Screen information
info = pygame.display.Info()
SCREEN_WIDTH = info.current_w
SCREEN_HEIGHT = info.current_h

DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")

base_path = os.path.dirname(__file__)  # Get the directory where the script is located
bg_image_path = os.path.join(base_path, '..', 'Sprites', 'game_background.jpg')  # Construct the full path

bg_original = pygame.image.load(bg_image_path)
bg = pygame.transform.scale(bg_original, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Camera class to handle scrolling
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

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        sprite_sheet_path = os.path.join(base_path, '..', 'Sprites', 'male', 'cole', 'base', 'move.png')

        sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
        
        frame_width = 24
        frame_height = 24

        frame = sprite_sheet.subsurface(pygame.Rect(1 * frame_width, 0, frame_width, frame_height))
        frame = pygame.transform.scale(frame, (100, 100))
        frame = pygame.transform.flip(frame, True, False)
        self.image = frame

        self.rect = self.image.get_rect()
        self.rect.center = (1150, 465)

    def Draw(self, surface, camera):
        surface.blit(self.image, camera.apply(self.rect))

    def Check_Collision(self, player):
        if self.rect.colliderect(player.rect):
            player.rect.center = (160, SCREEN_HEIGHT - 300)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        sprite_sheet_path = os.path.join(base_path, '..', 'Sprites', 'female', 'doux', 'base', 'move.png')

        sprite_sheet = pygame.image.load(sprite_sheet_path)
        frame_width = 24
        frame_height = 24
        num_frames = 5

        self.frames = []
        for i in range(num_frames):
            frame = sprite_sheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
            frame = pygame.transform.scale(frame, (100, 100))
            self.frames.append(frame)

        self.current_frame= 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.center = (160, SCREEN_HEIGHT - 300)
        self.is_jumping = False
        self.velocity_y = 0
        self.gravity = 1.5
        self.jump_strength = -22.5
        self.is_moving = False
        self.is_facing_right = True
        self.movement_speed = 6

        self.animation_delay = 5
        self.animation_counter = 0

    def Update(self, platforms, enemy, camera):
        pressed_keys = pygame.key.get_pressed()
        self.is_moving = False

        if pressed_keys[pygame.K_LEFT]:
            self.rect.move_ip(-self.movement_speed, 0)
            self.is_moving = True
            if self.is_facing_right:
                self.Flip_Sprites()
            self.is_facing_right = False

        if pressed_keys[pygame.K_RIGHT]:
            self.rect.move_ip(self.movement_speed, 0)
            self.is_moving = True
            if not self.is_facing_right:
                self.Flip_Sprites()
            self.is_facing_right = True

        self.Jump()
        self.Apply_Gravity()

        if self.is_moving:
            self.animation_counter += 1
            if self.animation_counter >= self.animation_delay:
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                self.image = self.frames[self.current_frame]
                self.animation_counter = 0

        for platform in platforms:
            platform.Check_Collision(self)

        enemy.Check_Collision(self)
        camera.update()  # Update camera position based on movement

    def Flip_Sprites(self):
        for i in range(len(self.frames)):
            self.frames[i] = pygame.transform.flip(self.frames[i], True, False)

    def Jump(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_SPACE] and not self.is_jumping:
            self.velocity_y = self.jump_strength
            self.is_jumping = True

    def Apply_Gravity(self):
        if self.is_jumping:
            self.velocity_y += self.gravity
            self.rect.y += self.velocity_y

        if self.rect.y >= SCREEN_HEIGHT - 350:
            self.rect.y = SCREEN_HEIGHT - 350
            self.velocity_y = 0
            self.is_jumping = False

    def Draw(self, surface, camera):
        surface.blit(self.image, camera.apply(self.rect))

class Platform:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def Draw(self, surface, camera):
        pygame.draw.rect(surface, (0, 255, 0), camera.apply(self.rect))

    def Check_Collision(self, player):
        if player.velocity_y > 0 and player.rect.bottom <= self.rect.top and \
            player.rect.bottom + player.velocity_y >= self.rect.top and \
            self.rect.left < player.rect.centerx < self.rect.right:
            player.rect.bottom = self.rect.top
            player.velocity_y = 0
            player.is_jumping = False
        else:
            if not (self.rect.left < player.rect.centerx < self.rect.right) and player.rect.bottom == self.rect.top:
                player.is_jumping = True

# Platform generation
def generate_platforms(platforms, camera):
    last_platform = platforms[-1]
    if last_platform.rect.right < SCREEN_WIDTH - camera.offset_x:
        new_platform = Platform(last_platform.rect.right + random.randint(100, 300), random.randint(300, 700), 200, 20)
        platforms.append(new_platform)

def remove_offscreen_platforms(platforms, camera):
    platforms[:] = [platform for platform in platforms if platform.rect.right > -camera.offset_x]

def main():
    P1 = Player()
    E1 = Enemy()
    platforms = [
        Platform(400, 700, 200, 20),
        Platform(700, 600, 200, 20),
        Platform(1000, 500, 200, 20),
    ]
    camera = Camera(P1, SCREEN_WIDTH)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return None
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        P1.Update(platforms, E1, camera)
        remove_offscreen_platforms(platforms, camera)
        generate_platforms(platforms, camera)

        # **Fix background scrolling logic**
        DISPLAYSURF.blit(bg, (camera.offset_x % SCREEN_WIDTH, 0))
        if camera.offset_x % SCREEN_WIDTH != 0:
            DISPLAYSURF.blit(bg, (camera.offset_x % SCREEN_WIDTH - SCREEN_WIDTH, 0))

        for platform in platforms:
            platform.Draw(DISPLAYSURF, camera)

        P1.Draw(DISPLAYSURF, camera)
        E1.Draw(DISPLAYSURF, camera)

        pygame.display.update()
        FramePerSec.tick(FPS)

if __name__ == '__main__':
    main()
