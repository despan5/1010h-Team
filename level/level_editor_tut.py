"""
Level Editor

This script creates a level editor for a 2D game using Pygame. 
It includes features to draw a grid, manage tiles, and save/load level data.
"""

import pygame
import button
import csv
import pickle

pygame.init()

clock = pygame.time.Clock()  # game clock to control FPS
FPS = 60  # set frames per second

# game window dimensions and margins
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450
LOWER_MARGIN = 100
SIDE_MARGIN = 300

# initialize the display window
screen = pygame.display.set_mode((SCREEN_WIDTH + SIDE_MARGIN, SCREEN_HEIGHT + LOWER_MARGIN))
pygame.display.set_caption('Level Editor')

# define game variables
ROWS = 16  # number of rows in the grid
MAX_COLS = 150  # maximum number of columns in the grid
TILE_SIZE = SCREEN_HEIGHT // ROWS  # size of each tile
TILE_TYPES = 2  # number of different tile types
level = 0  # current level
current_tile = 0  # currently selected tile type
scroll_left = False  # flag for scrolling left
scroll_right = False  # flag for scrolling right
scroll = 0  # current scroll position
scroll_speed = 1  # speed of scrolling

# load background images
pine1_img = pygame.image.load('level/img/Background/pine1.png').convert_alpha()
pine2_img = pygame.image.load('level/img/Background/pine2.png').convert_alpha()
mountain_img = pygame.image.load('level/img/Background/mountain.png').convert_alpha()
sky_img = pygame.image.load('level/img/Background/sky_cloud.png').convert_alpha()

# store tile images in a list
img_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(f'level/img/tile/{x}.png').convert_alpha()
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))  # scale to fit tile size
    img_list.append(img)

# load button images
save_img = pygame.image.load('level/img/save_btn.png').convert_alpha()
load_img = pygame.image.load('level/img/load_btn.png').convert_alpha()

# define colors
GREEN = (144, 201, 120)  # background color
WHITE = (255, 255, 255)  # grid line color
RED = (200, 25, 25)  # highlight color

# define font
font = pygame.font.SysFont('Futura', 30)

# create an empty tile grid with default values of -1
world_data = []
for row in range(ROWS):
    r = [-1] * MAX_COLS
    world_data.append(r)

# create the ground layer
for tile in range(0, MAX_COLS):
    world_data[ROWS - 1][tile] = 0

# function for displaying text on the screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)  # render text as an image
    screen.blit(img, (x, y))  # draw image to screen

# function to draw the background
def draw_bg():
    screen.fill(GREEN)  # fill background with solid color
    width = sky_img.get_width()
    # draw background layers with parallax scrolling
    for x in range(4):
        screen.blit(sky_img, ((x * width) - scroll * 0.5, 0))
        screen.blit(mountain_img, ((x * width) - scroll * 0.6, SCREEN_HEIGHT - mountain_img.get_height() - 300))
        screen.blit(pine1_img, ((x * width) - scroll * 0.7, SCREEN_HEIGHT - pine1_img.get_height() - 150))
        screen.blit(pine2_img, ((x * width) - scroll * 0.8, SCREEN_HEIGHT - pine2_img.get_height()))

# function to draw the grid
def draw_grid():
    # draw vertical lines
    for c in range(MAX_COLS + 1):
        pygame.draw.line(screen, WHITE, (c * TILE_SIZE - scroll, 0), (c * TILE_SIZE - scroll, SCREEN_HEIGHT))
    # draw horizontal lines
    for c in range(ROWS + 1):
        pygame.draw.line(screen, WHITE, (0, c * TILE_SIZE), (SCREEN_WIDTH, c * TILE_SIZE))

# function to draw world tiles
def draw_world():
    for y, row in enumerate(world_data):
        for x, tile in enumerate(row):
            if tile >= 0:  # only draw tiles with valid IDs
                screen.blit(img_list[tile], (x * TILE_SIZE - scroll, y * TILE_SIZE))

# create buttons
save_button = button.Button(SCREEN_WIDTH // 2 + 150, SCREEN_HEIGHT + LOWER_MARGIN - 50, save_img, 1)
load_button = button.Button(SCREEN_WIDTH // 2 + 300, SCREEN_HEIGHT + LOWER_MARGIN - 50, load_img, 1)

# create tile selection buttons
button_list = []
button_col = 0
button_row = 0
for i in range(len(img_list)):
    tile_button = button.Button(SCREEN_WIDTH + (75 * button_col) + 50, 75 * button_row + 50, img_list[i], 1)
    button_list.append(tile_button)
    button_col += 1
    if button_col == 3:  # move to next row after 3 buttons
        button_row += 1
        button_col = 0

# main game loop
run = True
while run:
    clock.tick(FPS)  # maintain consistent FPS

    draw_bg()  # draw background layers
    draw_grid()  # draw grid lines
    draw_world()  # draw placed tiles

    # display level info
    draw_text(f'Level: {level}', font, WHITE, 10, SCREEN_HEIGHT + LOWER_MARGIN - 90)
    draw_text('Press UP or DOWN to change level', font, WHITE, 10, SCREEN_HEIGHT + LOWER_MARGIN - 60)

    # handle save and load buttons
    if save_button.draw(screen):
        with open(f'level{level}_data.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            for row in world_data:
                writer.writerow(row)
    if load_button.draw(screen):
        scroll = 0  # reset scroll to start
        with open(f'level{level}_data.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for x, row in enumerate(reader):
                for y, tile in enumerate(row):
                    world_data[x][y] = int(tile)

    # draw tile panel
    pygame.draw.rect(screen, GREEN, (SCREEN_WIDTH, 0, SIDE_MARGIN, SCREEN_HEIGHT))

    # handle tile selection
    for button_count, i in enumerate(button_list):
        if i.draw(screen):
            current_tile = button_count

    # highlight selected tile
    pygame.draw.rect(screen, RED, button_list[current_tile].rect, 3)

    # handle scrolling
    if scroll_left and scroll > 0:
        scroll -= 5 * scroll_speed
    if scroll_right and scroll < (MAX_COLS * TILE_SIZE) - SCREEN_WIDTH:
        scroll += 5 * scroll_speed

    # handle tile placement
    pos = pygame.mouse.get_pos()
    x = (pos[0] + scroll) // TILE_SIZE
    y = pos[1] // TILE_SIZE
    if pos[0] < SCREEN_WIDTH and pos[1] < SCREEN_HEIGHT:  # ensure within bounds
        if pygame.mouse.get_pressed()[0] == 1:  # left-click to place tile
            if world_data[y][x] != current_tile:
                world_data[y][x] = current_tile
        if pygame.mouse.get_pressed()[2] == 1:  # right-click to remove tile
            world_data[y][x] = -1

    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                level += 1
            if event.key == pygame.K_DOWN and level > 0:
                level -= 1
            if event.key == pygame.K_LEFT:
                scroll_left = True
            if event.key == pygame.K_RIGHT:
                scroll_right = True
            if event.key == pygame.K_RSHIFT:
                scroll_speed = 5
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                scroll_left = False
            if event.key == pygame.K_RIGHT:
                scroll_right = False
            if event.key == pygame.K_RSHIFT:
                scroll_speed = 1

    pygame.display.update()  # update display

pygame.quit()  # exit game
