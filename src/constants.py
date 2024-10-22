"""
This is where we're putting all of our super cool constants for the entire project.
You can think of this is super-global unchanging variables.

Things that you should NOT include in this file are:
    - Non-constant variables
    - Constant variables that are only used in one file

Things that you SHOULD include in this file are:
    - Constants that are used in multiple files
"""

import pygame
import os

PROJECT_ROOT: str = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), '..'
    )
)

TPS: int = 60
MAIN_CLOCK: pygame.time.Clock = pygame.time.Clock()
# Screen information will go here when it makes more sense

# Predefined colors (we might want to add a dedicated file for this later!)
WHITE: tuple[int, int, int] = (255, 255, 255)

# Predefined fractions for making things dynamic with different screen sizes!
ONE_THIRD = 1/3
TWO_THIRDS = 2/3
ONE_HALF = 1/2
FIVE_SIXTHS = 5/6
THREE_FOURTHS = 3/4
ONE_FOURTH = 1/4