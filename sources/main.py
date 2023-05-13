import base64
import os
import pygame
import sys

# initializing the constructor
pygame.init()

# Setting the name and logo of the window
pygame.display.set_caption('BINGO')

Icon = pygame.image.load('sources/resources/bingo_icon.bmp')
pygame.display.set_icon(Icon)

# screen resolution
res = (1000,600)

# opens up a window
screen = pygame.display.set_mode(res, pygame.RESIZABLE)

# white color
white = (255,255,255)

# light shade of the button
color_light = (170,170,170) # Grey

# dark shade of the button
color_dark = (76,175,80) # Green

# stores the width of the
# screen into a variable
width = screen.get_width()

# stores the height of the
# screen into a variable
height = screen.get_height()


# defining a font
smallfont = pygame.font.SysFont('Verdana',35)

# rendering a text written in
# this font
text = smallfont.render('Exit', True, white)

# String with the scene in it
scene = "mainMenu"

def mainMenu():
	for ev in pygame.event.get():
		
		if ev.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
			
		#checks if a mouse is clicked
		if ev.type == pygame.MOUSEBUTTONDOWN:
			
			#if the mouse is clicked on the
			# button the game is terminated
			if width/2-70 <= mouse[0] <= width/2+70 and height/2-20 <= mouse[1] <= height/2+20:
				pygame.quit()
				sys.exit()
	
	# if mouse is hovered on a button it
	# changes to lighter shade
	if width/2-70 <= mouse[0] <= width/2+70 and height/2-20 <= mouse[1] <= height/2+20:
		pygame.draw.rect(screen,color_light,[width/2-70,height/2-20,140,40])
		
	else:
		pygame.draw.rect(screen,color_dark,[width/2-70,height/2-20,140,40])
	
	# superimposing the text onto our button
	screen.blit(text, (width/2-60,height/2-25))
	
	# updates the frames of the game
	pygame.display.update()


def game():
	for ev in pygame.event.get():
		
		if ev.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
			
		#checks if a mouse is clicked
		if ev.type == pygame.MOUSEBUTTONDOWN:
			
			#if the mouse is clicked on the
			# button the game is terminated
			if width/2-70 <= mouse[0] <= width/2+70 and height/2-20 <= mouse[1] <= height/2+20:
				pygame.quit()
				sys.exit()
	
	# if mouse is hovered on a button it
	# changes to lighter shade
	if width/2-70 <= mouse[0] <= width/2+70 and height/2-20 <= mouse[1] <= height/2+20:
		pygame.draw.rect(screen,color_light,[width/2-70,height/2-20,140,40])
		
	else:
		pygame.draw.rect(screen,color_dark,[width/2-70,height/2-20,140,40])
	
	# superimposing the text onto our button
	screen.blit(text, (width/2-60,height/2-25))
	
	# updates the frames of the game
	pygame.display.update()




while True:
	# fills the screen with a color
	screen.fill((18,18,18))
	

	# stores the (x,y) coordinates into
	# the variable as a tuple
	mouse = pygame.mouse.get_pos()
	if scene == "mainMenu":
		mainMenu()
	elif scene == "game":
		game()


