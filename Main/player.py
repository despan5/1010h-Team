import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, screen_height, sprite_sheet_path):
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

        #initialization of all the elements needed to function as a playable character
        self.current_frame= 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.center = (160, screen_height - 300)

        self.is_jumping = False
        self.velocity_y = 0
        self.gravity = 1.5
        self.jump_strength = -22.5
        self.is_moving = False
        self.is_facing_right = True
        self.movement_speed = 6

        self.animation_delay = 5
        self.animation_counter = 0

    #Checks for updates in the players inputs/movements
    def Update(self, platforms, enemy, screen_height):
        pressed_keys = pygame.key.get_pressed()
        self.is_moving = False

        if self.rect.left > 0:
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
        self.Apply_Gravity(screen_height)

        if self.is_moving:
            self.animation_counter+= 1
            if self.animation_counter >= self.animation_delay:
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                self.image = self.frames[self.current_frame]
                self.animation_counter = 0

        for platform in platforms:
            platform.Check_Collision(self)

        enemy.Check_Collision(self, screen_height)

    def Flip_Sprites(self):
        for i in range(len(self.frames)):
            self.frames[i] = pygame.transform.flip(self.frames[i], True, False)
    def Jump(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_SPACE] and not self.is_jumping:
            self.velocity_y = self.jump_strength #gravity effect, increases velocity each time.
            self.is_jumping = True

    def Apply_Gravity(self, screen_height):
        if self.is_jumping:
            self.velocity_y += self.gravity
            self.rect.y += self.velocity_y


        if self.rect.y >= screen_height - 350:
            self.rect.y = screen_height - 350
            self.velocity_y = 0
            self.is_jumping = False

    def Draw(self, surface):
        surface.blit(self.image, self.rect)