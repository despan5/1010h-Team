import pygame
import csv

class LevelGeneration:
    def __init__(self, csv_path, tile_size, sprite_sheet_path):
        self.level_data = []
        self.csv_path = csv_path
        self.tile_size = tile_size
        self.sprite_sheet = pygame.image.load(sprite_sheet_path)
        self.sprites = {}  # Dictionary to hold the different platform sprites
        self.platforms = []  # List to hold the platform rectangles
        self.left_wall_tiles = []  # Store wall tiles on the left side of the screen

        self.load_sprites(15, 15)

    def load_level(self):
        # Load the level data from the CSV file
        with open(self.csv_path, newline='') as file:
            reader = csv.reader(file)
            self.level_data = [list(map(int, row)) for row in reader]

    def load_sprites(self, sprite_width, sprite_height):
        """
        This function loads the sprites from the sprite sheet.
        Assuming the sprite sheet contains tiles arranged in a grid.
        """
        columns = 3  # Number of columns in your sprite sheet (48/16)
        rows = 10    # Number of rows in your sprite sheet (158/16)
        
        for row in range(rows):
            for col in range(columns):
                # Define the area of the sprite on the sprite sheet
                rect = pygame.Rect(col * sprite_width, row * sprite_height, sprite_width, sprite_height)
                # Extract the sprite using subsurface
                sprite = self.sprite_sheet.subsurface(rect)
                
                # Scale the sprite based on the tile size
                scaled_sprite = pygame.transform.scale(sprite, (self.tile_size + 10, self.tile_size + 10))
                
                # Store the scaled sprite along with its width and height
                self.sprites[(row, col)] = {
                    "image": scaled_sprite,
                    "width": scaled_sprite.get_width(),
                    "height": scaled_sprite.get_height()
                }

    def generate_level(self, screen, camera, player, show_debug_rects=False):
        # Clear the platform list at the start of each frame
        self.platforms.clear()

        # Iterate through the level data and place the correct platform sprite based on the number

        for y, row in enumerate(self.level_data):
            if row[0] != -1:  # Check if the first column cell is a wall tile
                x, y = 0, y * self.tile_size  # Position based on tile size
                wall_rect = pygame.Rect(x, y, self.tile_size, self.tile_size)
                self.left_wall_tiles.append(wall_rect)
                
        for y, row in enumerate(self.level_data):
            for x, cell in enumerate(row):
                if 1 <= cell <= 30:  # Platform cells
                    # Get the corresponding sprite based on the cell value
                    sprite_data = self.get_sprite_for_platform(cell)

                    if sprite_data is not None:
                        sprite = sprite_data["image"]
                        sprite_width = sprite_data["width"]
                        sprite_height = sprite_data["height"]

                        # Create the platform rect based on scaled sprite dimensions
                        platform_rect = pygame.Rect(
                            x * self.tile_size, y * self.tile_size, sprite_width, sprite_height
                        )
                        platform_rect_camera = camera.apply(platform_rect)
                        screen.blit(sprite, platform_rect_camera)

                        # Add the platform rect to the list for collision checks
                        self.platforms.append(platform_rect)

                        # Draw debug rectangles around the platforms if enabled
                        if show_debug_rects:
                            pygame.draw.rect(screen, (255, 0, 0), camera.apply(platform_rect), 2)  # Red color, 2px border

        # Check for collision with the player
        self.Check_Collision(player)

    def get_sprite_for_platform(self, cell):
        """
        Map the CSV cell value to a platform sprite based on its index in the sprite sheet.
        """
        try:
            sprite_map = {
                1: (0, 0), 2: (0, 1), 3: (0, 2),
                4: (1, 0), 5: (1, 1), 6: (1, 2),
                7: (2, 0), 8: (2, 1), 9: (2, 2),
                10: (3, 0), 11: (3, 1), 12: (4, 0),
                13: (4, 1), 14: (4, 2), 15: (5, 0),
                16: (5, 1), 17: (5, 2), 18: (6, 0),
                19: (6, 1), 20: (6, 2), 21: (7, 0),
                22: (7, 1), 23: (7, 2), 24: (8, 0),
                25: (8, 1), 26: (8, 2), 27: (9, 0),
                28: (9, 1), 29: (9, 2), 30: (10, 0)
            }
            if cell in sprite_map:
                return self.sprites[sprite_map[cell]]
        except KeyError:
            print(f"Error: No sprite found for cell {cell}")
        return None
    
    def Check_Collision(self, player):
        player_on_platform = False
        BUFFER = 5  # Small buffer to prevent micro-bouncing

        for platform_rect in self.platforms:
            # Check if the player is falling and is within the range to land on the platform
            if (
                player.velocity_y > 0 and
                player.rect.bottom + player.velocity_y >= platform_rect.top - BUFFER and
                player.rect.bottom <= platform_rect.top + BUFFER and
                platform_rect.left < player.rect.right and
                player.rect.left < platform_rect.right
            ):
                # Snap player to the platform's top
                player.rect.bottom = platform_rect.top
                player.velocity_y = 0  # Stop vertical movement when landing
                player.is_jumping = False  # Reset jumping state
                player_on_platform = True
                break  # Exit loop after finding a platform collision

        # Set `is_on_platform` based on whether the player is supported
        player.is_on_platform = player_on_platform

        for wall_rect in self.left_wall_tiles:
            if player.rect.colliderect(wall_rect):
                player.can_move_left = False
                break
        else:
            player.can_move_left = True  # Allow left movement if not colliding with the wall


    # def Check_Collision(self, player):
    #     # Variable to track if the player is standing on any platform
    #     player_on_platform = False
    #     collided_platform_rect = None
    #     BUFFER = 10  # Small buffer for collision check
    #     OFFSET = 10  # Offset to prevent player from falling off the platform

    #     for platform_rect in self.platforms:
    #         # Check if the player is falling (velocity > 0) and is close enough to the platform's top to land
    #         if player.velocity_y > 0:  # Ensure only downward movement triggers landing logic
    #             if (
    #                 player.rect.bottom + player.velocity_y >= platform_rect.top - BUFFER and
    #                 player.rect.bottom <= platform_rect.bottom - BUFFER and
    #                 platform_rect.left < player.rect.right and
    #                 player.rect.left < platform_rect.right
    #             ):
                    
    #                 #print(f"Landing detected at Platform Top: {platform_rect.top}")

    #                 # Player has landed on the platform
    #                 player.rect.bottom = platform_rect.top  # Snap player's bottom to the platform's top
    #                 player.velocity_y = 0  # Stop vertical movement
    #                 player.is_jumping = False  # Player is not jumping
    #                 player_on_platform = True  # Mark the player as on a platform
    #                 player.is_on_platform = True  # Mark the player as on a platform
    #                 collided_platform_rect = platform_rect
    #                 break  # Exit loop once a collision is found

    #     # Update `is_on_platform` based on collision checks
    #     if player_on_platform:
    #         player.is_on_platform = True
    #         if player.rect.bottom != collided_platform_rect.top + OFFSET:  # Only adjust if not already on the platform
    #             player.rect.bottom = collided_platform_rect.top + OFFSET  # Ensure player stays on the platform
    #             player.velocity_y = 0  # Stop vertical movement
    #             player.is_jumping = False
    #     else:
    #         # Check if the player is no longer supported by any platform
    #         is_still_supported = any(
    #             platform_rect.colliderect(player.rect.move(0, BUFFER))
    #             for platform_rect in self.platforms
    #         )

    #         print(f"Player is_still_supported: {is_still_supported} and is_jumping: {player.is_jumping}")

    #         if not is_still_supported:
    #             player.is_jumping = True  # Start falling when not supported
    #             player.is_on_platform = False  # Player is no longer on a platform
    #             #print("Player starts falling.")
    #         else: 
    #             #print("Player remains on the platform.")
    #             pass