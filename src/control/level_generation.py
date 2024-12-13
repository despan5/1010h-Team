"""
LevelGeneration Class

This script defines the `LevelGeneration` class for creating, rendering, and managing game levels.
It handles loading level data from a CSV file, generating tiles from a sprite sheet, 
and implementing collision detection with platforms, walls, and doors.
"""

import pygame
import csv
from constants import PROJECT_ROOT
import os

class LevelGeneration:
    def __init__(self, csv_path, tile_size, sprite_sheet_path):
        """
        Initialize the level generation system.
        Args:
            csv_path (str): path to the CSV file containing level data.
            tile_size (int): size of each tile in pixels.
            sprite_sheet_path (str): path to the sprite sheet image.
        """
        self.level_data = []  # stores level layout from CSV
        self.csv_path = csv_path
        self.tile_size = tile_size
        self.sprite_sheet = pygame.image.load(sprite_sheet_path)  # load sprite sheet
        self.sprites = {}  # dictionary to hold platform sprites
        self.platforms = []  # list to hold platform rectangles
        self.left_wall_tiles = []  # list for wall tiles on the left
        self.door_positions = []  # list for door positions

        self.load_sprites(15, 15)  # load sprite sheet tiles

        # load door sprites
        self.door_sprites = {
            5: self.load_and_scale_door_sprite(os.path.join(PROJECT_ROOT, "assets", "sprites", "Platforms", "top_right_door.jpg")),
            6: self.load_and_scale_door_sprite(os.path.join(PROJECT_ROOT, "assets", "sprites", "Platforms", "bottom_right_door.jpg")),
            7: self.load_and_scale_door_sprite(os.path.join(PROJECT_ROOT, "assets", "sprites", "Platforms", "bottom_left_door.jpg")),
            8: self.load_and_scale_door_sprite(os.path.join(PROJECT_ROOT, "assets", "sprites", "Platforms", "top_left_door.jpg")),
        }

    def load_level(self):
        """
        Load level data from a CSV file into a 2D list.
        """
        with open(self.csv_path, newline='') as file:
            reader = csv.reader(file)
            self.level_data = [list(map(int, row)) for row in reader]

    def load_sprites(self, sprite_width, sprite_height):
        """
        Extract sprites from the sprite sheet and scale them.
        Args:
            sprite_width (int): width of each sprite in the sheet.
            sprite_height (int): height of each sprite in the sheet.
        """
        columns = 3  # number of columns in the sprite sheet
        rows = 10    # number of rows in the sprite sheet
        
        for row in range(rows):
            for col in range(columns):
                # define sprite rectangle on the sprite sheet
                rect = pygame.Rect(col * sprite_width, row * sprite_height, sprite_width, sprite_height)
                sprite = self.sprite_sheet.subsurface(rect)  # extract sprite
                scaled_sprite = pygame.transform.scale(sprite, (self.tile_size + 10, self.tile_size + 10))
                # store scaled sprite and its dimensions
                self.sprites[(row, col)] = {
                    "image": scaled_sprite,
                    "width": scaled_sprite.get_width(),
                    "height": scaled_sprite.get_height()
                }

    def generate_level(self, screen, camera, player, show_debug_rects=False):
        """
        Generate and draw the level based on the level data.
        Args:
            screen (pygame.Surface): the display surface.
            camera (Camera): camera for scrolling.
            player (Player): the player object for collision detection.
            show_debug_rects (bool): enable debug mode to show platform bounds.
        """
        self.platforms.clear()  # reset platforms list
        
        # process left wall tiles
        for y, row in enumerate(self.level_data):
            if row[0] != -1:
                x, y = 0, y * self.tile_size
                wall_rect = pygame.Rect(x, y, self.tile_size, self.tile_size)
                self.left_wall_tiles.append(wall_rect)
        
        # draw platforms and doors
        for y, row in enumerate(self.level_data):
            for x, cell in enumerate(row):
                if 1 <= cell <= 30 and not (5 <= cell <= 8):  # platform cells
                    sprite_data = self.get_sprite_for_platform(cell)
                    if sprite_data:
                        sprite = sprite_data["image"]
                        platform_rect = pygame.Rect(x * self.tile_size, y * self.tile_size, 
                                                     sprite_data["width"], sprite_data["height"])
                        screen.blit(sprite, camera.apply(platform_rect))  # draw platform
                        self.platforms.append(platform_rect)  # add to platform list

                        if show_debug_rects:  # draw debug rectangle if enabled
                            pygame.draw.rect(screen, (255, 0, 0), camera.apply(platform_rect), 2)

                elif 5 <= cell <= 8:  # door cells
                    if cell in self.door_sprites:
                        sprite = self.door_sprites[cell]
                        door_rect = pygame.Rect(x * self.tile_size, y * self.tile_size, sprite.get_width(), sprite.get_height())
                        screen.blit(sprite, camera.apply(door_rect))  # draw door
                        self.door_positions.append((door_rect, cell))

        self.Check_Collision(player)  # check for collisions

    def load_and_scale_door_sprite(self, sprite_path):
        """
        Load and scale door sprites.
        Args:
            sprite_path (str): path to the door sprite.
        Returns:
            pygame.Surface: scaled door sprite.
        """
        sprite = pygame.image.load(sprite_path)
        return pygame.transform.scale(sprite, (self.tile_size, self.tile_size))

    def get_sprite_for_platform(self, cell):
        """
        Get the sprite corresponding to a platform cell value.
        Args:
            cell (int): cell value from the CSV.
        Returns:
            dict: sprite data with image and dimensions.
        """
        sprite_map = {
            1: (0, 0), 2: (0, 1), 3: (0, 2),
            4: (1, 0), 5: (1, 1), 6: (1, 2),
            7: (2, 0), 8: (2, 1), 9: (2, 2),
            # additional mappings...
        }
        return self.sprites.get(sprite_map.get(cell))

    def Check_Collision(self, player):
        """
        Check for player collisions with platforms, walls, and doors.
        Args:
            player (Player): the player object.
        """
        BUFFER = 5  # small buffer for collision adjustment
        player_on_platform = False

        # check for platform collisions
        for platform_rect in self.platforms:
            if (
                player.velocity_y > 0 and
                player.rect.bottom + player.velocity_y >= platform_rect.top - BUFFER and
                player.rect.bottom <= platform_rect.top + BUFFER and
                platform_rect.left < player.rect.right and
                player.rect.left < platform_rect.right
            ):
                player.rect.bottom = platform_rect.top  # snap player to platform
                player.velocity_y = 0  # stop vertical movement
                player.is_jumping = False  # reset jumping state
                player_on_platform = True
                break

        player.is_on_platform = player_on_platform  # update player status

        # check for wall collisions
        player.can_move_left = all(not player.rect.colliderect(wall_rect) for wall_rect in self.left_wall_tiles)

        # check for door collisions
        self.check_door_collision(player)

    def check_door_collision(self, player):
        """
        Check if the player collides with a door.
        Args:
            player (Player): the player object.
        """
        for door_rect, cell in self.door_positions:
            if player.rect.colliderect(door_rect):
                print(f"Player collided with door: {cell}")
                player.increase_level()  # trigger level change
                break
