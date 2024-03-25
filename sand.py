import pygame
import time
import random
import math
from sys import exit
from pygame.locals import *
import colorsys

pygame.init()

WIDTH, HEIGHT = 800, 800
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sand!")
clock = pygame.time.Clock()
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
# background_image = pygame.image.load("assets/ocean.gif")
# background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

def createEmptyGrid(s):
    grid = []
    for i in range(s):
        gridRow = [{"state": 0, "color": None} for _ in range(s)]  # Create a row filled with zeros
        gridRow[-1]["state"] = 2  # Set the floor
        grid.append(gridRow)
    return grid

def withinRows(j):
    return j >= 0 and j <= gridSize - 1

def withinCols(i):
    return i >= 0 and i <= gridSize - 1

def main():
    run = True

    # Sand Color
    hue = 0
    sandPalette = [(246,215,176),
                   (242,210,169),
                   (236,204,162),
                   (231,196,150),
                   (226,191,146)]

    
    backgrounds = ["assets/o1.jpg",
                   "assets/o2.jpg",
                   "assets/o3.jpg",
                   "assets/o4.jpg"]
    
    gridSizes = [80, 100, 160, 200]
    
    # LOAD BACKGROUNDS
    background_image1 = pygame.image.load(backgrounds[0])
    background_image1 = pygame.transform.scale(background_image1, (WIDTH, HEIGHT))
    background_image2 = pygame.image.load(backgrounds[1])
    background_image2 = pygame.transform.scale(background_image2, (WIDTH, HEIGHT))
    background_image3 = pygame.image.load(backgrounds[2])
    background_image3 = pygame.transform.scale(background_image3, (WIDTH, HEIGHT))
    background_image4 = pygame.image.load(backgrounds[3])
    background_image4 = pygame.transform.scale(background_image4, (WIDTH, HEIGHT))
    bcount = 0

    # Font
    font = pygame.font.SysFont("Arial", 20)

    # Music and Sounds
    oceanSounds = 'music/waves.mp3'
    oceanMusic = 'music/song.mp3'
    sandPour = 'music/sand.mp3'

    pygame.mixer.music.load(oceanMusic)
    pygame.mixer.music.play(-1)  # Play the first music file on loop

    pygame.mixer.music.load(oceanSounds)
    pygame.mixer.music.play(-1)  # Play the second music file on loop

    pygame.mixer.music.load(sandPour)

    pygame.mixer.set_num_channels(2)  # Set the number of available channels to 2

    channel1 = pygame.mixer.Channel(0)
    channel2 = pygame.mixer.Channel(1)

    track = pygame.mixer.Sound(oceanMusic)
    waves = pygame.mixer.Sound(oceanSounds)
    pour = pygame.mixer.Sound(sandPour)

    channel1.set_volume(0.3)
    channel2.set_volume(2)
    channel1.play(track, loops=-1)  # Play the first music file on channel 1
    channel2.play(waves, loops=-1)  # Play the second music file on channel 2



    # Declare Grid
    size = 0
    global gridSize
    gridSize = 160
    tileWidth = math.floor(WIDTH / gridSize)
    tileHeight = math.floor(HEIGHT / gridSize)

    # Blank tiles
    square = pygame.Surface((tileWidth,tileHeight))
    square.fill(BLACK)

    last_click_time = time.time()

    floor = pygame.Surface((tileWidth, tileHeight))
    floor.fill(sandPalette[4])

    # FILL INITIAL GRID
    grid = createEmptyGrid(gridSize)
    curr = grid

    # Assign color to sand particles upon spawn
    for i in range(gridSize):
        for j in range(gridSize):
            if curr[i][j]["state"] == 1:
                curr[i][j]["color"] = sandPalette[random.randint(0,4)]


    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        bcount += 1
        if bcount < 24:
            if bcount >= 0 and bcount < 6:
                background_image = background_image1
            elif bcount >= 6 and bcount < 12:
                background_image = background_image2
            elif bcount >= 12 and bcount < 18:
                background_image = background_image3
            elif bcount >= 18 and bcount < 24:
                background_image = background_image4
            elif bcount >= 24:
                background_image = background_image1
        if bcount >= 24:
            bcount = 0


        # CLEAR LAST BOARD
        WINDOW.fill(BLACK)
        WINDOW.blit(background_image, (0,0))

        for i, inner_array in enumerate(curr):
            for j, element in enumerate(inner_array):
                posX = i * (WIDTH / gridSize)
                posY = j * (HEIGHT / gridSize)
                if element["state"] == 1:
                    sand = pygame.Surface((tileWidth, tileHeight))
                    sand.fill(element["color"])
                    WINDOW.blit(sand, (posX, posY))
                elif element["state"] == 2:
                    WINDOW.blit(floor, (posX, posY))

        # Check for user click
        current_time = time.time()
        if current_time - last_click_time >= 0.01:
            mouse_buttons = pygame.mouse.get_pressed()
            if mouse_buttons[0]:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                row = math.floor((mouse_x/WIDTH) * gridSize)
                col = math.floor((mouse_y/HEIGHT) * gridSize)
                if withinCols(row+1):
                    curr[row][col]["state"] = 1
                    curr[row][col]["color"] = sandPalette[random.randint(0,4)]
                    curr[row-1][col]["state"] = 1
                    curr[row-1][col]["color"] = sandPalette[random.randint(0,4)]
                    curr[row][col-1]["state"] = 1
                    curr[row][col-1]["color"] = sandPalette[random.randint(0,4)]
                    curr[row+1][col]["state"] = 1
                    curr[row+1][col]["color"] = sandPalette[random.randint(0,4)]
                    curr[row][col+1]["state"] = 1
                    curr[row][col+1]["color"] = sandPalette[random.randint(0,4)]
                last_click_time = current_time
            if mouse_buttons[1]:
                curr = grid

        # Changing grid size // NEEDS WORK //
        # if current_time - last_click_time >= 1:
        #     mouse_buttons = pygame.mouse.get_pressed()
        #     if mouse_buttons[2]:
        #         size += 1
        #         if size >= 0 and size < 4:
        #             gridSize = gridSizes[size]
        #         else:
        #             size = 0
                

        
        # Create the next frame
        nextGrid = createEmptyGrid(gridSize)
        for i in range(len(curr)):
            for j in range(len(curr[i])-1):
                    state = curr[i][j]["state"]
                    if state > 0:
                        below = curr[i][j+1]["state"]
                        dir = 1
                        if random.randint(0,1) < 0.5:
                            dir *= -1
                        

                        # Check if left and right underneath are within bounds
                        belowA = -1
                        belowB = -1
                        if withinCols(i + dir):
                            belowA = curr[i + dir][j+1]["state"]
                        if withinCols(i - dir):
                            belowB = curr[i-dir][j+1]["state"]
                        
                        # Determine where to fall
                        if below == 0:
                            nextGrid[i][j+1]["state"] = state
                            nextGrid[i][j+1]["color"] = curr[i][j]["color"]
                        elif belowA == 0:
                            nextGrid[i+dir][j+1]["state"] = state
                            nextGrid[i+dir][j+1]["color"] = curr[i][j]["color"]
                        elif belowB == 0:
                            nextGrid[i-dir][j+1]["state"] = state
                            nextGrid[i-dir][j+1]["color"] = curr[i][j]["color"]
                        else:
                            nextGrid[i][j]["state"] = state
                            nextGrid[i][j]["color"] = curr[i][j]["color"]
        
        curr = nextGrid
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
