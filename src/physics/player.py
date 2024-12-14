"""
Player Class

This class defines the main player character, including its movements, animations, 
interactions with the game world, and score/health management.
"""

import pygame
import os
from control.health import Health
from constants import PROJECT_ROOT
from database import Database


class Player(pygame.sprite.Sprite):
    """
    Represents the player character with movement, animation, and interactions.
    """

    def __init__(self, SCREEN_HEIGHT):
        """
        Initialize the player with animations, physics attributes, and initial states.

        Args:
            SCREEN_HEIGHT (int): Height of the screen to position the player initially.
        """
        super().__init__()
        
        self.username = None  # username of the player, loaded from the database
        
        # load sprite sheets for animations
        self.idle_sprites = self.load_sprites(os.path.join(PROJECT_ROOT, 'assets', 'sprites', 'female', 'doux', 'base', 'idle.png'), 24, 24)
        self.move_sprites = self.load_sprites(os.path.join(PROJECT_ROOT, 'assets', 'sprites', 'female', 'doux', 'base', 'move.png'), 24, 24)
        self.jump_sprites = self.load_sprites(os.path.join(PROJECT_ROOT, 'assets', 'sprites', 'female', 'doux', 'base', 'jump.png'), 24, 24)
        self.bite_sprites = self.load_sprites(os.path.join(PROJECT_ROOT, 'assets', 'sprites', 'female', 'doux', 'base', 'bite.png'), 24, 24)

        # set the initial animation and position
        self.current_sprites = self.idle_sprites
        self.current_frame = 0
        self.image = self.current_sprites[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect = self.rect.inflate(-37.5, -10)  # shrink hitbox size for better collision detection
        self.rect.center = (400, SCREEN_HEIGHT - 500)
        self.current_level = 1
        
        # movement and action attributes
        self.is_jumping = False
        self.is_on_platform = False
        self.velocity_y = 0
        self.gravity = 1.5
        self.jump_strength = -25
        self.is_moving = False
        self.is_facing_right = True
        self.movement_speed = 8
        self.can_double_jump = False # start with double jump disabled
        self.can_move_left = True

        # animation control
        self.animation_delay = 10
        self.animation_counter = 0
        self.bite_animation_playing = False # to track bite animation
        self.screen_height = SCREEN_HEIGHT

        # player state
        self.hp = Health()  # health management
        self.score = 0     # initialize score

    def load_sprites(self, sprite_sheet_path, frame_width, frame_height):
        """
        Load sprites from a sprite sheet.

        Args:
            sprite_sheet_path (str): Path to the sprite sheet image.
            frame_width (int): Width of each frame in the sprite sheet.
            frame_height (int): Height of each frame in the sprite sheet.

        Returns:
            list[pygame.Surface]: List of frames extracted from the sprite sheet.
        """
        sprite_sheet = pygame.image.load(sprite_sheet_path)
        sheet_width, sheet_height = sprite_sheet.get_size()
        num_frames = sheet_width // frame_width  # calculate the number of frames based on the width of the sheet
        frames = []
        
        for i in range(num_frames):
            frame = sprite_sheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
            frame = pygame.transform.scale(frame, (100, 100)) #scale each frame
            frames.append(frame)
        return frames

    def Update(self, lvlgen, enemies, camera, SCREEN_HEIGHT):
        """
        Update the player's state, handle inputs, and interactions.

        Args:
            lvlgen (LevelGenerator): The level generator for collision checks.
            enemies (list[Enemy]): List of enemies in the level.
            camera (Camera): The camera object for scrolling.
            SCREEN_HEIGHT (int): Screen height for boundary checks.
        """
        pressed_keys = pygame.key.get_pressed()

        # reset movement and action states
        self.is_moving = False
        self.bite_animation_playing = False

        # movement: left and right
        if pressed_keys[pygame.K_LEFT] and self.can_move_left:
            self.rect.move_ip(-self.movement_speed, 0)
            self.is_moving = True
            self.is_facing_right = False
        # movement logic for right (even while jumping)
        elif pressed_keys[pygame.K_RIGHT]:
            self.rect.move_ip(self.movement_speed, 0)
            self.is_moving = True
            if not self.is_facing_right:  # only flip if the sprite is facing left
                self.is_facing_right = True

        # jump
        if pressed_keys[pygame.K_UP]:
            self.Jump()

        # store the current sprite state for comparison later
        previous_sprites = self.current_sprites

        # determine which animation to use
        if pressed_keys[pygame.K_UP]:  # bite attack logic
            self.current_sprites = self.bite_sprites  # use bite animation
            self.bite_animation_playing = True
        
        elif self.is_jumping:  # if the player is in the air, always use jump animation
            self.current_sprites = self.jump_sprites
        
        elif self.is_moving:  # if no jumping and player is moving, use move animation
            self.current_sprites = self.move_sprites
        
        else:  # if no movement or jumping, play idle animation
            self.current_sprites = self.idle_sprites

        # if the sprite list changed, reset the frame index
        if previous_sprites != self.current_sprites:
            self.current_frame = 0

        # gravity and collision
        lvlgen.Check_Collision(self)
        self.Apply_Gravity(SCREEN_HEIGHT)

        # handle animation frame updates
        self.animation_counter += 1
        if self.animation_counter >= self.animation_delay:
            self.current_frame = (self.current_frame + 1) % len(self.current_sprites)
            self.animation_counter = 0

        # handle enemy collisions
        for enemy in enemies:
            enemy.Check_Collision(self, SCREEN_HEIGHT)

        # update camera
        if camera:
            camera.update()

    def Jump(self):
        """
        Trigger jump or double jump actions based on current state.
        """
        if self.is_on_platform:  # first jump
            self.is_jumping = True
            self.velocity_y = self.jump_strength
            self.can_double_jump = True
            self.is_on_platform = False

        elif self.can_double_jump:  # double jump
            self.velocity_y = self.jump_strength
            self.can_double_jump = False

    def Apply_Gravity(self, SCREEN_HEIGHT):
        """
        Apply gravity to the player and update its vertical position.

        Args:
            SCREEN_HEIGHT (int): Height of the screen to prevent falling off.
        """
        if not self.is_on_platform:
            self.velocity_y += self.gravity
            self.rect.y += self.velocity_y
        else:
            self.is_jumping = False
            self.can_double_jump = False

    def Take_Damage(self):
        """
        Reduce the player's health.
        """
        self.hp.Take_Damage()

    def Draw(self, surface, camera, show_debug_rects=False):
        """
        Draw the player on the screen.

        Args:
            surface (pygame.Surface): The surface to draw on.
            camera (Camera): The camera object for scrolling.
            show_debug_rects (bool): If True, draw the player's collision box for debugging.
        """
        if hasattr(camera, 'apply'):
            surface.blit(self.image, camera.apply(self.rect))
        else:
            surface.blit(self.image, self.rect)

        if show_debug_rects:
            pygame.draw.rect(surface, (0, 255, 0), camera.apply(self.rect), 2)

    # score management
    def increase_score(self, amount):
        self.score += amount

    def decrease_score(self, amount):
        self.score -= amount

    def get_score(self):
        return self.score

    def update_score(self, username, score):
        Database().add_score(username, score)

    def find_score(self, username):
        self.score = Database().get_score(username)
        if self.score is None:
            self.score = 0
        return self.score

    # level progression
    def increase_level(self):
        self.current_level += 1
        self.rect.center = (160, self.screen_height - 300)