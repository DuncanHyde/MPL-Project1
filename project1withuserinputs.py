from __future__ import division
import pygame
import random
import math
import sys
from pygame.locals import*

import os
cwd = os.path.dirname(os.path.realpath(__file__))

import sys
sys.path.append(cwd+'\pygame')

#config vars
gridWidth = 12
gridHeight = 8
total = gridHeight * gridWidth
bgColour = (255,255,255)

obstacles = int(total * 0.25)
stars = int(total * 0.2)

#control = ["empty", "wall", "goal", "star", "visited"]
control = [0, 1, 2, 3, 4]

def PlaceObjects(state, num):
    for i in range(num):                                    #For each required instance of the object
        while True:
            ranx = random.randint(0, gridWidth-1)           #Selects random square
            rany = random.randint(0, gridHeight-1)

            if gamegrid[rany][ranx] == 0:                   #Checks if empty
                gamegrid[rany][ranx] = control[state]       #Sets to new state
                break                                       #Breaks out while loop
    return

def OutputGrid(grid):
    for row in grid:
        out = ""
        for val in row:
            out = str(out) + " " + str(val)
        print out

def find(grid):
   for row, i in enumerate(grid):
       try:
           column = i.index(2)
       except ValueError:
           continue
       return row, column
   return -1

def test(grid):
    row, column = find(grid)

    try:
        if grid[row+1][column] == 0 and row+1 <= gridHeight:
            return True
        if grid[row-1][column] == 0 and row-1 >= 0:
            return True
        if grid[row][column+1] == 0 and column <= gridWidth:
            return True
        if grid[row][column-1] == 0 and column-1 >= 0:
            return True
        return False
    except IndexError:
        return False

while True:
    gamegrid = [[0 for i in xrange(gridWidth)] for i in xrange(gridHeight)]

    PlaceObjects(1, obstacles)
    PlaceObjects(2, 1)
    PlaceObjects(3, stars)
    temp = test(gamegrid)

    if temp == True:
        break

OutputGrid(gamegrid)

#Graphical stuff
pygame.init()
squareRenderSize = 64 # the pixel size of each square
gridColour = { # default colours for square types that do not have textures
	0: (255,255,255), # empty
	1: (0,0,0), # obstacle
	2: (255,0,0), # goal
	3: (0,255,0) # star
}
x1=0
y1=0
charPos = { # character position, in squares, 0,0 is the top left square, 1,0 is one square right from the top left etc.
	'x':x1,
    'y':y1
}
textures = { # texture definitions, they must be either 32x32 or 128x64 (8x 32x32 images that will be animated)
	'char' : pygame.image.load('char.png'),
	'grass' : pygame.image.load('grass.png'), # square background
	1 : pygame.image.load('rock.png'), # obstacle
	2 : pygame.image.load('heart.png'), # goal
	3 : pygame.image.load('star.png') # star
}
textureRects = {} # store texture dimensions into a variable
for i, img in textures.iteritems():
	textureRects[i] = img.get_rect() # store the dimensions
if squareRenderSize != 32: # scale textures if render scale is not the native 32px/square
	renderScale = squareRenderSize/32 # store the scale
	for i, rect in textureRects.iteritems():
		scaledTexture = pygame.transform.scale(textures[i], (int(textureRects[i].width * renderScale), int(textureRects[i].height * renderScale))) # rescale the image
		textures[i] = scaledTexture # save the rescaled image
		textureRects[i].width = textureRects[i].width * renderScale # update the rect width to reflect new scale
		textureRects[i].height = textureRects[i].height * renderScale # update the rect height to reflect new scale


screen = pygame.display.set_mode((gridWidth*squareRenderSize,gridHeight*squareRenderSize)) # initialise the window
clock = pygame.time.Clock()
frame = 1 # sprite-frame counter, defined which area of the sprite to draw
animationSpeed = 2 # lower is faster

def BufferScreen(grid):
	global frame
	realFrame = math.ceil(frame/animationSpeed) # repeat the same sprite position for animSpeed times
	spritePos = pygame.Rect((realFrame-1)%4*squareRenderSize,(math.ceil(realFrame/4)-1)*squareRenderSize,squareRenderSize,squareRenderSize) # define the rect position of the current frame being displayed
	for y, valy in enumerate(grid): # loop the rows
		for x, valx in enumerate(grid[y]): # loop the columns
			screen.blit(textures['grass'], [x * squareRenderSize, y * squareRenderSize])
			if valx in textures: # if this square's content has a texture, draw it
				if textureRects[valx].width == 4*squareRenderSize and textureRects[valx].height == 2*squareRenderSize: # if the texture is an animated one
					screen.blit(textures[valx], [x * squareRenderSize, y * squareRenderSize], spritePos)
				else: # or a static one
					screen.blit(textures[valx], [x * squareRenderSize, y * squareRenderSize])
	screen.blit(textures['char'], [charPos['x'] * squareRenderSize, charPos['y'] * squareRenderSize], spritePos) # draw the character
	frame = frame + 1 # increment sprite-frame counter

	if frame > 8*animationSpeed: # reset the sprite-frame counter if it's greater than 8
		frame = 1



def DrawScreen():
	pygame.display.flip() # render the buffer
	#catch close-window event (pressing x in the corner)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit(); sys.exit();
x1=0
x2=0
while (True): # endless loop to redraw the screen
    for event in pygame.event.get():
        if event.type == KEYDOWN and event.key == K_a:
            x1=x1-1
            msElapsed = clock.tick(30) # define the fps the game should try to run at
            screen.fill(bgColour) # empty the screen
            BufferScreen(gamegrid) # buffer everything to be drawn
            DrawScreen() # draw them

        if event.type == KEYDOWN and event.key == K_d:
            x1=x1+1
            msElapsed = clock.tick(30) # define the fps the game should try to run at
            screen.fill(bgColour) # empty the screen
            BufferScreen(gamegrid) # buffer everything to be drawn
            DrawScreen() # draw them

        if event.type == KEYDOWN and event.key == K_s:
            y1=y1+1
            msElapsed = clock.tick(30) # define the fps the game should try to run at
            screen.fill(bgColour) # empty the screen
            BufferScreen(gamegrid) # buffer everything to be drawn
            DrawScreen() # draw them
        if event.type == KEYDOWN and event.key == K_w:
            y1=y1-1
            msElapsed = clock.tick(30) # define the fps the game should try to run at
            screen.fill(bgColour) # empty the screen
            BufferScreen(gamegrid) # buffer everything to be drawn
            DrawScreen() # draw them
        if x1<0:
            x1=x1+1
            msElapsed = clock.tick(30) # define the fps the game should try to run at
            screen.fill(bgColour) # empty the screen
            BufferScreen(gamegrid) # buffer everything to be drawn
            DrawScreen() # draw them
        if y1<0:
            y1=y1+1
        if x1>11:
            x1=x1-1
        if y1>7:
            y1=y1-1

        #if event.type == MOUSEBUTTONDOWN:
         #   print pygame.mouse.get_pos()
          #  p = pygame.mouse.get_pos()
           # print p[0]
            #print p[1]
            #x1 = round( p[0]/64)
            #y1 = round(p[1]/64)
            #print x1
            #print y1




        charPos = {
            'x':x1,
            'y':y1}
        screen.blit(textures['char'], [charPos['x'] * squareRenderSize, charPos['y'] * squareRenderSize])


        msElapsed = clock.tick(30) # define the fps the game should try to run at
        screen.fill(bgColour) # empty the screen
        BufferScreen(gamegrid) # buffer everything to be drawn
        DrawScreen() # draw them
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        pygame.display.update()

