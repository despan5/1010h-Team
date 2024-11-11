import pygame
import os
from control.health import Health
from constants import PROJECT_ROOT



class Player(pygame.sprite.Sprite):
    def __init__(self, SCREEN_HEIGHT):
        super().__init__()
        
        # load sprite sheets for different animations
        self.idle_sprites = self.load_sprites(os.path.join(PROJECT_ROOT, 'assets', 'sprites', 'female', 'doux', 'base', 'idle.png'), 24, 24)
        self.move_sprites = self.load_sprites(os.path.join(PROJECT_ROOT, 'assets', 'sprites', 'female', 'doux', 'base', 'move.png'), 24, 24)
        self.jump_sprites = self.load_sprites(os.path.join(PROJECT_ROOT, 'assets', 'sprites', 'female', 'doux', 'base', 'jump.png'), 24, 24)
        self.bite_sprites = self.load_sprites(os.path.join(PROJECT_ROOT, 'assets', 'sprites', 'female', 'doux', 'base', 'bite.png'), 24, 24)

        # set the initial states
        self.current_sprites = self.idle_sprites
        self.current_frame = 0
        self.image = self.current_sprites[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.center = (400, SCREEN_HEIGHT - 500)
        

        # variables for player movement and actions
        self.is_jumping = False
        self.is_on_platform = False
        self.velocity_y = 0
        self.gravity = 1.5
        self.jump_strength = -25
        self.is_moving = False
        self.is_facing_right = True
        self.movement_speed = 8

        # animation timing
        self.animation_delay = 10
        self.animation_counter = 0
        self.bite_animation_playing = False  # to track bite animation

        # health
        self.hp = Health()

    def load_sprites(self, sprite_sheet_path, frame_width, frame_height):
        # load the sprite sheet
        sprite_sheet = pygame.image.load(sprite_sheet_path)
        sheet_width, sheet_height = sprite_sheet.get_size()
        num_frames = sheet_width // frame_width  # calculate the number of frames based on the width of the sheet
        frames = []
        
        for i in range(num_frames):
            frame = sprite_sheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
            frame = pygame.transform.scale(frame, (100, 100))
            frames.append(frame)
        return frames

    def Update(self, lvlgen, enemy, camera, SCREEN_HEIGHT):
        pressed_keys = pygame.key.get_pressed()

        # reset movement and bite status at the start of update
        self.is_moving = False
        self.bite_animation_playing = False

        # movement logic for left (even while jumping)
        if pressed_keys[pygame.K_LEFT]:
            self.rect.move_ip(-self.movement_speed, 0)
            self.is_moving = True
            if self.is_facing_right:  # Only flip if the sprite is facing right
                self.is_facing_right = False

        # movement logic for right (even while jumping)
        elif pressed_keys[pygame.K_RIGHT]:
            self.rect.move_ip(self.movement_speed, 0)
            self.is_moving = True
            if not self.is_facing_right:  # Only flip if the sprite is facing left
                self.is_facing_right = True

        # jumping logic -- space key (trigger jump only when on the ground)
        if pressed_keys[pygame.K_SPACE] and self.is_on_platform and not self.is_jumping:
            self.Jump(SCREEN_HEIGHT)

        # Store the current sprite state for comparison later
        previous_sprites = self.current_sprites

        # determine which animation to use
        if self.is_jumping:  # if the player is in the air, always use jump animation
            self.current_sprites = self.jump_sprites

        elif pressed_keys[pygame.K_UP]:  # bite attack logic
            self.current_sprites = self.bite_sprites  # use bite animation
            self.bite_animation_playing = True

        # if no jumping and player is moving, use move animation
        elif self.is_moving:
            self.current_sprites = self.move_sprites

        # if no movement or jumping, play idle animation
        else:
            self.current_sprites = self.idle_sprites  # use idle animation

        # If the sprite list changed, reset the frame index
        if previous_sprites != self.current_sprites:
            self.current_frame = 0

        #print(f"Before Collision Check - Velocity Y: {self.velocity_y}, Is Jumping: {self.is_jumping}, Is On Platform: {self.is_on_platform}")

        # apply gravity and handle the jumping mechanism
        self.Apply_Gravity(SCREEN_HEIGHT)

        # handle sprite flipping based on direction
        self.image = self.current_sprites[self.current_frame]
        if not self.is_facing_right:
            self.image = pygame.transform.flip(self.image, True, False)

        # handle animation frame changes
        self.animation_counter += 1
        if self.animation_counter >= self.animation_delay:
            self.current_frame = (self.current_frame + 1) % len(self.current_sprites)
            self.animation_counter = 0

        # check collisions with platforms and enemies
    
        lvlgen.Check_Collision(self)

        #print(f"After Collision Check - Velocity Y: {self.velocity_y}, Is Jumping: {self.is_jumping}, Is On Platform: {self.is_on_platform}")

        if enemy:
            enemy.Check_Collision(self, SCREEN_HEIGHT)
        if camera:
            camera.update()

    def Jump(self, SCREEN_HEIGHT):
        if self.is_on_platform:  # Ensure the player can only jump when on a platform
            self.is_jumping = True
            self.velocity_y = self.jump_strength  # Set the initial jump strength

    def Apply_Gravity(self, SCREEN_HEIGHT):
        if not self.is_on_platform:
            self.velocity_y += self.gravity
            self.rect.y += self.velocity_y
            print(f"Gravity applied: velocity_y={self.velocity_y}, rect.bottom={self.rect.bottom}")
        else:
            print(f"No gravity: is_on_platform={self.is_on_platform}, velocity_y={self.velocity_y}")

    def Take_Damage(self):  # reduce player health
        self.hp.Take_Damage()

    

    def Draw(self, surface, camera, show_debug_rects=True):
       # If camera is not passed, or it's a lambda function for cutscenes, skip the camera logic
        if hasattr(camera, 'apply'):
            surface.blit(self.image, camera.apply(self.rect))
        else:
            surface.blit(self.image, camera.apply(self.rect))  # Just blit normally if no camera is used

        if show_debug_rects:
            pygame.draw.rect(surface, (0, 255, 0), camera.apply(self.rect), 2)

