import pygame
import os
from control.health import Health
from constants import PROJECT_ROOT
from ui.score_manager import ScoreManager



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
        self.rect = self.rect.inflate(-37.5, -10)  # Reduce width by 37.5 pixels and height by 25 pixels
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
        self.can_double_jump = False  # Start with double jump disabled
        self.can_move_left = True

        # animation timing
        self.animation_delay = 10
        self.animation_counter = 0
        self.bite_animation_playing = False  # to track bite animation

        # health
        self.hp = Health()

        self.score = 0  # Initialize score

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
        if pressed_keys[pygame.K_LEFT] and self.can_move_left:
            self.rect.move_ip(-self.movement_speed, 0)
            self.is_moving = True
            self.is_facing_right = False
        # movement logic for right (even while jumping)
        elif pressed_keys[pygame.K_RIGHT]:
            self.rect.move_ip(self.movement_speed, 0)
            self.is_moving = True
            if not self.is_facing_right:  # Only flip if the sprite is facing left
                self.is_facing_right = True

        # jumping logic -- space key (trigger jump only when on the ground)
        if pressed_keys[pygame.K_SPACE]:
            self.Jump()
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
        lvlgen.Check_Collision(self)
        
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
    
       

        #print(f"After Collision Check - Velocity Y: {self.velocity_y}, Is Jumping: {self.is_jumping}, Is On Platform: {self.is_on_platform}")

        if enemy:
            enemy.Check_Collision(self, SCREEN_HEIGHT)
        if camera:
            camera.update()

    def Jump(self):
        if self.is_on_platform:  # First jump
            self.is_jumping = True
            self.velocity_y = self.jump_strength
            self.can_double_jump = True
            self.is_on_platform = False

        elif self.can_double_jump:  # Double jump
            self.velocity_y = self.jump_strength
            self.can_double_jump = False



    def Apply_Gravity(self, SCREEN_HEIGHT):
        if not self.is_on_platform:
            self.velocity_y += self.gravity
            self.rect.y += self.velocity_y
        else:
            self.is_jumping = False
            self.can_double_jump = False  # Reset double jump on landing


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

    def increase_score(self, amount):
        self.score += amount

    def decrease_score(self, amount):
        self.score -= amount

    def get_score(self):
        return self.score
    
    def save_score(self, player_name):
        score_manager = ScoreManager()
        score_manager.add_score(player_name, self.score)

