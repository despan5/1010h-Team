import pygame
import sys
import random

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

bg_original = pygame.image.load('C:/Users/thoma/Documents/GitHub/1010h-Team/Sprites/game_background.jpg')
bg = pygame.transform.scale(bg_original, (SCREEN_WIDTH, SCREEN_HEIGHT))

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('C:/Users/thoma/Documents/GitHub/1010h-Team/Sprites/female/doux/base/move.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)


    def Move(self):
        self.rect.move_ip(0, 5)
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.top = 0
            self.rect.center = (random.randint(30, 370), 0)

    def Draw(self, surface):
        surface.blit(self.image, self.rect)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        sprite_sheet = pygame.image.load('C:/Users/thoma/Documents/GitHub/1010h-Team/Sprites/female/doux/base/move.png')

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
        self.gravity = 1
        self.jump_strength = -15
        self.is_moving = False
        self.is_facing_right = True

        self.animation_delay = 5
        self.animation_counter = 0

    def Update(self):
        pressed_keys = pygame.key.get_pressed()
        self.is_moving = False

        if self.rect.left > 0:
            if pressed_keys[pygame.K_LEFT]:
                self.rect.move_ip(-5, 0)
                self.is_moving = True
                if self.is_facing_right:
                    self.Flip_Sprites()
                self.is_facing_right = False

        if pressed_keys[pygame.K_RIGHT]:
            self.rect.move_ip(5, 0)
            self.is_moving = True
            if not self.is_facing_right:
                self.Flip_Sprites()
            self.is_facing_right = True

        self.Jump()
        self.Apply_Gravity()

        if self.is_moving:
            self.animation_counter+= 1
            if self.animation_counter >= self.animation_delay:
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                self.image = self.frames[self.current_frame]
                self.animation_counter = 0

    def Flip_Sprites(self):
        for i in range(len(self.frames)):
            self.frames[i] = pygame.transform.flip(self.frames[i], True, False)
    def Jump(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_SPACE] and not self.is_jumping:
            self.velocity_y = self.jump_strength #gravity effect, increases velocity each time.
            self.is_jumping = True

    def Apply_Gravity(self):
        if self.is_jumping:
            self.velocity_y += self.gravity
            self.rect.y += self.velocity_y


        if self.rect.y >= SCREEN_HEIGHT - 350:
            self.rect.y = SCREEN_HEIGHT - 350
            self.velocity_y = 0
            self.is_jumping = False

    def Draw(self, surface):
        surface.blit(self.image, self.rect)


P1 = Player()
#E1 = Enemy()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    P1.Update()
    #E1.Move()

    DISPLAYSURF.blit(bg, (0, 0))
    P1.Draw(DISPLAYSURF)
    #E1.Draw(DISPLAYSURF)

    pygame.display.update()
    FramePerSec.tick(FPS)