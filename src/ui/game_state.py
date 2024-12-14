'''
GameState Class

This class manages the different states of the game, including start menu, game running, 
death screen, high score, pause, and quit. It handles state transitions and plays corresponding 
background music for each state.

'''

import pygame

class GameState():
    def __init__(self):
        # define available states
        self.states = {
            'START_MENU': 1,
            'GAME_RUNNING': 2,
            'DEATH_SCREEN': 3,
            'HIGH_SCORE': 4,
            'PAUSE': 5,
            'YOU_WON': 6,
            'QUIT': 7
        }

        # music files corresponding to each state
        self.music_files = {
            'START_MENU': 'assets/sound/start_song.mp3',
            'GAME_RUNNING': 'assets/sound/song1.mp3',
            'DEATH_SCREEN': 'assets/sound/death_song.mp3',
            'HIGH_SCORE': 'assets/sound/high_score.mp3'
        }
            
        self.current = None
        self.current_music = None
        self.set_state('START_MENU')  # initialize to the start menu state

    def set_state(self, new_state):
        # set the current state if it's a valid state
        if new_state in self.states:
            self.current = self.states[new_state]
            self.music_state(new_state)  # change the music to match the new state

    def is_current(self, state):
        # check if the given state is the current one
        return self.current == self.states.get(state)
    
    def music_state(self, state):
        # load and play the appropriate music for the given state
        new_music = self.music_files.get(state)
        
        # play new music only if it's different from the current music
        if new_music and new_music != self.current_music:
            pygame.mixer.music.stop()  # stop any currently playing music
            pygame.mixer.music.load(new_music)
            pygame.mixer.music.play(-1)  # play the music in a loop
            self.current_music = new_music

    def stop_music(self):
        # stop any currently playing music
        pygame.mixer.music.stop()
        self.current_music = None