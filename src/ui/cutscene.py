import pygame

class CutSceneManager():

    def __init__(self, screen):
        self.cutscenes_complete = []
        self.cutscene = None
        self.cutscene_running = False

        # Drawing Variables
        self.screen = screen
        self.window_size = 0

    def start_cutscene(self, cutscene):
        if cutscene.name not in self.cutscenes_complete:
            self.cutscenes_complete.append(cutscene.name)
            self.cutscene = cutscene
            self.cutscene_running = True

    def end_cutscene(self):
        self.cutscene = None
        self.cutscene_running = False

    def update(self):
        if self.cutscene_running:
            if self.window_size <self.get_height()*0.3: self.window_size += 2
            self.cutscene_running - self.cutscene.update()
        else:
            self.end_cutscene()

    def draw(self):
            if self.cutscene_running:
                self.cutscene.draw(self.screen)

class StartCutScene:
    def __init__(self, player, screen_width):
        # Variables
        self.name = 'test'
        self.step = 0
        self.cut_scene_running = True

        # Player reference and animation setup
        self.player = player
        self.player.rect.x = 0  # Start the player off-screen
        self.player.rect.y = screen_width // 2  # Center vertically

        self.screen_width = screen_width
        self.animation_delay = 10
        self.animation_counter = 0

        # Dialogue (commented out)
        # self.text = {
        #     'one': "Get ready to jump over obstacles!",
        #     'two': "Great job! You're all set to begin.",
        # }
        # self.text_counter = 0

    def update(self):
        """Update cutscene steps and player animation."""
        # Handle sprite animation
        self.animation_counter += 1
        if self.animation_counter >= self.animation_delay:
            self.animation_counter = 0
            self.player.current_frame = (self.player.current_frame + 1) % len(self.player.current_sprites)
            self.player.image = self.player.current_sprites[self.player.current_frame]

        # Step 1: Player running animation
        self.player.rect.x += 5  # Move right
        if self.player.rect.x > self.screen_width:  # End cutscene when player moves off screen
            self.player.rect.right = 0


    def draw(self, screen):
        """Draw the player running on the screen."""
        self.player.Draw(screen)
        # Dialogue logic (commented out)
        # if self.step == 0:
        #     draw_text(screen, self.text['one'][0:int(self.text_counter)], 50, (255, 255, 255), 50, 50)
        # elif self.step == 2:
        #     draw_text(screen, self.text['two'][0:int(self.text_counter)], 50, (255, 255, 255), 50, 50)