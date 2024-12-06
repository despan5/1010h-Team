import pygame

class GameState():
    def __init__(self):
        self.states = {
            'START_MENU': 1,
            'GAME_RUNNING': 2,
            'DEATH_SCREEN': 3,
            'HIGH_SCORE': 4,
            'QUIT': 5
        }

        self.music_files = {
            'START_MENU': 'assets/sound/start_song.mp3',
            'GAME_RUNNING': 'assets/sound/song1.mp3',
            'DEATH_SCREEN': 'assets/sound/death_song.mp3',
            'HIGH_SCORE': 'assets/sound/high_score.mp3'
        }
            
        self.current = None
        self.current_music = None
        self.set_state('START_MENU')

    def set_state(self, new_state):
        if new_state in self.states:
            self.current = self.states[new_state]
            # Handle music change
            self.music_state(new_state)

    def is_current(self, state):
        return self.current == self.states.get(state)
    
    def music_state(self, state):
        new_music = self.music_files.get(state)
        
        # Play new music only if it’s different from the current one
        if new_music and new_music != self.current_music:
            pygame.mixer.music.stop()  # Stop any currently playing music
            pygame.mixer.music.load(new_music)
            pygame.mixer.music.play(-1)  # Play the music in a loop
            self.current_music = new_music

    def stop_music(self):
        pygame.mixer.music.stop()
        self.current_music = None