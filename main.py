import os
import pygame
from os import listdir
from os.path import isfile, join

pygame.init()

# Game window settings
pygame.display.set_caption("Platformer")
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60

# Global constants
BG_COLOR = (255, 255, 255)  # White background
GROUND_COLOR = (0, 0, 0)  # Black ground
PLAYER_VEL = 5
GRAVITY = 1

# Helper functions
def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]

def load_sprite_sheets(base_dir, char_dir, action_dir, width, height, direction=False):
    path = join(base_dir, char_dir, action_dir)
    images = [f for f in listdir(path) if isfile(join(path, f))]

    all_sprites = {}
    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()

        sprites = []
        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)
            sprites.append(pygame.transform.scale2x(surface))

        if direction:
            all_sprites[image.replace(".png", "") + "_right"] = sprites
            all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)
        else:
            all_sprites[image.replace(".png", "")] = sprites

    return all_sprites

# Player class
class Player(pygame.sprite.Sprite):
    SPRITES = load_sprite_sheets("assets", "male", "olaf/base", 24, 24, True)  # Use a cropped 32x32 size
    
    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.direction = "right"
        self.animation_count = 0
        self.fall_count = 0
        self.jumping = False

    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def jump(self):
        if not self.jumping:
            self.jumping = True
            self.y_vel = -15  # Jump height

    def apply_gravity(self):
        self.y_vel += GRAVITY
        if self.y_vel > 10:  # Max fall speed
            self.y_vel = 10

    def move(self):
        self.rect.x += self.x_vel
        self.rect.y += self.y_vel

    def handle_screen_boundaries(self):
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.jumping = False
            self.y_vel = 0  # Reset velocity when hitting the ground

    def handle_vertical_collision(self, platforms):
        for platform in platforms:
            if pygame.sprite.collide_rect(self, platform):
                if self.y_vel > 0:  # Falling
                    self.rect.bottom = platform.rect.top
                    self.jumping = False
                    self.y_vel = 0
                elif self.y_vel < 0:  # Jumping and hitting the ceiling
                    self.rect.top = platform.rect.bottom
                    self.y_vel = 0

    def update(self, platforms):
        self.apply_gravity()
        self.move()
        self.handle_vertical_collision(platforms)
        self.handle_screen_boundaries()

    def draw(self, window):
        sprite = self.SPRITES["move_right"][0] if self.direction == "right" else self.SPRITES["move_left"][0]
        window.blit(sprite, (self.rect.x, self.rect.y))

# Platform class
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, window):
        pygame.draw.rect(window, GROUND_COLOR, self.rect)  # Black platforms

def draw(window, player, platforms):
    window.fill(BG_COLOR)
    player.draw(window)
    for platform in platforms:
        platform.draw(window)
    pygame.display.update()

def handle_move(player):
    keys = pygame.key.get_pressed()
    player.x_vel = 0

    if keys[pygame.K_LEFT]:
        player.move_left(PLAYER_VEL)
    if keys[pygame.K_RIGHT]:
        player.move_right(PLAYER_VEL)
    if keys[pygame.K_UP] and not player.jumping:
        player.jump()

def main(window):
    clock = pygame.time.Clock()
    player = Player(100, 500, 50, 50)
    
    platforms = [
        Platform(0, HEIGHT - 50, WIDTH, 50),  # Ground
        Platform(100, 450, 150, 10),          # Platform 1
        Platform(300, 350, 150, 10),          # Platform 2
        Platform(500, 250, 150, 10),          # Platform 3
        Platform(650, 150, 150, 10)           # Platform 4
    ]

    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        handle_move(player)
        player.update(platforms)
        draw(window, player, platforms)

    pygame.quit()

if __name__ == "__main__":
    main(window)
