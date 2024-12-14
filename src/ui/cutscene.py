"""
CutSceneManager and StartCutScene Classes

These classes manage and display cutscenes in the game, allowing for scripted events and animations.
"""

import pygame

class CutSceneManager:
    """
    Manages the execution and flow of cutscenes during the game.
    """

    def __init__(self, screen):
        """
        Initialize the CutSceneManager.

        Args:
            screen (pygame.Surface): The game screen where cutscenes will be drawn.
        """
        self.cutscenes_complete = []  # list of completed cutscenes
        self.cutscene = None  # currently active cutscene
        self.cutscene_running = False  # flag to check if a cutscene is active

        # Drawing variables
        self.screen = screen
        self.window_size = 0

    def start_cutscene(self, cutscene):
        """
        Start a cutscene if it hasn't been completed yet.

        Args:
            cutscene (StartCutScene): The cutscene to start.
        """
        if cutscene.name not in self.cutscenes_complete:
            self.cutscenes_complete.append(cutscene.name)
            self.cutscene = cutscene
            self.cutscene_running = True

    def end_cutscene(self):
        """
        End the currently active cutscene.
        """
        self.cutscene = None
        self.cutscene_running = False

    def update(self):
        """
        Update the active cutscene and manage the opening window animation.
        """
        if self.cutscene_running:
            if self.window_size < self.screen.get_height() * 0.3:
                self.window_size += 2
            self.cutscene.update()
        else:
            self.end_cutscene()

    def draw(self):
        """
        Draw the active cutscene on the screen.
        """
        if self.cutscene_running:
            self.cutscene.draw(self.screen)


class StartCutScene:
    """
    Represents a specific cutscene, showing the player entering the screen.

    Args:
        player (Player): The player object to animate.
        screen_width (int): The width of the screen for positioning.
    """

    def __init__(self, player, screen_width):
        # variables
        self.name = 'test'  # name of the cutscene
        self.step = 0  # current step of the cutscene
        self.cut_scene_running = True

        # player reference and animation setup
        self.player = player
        self.player.rect.x = 0  # start the player off-screen
        self.player.rect.y = screen_width // 2  # center vertically

        self.screen_width = screen_width
        self.animation_delay = 10
        self.animation_counter = 0

        # Optional dialogue logic (currently disabled)
        # self.text = {
        #     'one': "Get ready to jump over obstacles!",
        #     'two': "Great job! You're all set to begin.",
        # }
        # self.text_counter = 0

    def update(self):
        """
        Update the cutscene logic, including player movement and animations.
        """
        # handle sprite animation
        self.animation_counter += 1
        if self.animation_counter >= self.animation_delay:
            self.animation_counter = 0
            self.player.current_frame = (self.player.current_frame + 1) % len(self.player.current_sprites)
            self.player.image = self.player.current_sprites[self.player.current_frame]

        # step 1: Move the player across the screen
        self.player.rect.x += 5  # move the player to the right
        if self.player.rect.x > self.screen_width:  # reset position after moving off screen
            self.cut_scene_running = False  # end cutscene

    def draw(self, screen):
        """
        Draw the player and any related visuals on the screen.

        Args:
            screen (pygame.Surface): The game screen to draw on.
        """
        self.player.Draw(screen)
        # Optional dialogue drawing logic (currently disabled)
        # if self.step == 0:
        #     draw_text(screen, self.text['one'][0:int(self.text_counter)], 50, (255, 255, 255), 50, 50)
        # elif self.step == 2:
        #     draw_text(screen, self.text['two'][0:int(self.text_counter)], 50, (255, 255, 255), 50, 50)