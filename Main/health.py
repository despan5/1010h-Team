import os
import pygame
import time

class Health:
    def __init__(self):
        pygame.font.init()
        self.font = pygame.font.SysFont(None, 48)
        self.health_count = 4

        base_path = os.path.dirname(__file__)
        health_bar_path = os.path.join(base_path, '..', 'Sprites', 'Health', 'health_bars', 'health_bar.png')
        health_bar_sheet = pygame.image.load(health_bar_path).convert_alpha()

        health_bar_image_width = 48
        health_bar_image_height = 18   
        frame_count = 5

        self.health_frames = []
        for i in range(frame_count):
            frame = health_bar_sheet.subsurface(pygame.Rect(i * health_bar_image_width, 0, health_bar_image_width, health_bar_image_height))
            frame = pygame.transform.scale(frame, (health_bar_image_width * 8, health_bar_image_height * 8))
            self.health_frames.append(frame)
        
        self.current_frame = 4 - self.health_count
        self.health_image = self.health_frames[self.current_frame]

        self.is_flasing = False
        self.flash_start_time = None
        self.flash_duration = 2
        self.flash_interval = .01
        self.last_flash_time = 0

        self.alpha = 0
        self.fade_speed = .5

    def Take_Damage(self):
        if self.health_count > 0:
            self.health_count -= 1
            self.current_frame = 4 - self.health_count
            #print(f"Current health: {self.health_count}")
            #print(f"Current frame: {self.current_frame}")
            self.health_image = self.health_frames[self.current_frame]
            #print("Took damage!")

            self.is_flasing = True
        elif self.health_count == 0:        

            print("you died")
            
    
    def Draw(self, surface, height, width):
        x = 10
        y = 10
        
        if (self.health_count > 0):
            #print(f"Drawing frame: {self.current_frame}")
            surface.blit(self.health_image, (x, y))
        elif (self.health_count == 0):
            font = pygame.font.SysFont('Adobe Garamond', 100)
            red = (255, 0, 0)
            black = (0, 0, 0)
            death_text = font.render("YOU DIED", True, red)
            death_text_rect = death_text.get_rect(center=(width // 2, height // 2))

            

            death_text.set_alpha(self.alpha)

            surface.fill(black)
            

            if self.alpha < (255):
                self.alpha += self.fade_speed
                if self.alpha > (255):
                    self.alpha = 255

            

            surface.blit(death_text, death_text_rect)

