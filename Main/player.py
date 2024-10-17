import pygame
import os

class Player(pygame.sprite.Sprite):
    def __init__(self, SCREEN_HEIGHT):
        super().__init__()
        base_path = os.path.dirname(__file__) # Get the directory where the script is located

        # load sprite sheets for different animations
        self.idle_sprites = self.load_sprites(os.path.join(base_path, '..', 'Sprites', 'female', 'doux', 'base', 'idle.png'), 5, 24, 24)
        self.move_sprites = self.load_sprites(os.path.join(base_path, '..', 'Sprites', 'female', 'doux', 'base', 'move.png'), 5, 24, 24)
        self.jump_sprites = self.load_sprites(os.path.join(base_path, '..', 'Sprites', 'female', 'doux', 'base', 'jump.png'), 1, 24, 24)  # Only 1 frame for jump
        self.bite_sprites = self.load_sprites(os.path.join(base_path, '..', 'Sprites', 'female', 'doux', 'base', 'bite.png'), 3, 24, 24)  # 3 frames for bite

        # set the initial states
        self.current_sprites = self.idle_sprites
        self.current_frame = 0
        self.image = self.current_sprites[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.center = (160, SCREEN_HEIGHT - 300)

        # variables for player movement and actions
        self.is_jumping = False
        self.velocity_y = 0
        self.gravity = 1.5
        self.jump_strength = -22.5
        self.is_moving = False
        self.is_facing_right = True
        self.movement_speed = 6

        # animation timing
        self.animation_delay = 5
        self.animation_counter = 0
        self.bite_animation_playing = False  # to track bite animation

    def load_sprites(self, sprite_sheet_path, num_frames, frame_width, frame_height):
        # load the sprite sheet and split it into individual frames
        sprite_sheet = pygame.image.load(sprite_sheet_path)
        frames = []
        for i in range(num_frames):
            frame = sprite_sheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
            frame = pygame.transform.scale(frame, (100, 100))
            frames.append(frame)
        return frames

    def Update(self, platforms, enemy, camera, SCREEN_HEIGHT):
        pressed_keys = pygame.key.get_pressed()

        # reset movement and bite status at the start of update
        self.is_moving = False
        self.bite_animation_playing = False

        if pressed_keys[pygame.K_LEFT]: # movement logic
            self.rect.move_ip(-self.movement_speed, 0)
            self.is_moving = True
            if self.is_facing_right:
                self.Flip_Sprites()
            self.is_facing_right = False
            self.current_sprites = self.move_sprites  # use move animation

        if pressed_keys[pygame.K_RIGHT]: # movement logic
            self.rect.move_ip(self.movement_speed, 0)
            self.is_moving = True
            if not self.is_facing_right:
                self.Flip_Sprites()
            self.is_facing_right = True
            self.current_sprites = self.move_sprites  # use move animation

        # jumping logic -- space key
        if pressed_keys[pygame.K_SPACE] and not self.is_jumping:
            self.velocity_y = self.jump_strength
            self.is_jumping = True
            self.current_sprites = self.jump_sprites  # use jump animation

        if pressed_keys[pygame.K_UP]: # bite attack logic when up arrow is pressed
            self.current_sprites = self.bite_sprites  # use bite animation
            self.bite_animation_playing = True

        # if no movement or jumping, play idle animation
        if not self.is_moving and not self.is_jumping and not self.bite_animation_playing:
            self.current_sprites = self.idle_sprites  # use idle animation

        self.Jump()
        self.Apply_Gravity(SCREEN_HEIGHT)

        # handle animation frame changes
        self.animation_counter += 1
        if self.animation_counter >= self.animation_delay:
            self.current_frame = (self.current_frame + 1) % len(self.current_sprites)
            self.image = self.current_sprites[self.current_frame]
            self.animation_counter = 0

        # check collisions with platforms and enemies
        for platform in platforms:
            platform.Check_Collision(self)

        enemy.Check_Collision(self, SCREEN_HEIGHT)
        camera.update()

    def Flip_Sprites(self): # flip sprites for different directions
        for i in range(len(self.current_sprites)):
            self.current_sprites[i] = pygame.transform.flip(self.current_sprites[i], True, False)

    def Jump(self):
        if self.is_jumping: # apply gravity to jumping behavior
            self.velocity_y += self.gravity
            self.rect.y += self.velocity_y

        if self.rect.y >= SCREEN_HEIGHT - 350:# stop jumping when player hits the ground
            self.rect.y = SCREEN_HEIGHT - 350
            self.velocity_y = 0
            self.is_jumping = False

    def Apply_Gravity(self, SCREEN_HEIGHT):
        if self.is_jumping: # apply gravity to pull the player down when in the air
            self.velocity_y += self.gravity
            self.rect.y += self.velocity_y

        if self.rect.y >= SCREEN_HEIGHT - 350: # stop applying gravity when player reaches the ground
            self.rect.y = SCREEN_HEIGHT - 350
            self.velocity_y = 0
            self.is_jumping = False

    def Draw(self, surface, camera):
        surface.blit(self.image, camera.apply(self.rect))
