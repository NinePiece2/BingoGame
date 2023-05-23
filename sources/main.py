# Imports and setting pygame to use the resolution of the display, not a scaled one
import sys

if sys.platform == 'win32':
    import ctypes
    try:
       ctypes.windll.user32.SetProcessDPIAware()
    except AttributeError:
        pass

import pygame
import random
import datetime
import base64
import json
from tkinter import Tk, filedialog, messagebox
import os
from sys import exit
from PIL import Image
import webbrowser

# Global Variable Declorations
numbers = []
board = []
boardText = []
currentTurn = -1
configFolder='settings'
configFile='settings/config.ini'
savesFolder='saves'
framerate = 60

base_screen_width = 1100
base_screen_height = 600

scale_factor_x = 1.5
scale_factor_y = 1.5

screen1 = pygame.display.set_mode((1100*scale_factor_x, 600*scale_factor_y), pygame.RESIZABLE)

# Check if the settings and saves folder exists, if it doesn't make the folders
if not os.path.exists(configFolder):
    os.makedirs(configFolder)
if not os.path.exists(savesFolder):
    os.makedirs(savesFolder)

    
# Check if the config file exisits and if it doesn't one is created
def configFileExists():
    try:
        with open(configFile, 'r') as f:
            return True
    except:
        return False

if configFileExists() == False:
    with open(configFile, 'w') as f:
        f.write('')


# Check if the configFile is empty
def emptyConfigFile():
    try:
        with open(configFile, 'r') as f:
            return f.read() == ''
    except:
        return False

# if emptyConfigFile then add a framerate setting, else read the value of the framerate setting
if emptyConfigFile():
    with open(configFile, 'r') as f:
        lines = f.readlines()
        with open(configFile, 'a') as f:
            f.write('MaxFramerate=' + str(framerate))
else:
    with open(configFile, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if 'MaxFramerate' in line:
                framerate = line.split('=')[1]
                framerate = int(framerate)
        

# Create the Tkinter root window for the messagebox
root = Tk()
root.wm_attributes("-topmost", 1)
root.withdraw()  # Hide the root window

# light shade of the button
color_light = (42,42,42) # Grey

# dark shade of the button
color_dark = (76,175,80) # Green

# Base class for setting up the pygmae application
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1100*scale_factor_x, 600*scale_factor_y), pygame.RESIZABLE)

        # Setting the name and logo of the window
        pygame.display.set_caption('BINGO')
        image = Image.open('resources/bingo_icon.png')
        Icon = pygame.image.fromstring(image.tobytes(), image.size, image.mode)
        #Icon = pygame.image.load('resources/bingo_icon.png')
        pygame.display.set_icon(Icon)
        self.clock = pygame.time.Clock()
        self.current_scene = None


    def run(self):
        self.current_scene = MenuScene(self)

        while True:
            # Handle events
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            self.current_scene.handle_events(events)

            # Update
            self.current_scene.update()

            # Draw
            self.current_scene.draw()

            # Update the display
            pygame.display.flip()

            # Cap the frame rate
            self.clock.tick(framerate)

    def change_scene(self, scene):
        self.current_scene = scene

# Base Class for all Scenes in the application
class Scene:
    def __init__(self, game):
        self.game = game

    def handle_events(self, events):
        pass

    def update(self):
        pass

    def draw(self):
        pass

# Function that is a child of the Scene Class to make the Main Menu of the Application
class MenuScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.SysFont('Verdana',int(35*(scale_factor_x+scale_factor_y)/2))

    # Handles Events on the Menu Scene
    def handle_events(self, events):
        for event in events:
            
            # Gets the current height and width of the window
            width = screen1.get_width()
            height = screen1.get_height()
            
            global scale_factor_x, scale_factor_y

            # Sets the scale factors based on the current size of the screen and the inital size
            scale_factor_x = self.game.screen.get_width() / base_screen_width
            scale_factor_y = self.game.screen.get_height() / base_screen_height

            mouse = pygame.mouse.get_pos()

            # Handles when the mouse selects screen elements
            if event.type == pygame.MOUSEBUTTONDOWN:
                if width/2-70*scale_factor_x <= mouse[0] <= width/2+70*scale_factor_x and height/2-80*scale_factor_y <= mouse[1] <= height/2-40*scale_factor_y:
                    # Play Button
                    self.game.change_scene(GameScene(self.game))
                elif width/2-70*scale_factor_x <= mouse[0] <= width/2+70*scale_factor_x and height/2+40*scale_factor_y <= mouse[1] <= height/2+80*scale_factor_y:
                    # Exit Button
                    pygame.quit()
                    exit()
                elif width/2-70*scale_factor_x <= mouse[0] <= width/2+70*scale_factor_x and height/2-20*scale_factor_y <= mouse[1] <= height/2+20*scale_factor_y:
                    # Rules Buton 
                    self.game.change_scene(RulesScene(self.game))
                elif width - 150*scale_factor_x <= mouse[0] <= width - 10*scale_factor_x and 20*scale_factor_y <= mouse[1] <= 60*scale_factor_y:
                    # Load Save Button
                    # choose a file from explorer to load the number snad current turn from
                    # Prompt the user to select a file

                    current = os.getcwd()
                    file_path = filedialog.askopenfilename(initialdir=current + '/saves')

                    # Check if a file was selected
                    if file_path:
                        # Read the encoded data from the file
                        try:
                            with open(file_path, "rb") as file:
                                encoded_data = file.read()

                            # Decode the base64-encoded data
                            decoded_data = base64.b64decode(encoded_data)

                            # Decode the data from JSON
                            json_data = decoded_data.decode("utf-8")
                            data = json.loads(json_data)

                            # Extract the numbers and currentTurn from the data
                            global numbers, currentTurn
                            numbers = data["numbers"]
                            currentTurn = data["currentTurn"]

                            Tk().wm_withdraw()
                            messagebox.showinfo('Continue', f"Save {file_path} Loaded")

                        except:
                            print("Wrong File/ Data Corrupted or Tampered with")
                            Tk().wm_withdraw()
                            messagebox.showerror('Error', f"Wrong File/ Data Corrupted or Tampered with")
                            return

                    else:
                        print("No file selected.")
                        return

                elif width - 150*scale_factor_x <= mouse[0] <= width - 10*scale_factor_x and 80*scale_factor_y <= mouse[1] <= 120*scale_factor_y:
                    # Save Button

                    if not os.path.exists(savesFolder):
                        os.makedirs(savesFolder)
                    
                    # Generate a unique filename using the current date and time
                    now = datetime.datetime.now()
                    current_time = datetime.datetime.now()
                    filename = current_time.strftime("Bingo-Save-%Y-%m-%d_%H-%M-%S") + ".txt"
                    file_path = os.path.join(savesFolder, filename)

                    # Prepare the data to be saved
                    data = {
                        "numbers": numbers,
                        "currentTurn": currentTurn
                    }

                    # Encode the data as JSON and convert it to bytes
                    json_data = json.dumps(data).encode("utf-8")

                    # Encode the bytes using base64
                    encoded_data = base64.b64encode(json_data)

                    # Write the encoded data to the file
                    with open(file_path, "wb") as file:
                        file.write(encoded_data)

                    print(f"Data saved to {filename}")

                    Tk().wm_withdraw()
                    messagebox.showinfo('Continue', f"New Save Made: {filename}")

    # Displays the user interface
    def draw(self):
        # Gets the current height and width of the window
        width = screen1.get_width()
        height = screen1.get_height()
        mouse = pygame.mouse.get_pos()

        # Sets the default cursor
        hover = False

        # Sets the scale factors based on the current size of the screen and the inital size
        global scale_factor_x, scale_factor_y
        scale_factor_x = self.game.screen.get_width() / base_screen_width
        scale_factor_y = self.game.screen.get_height() / base_screen_height

        # Sets the font size based on the scale factors 
        self.font = pygame.font.SysFont('Verdana',int(35*(scale_factor_x+scale_factor_y)/2))

        # Background Colour
        self.game.screen.fill((18,18,18))

        # Checks if the user is hovering the menu options  
        # Rules Menu
        if width/2-70*scale_factor_x <= mouse[0] <= width/2+70*scale_factor_x and height/2-20*scale_factor_y <= mouse[1] <= height/2+20*scale_factor_y:
            pygame.draw.rect(self.game.screen,color_light,[width/2-70*scale_factor_x,height/2-20*scale_factor_y,140*scale_factor_x,40*scale_factor_y])  
            hover = True         
        else:
            pygame.draw.rect(self.game.screen,color_dark,[width/2-70*scale_factor_x,height/2-20*scale_factor_y,140*scale_factor_x,40*scale_factor_y])

        # Exit Button
        if width/2-70*scale_factor_x <= mouse[0] <= width/2+70*scale_factor_x and height/2-80*scale_factor_y <= mouse[1] <= height/2-40*scale_factor_y:
            pygame.draw.rect(self.game.screen,color_light,[width/2-70*scale_factor_x,height/2-80*scale_factor_y,140*scale_factor_x,40*scale_factor_y])
            hover = True
        else:
            pygame.draw.rect(self.game.screen,color_dark,[width/2-70*scale_factor_x,height/2-80*scale_factor_y,140*scale_factor_x,40*scale_factor_y])

        # Game Button / Menu
        if width/2-70*scale_factor_x <= mouse[0] <= width/2+70*scale_factor_x and height/2+40*scale_factor_y <= mouse[1] <= height/2+80*scale_factor_y:
            pygame.draw.rect(self.game.screen,color_light,[width/2-70*scale_factor_x,height/2+40*scale_factor_y,140*scale_factor_x,40*scale_factor_y])
            hover = True
        else: 
            pygame.draw.rect(self.game.screen,color_dark,[width/2-70*scale_factor_x,height/2+40*scale_factor_y,140*scale_factor_x,40*scale_factor_y])

        # Load Save Button
        if width - 150*scale_factor_x <= mouse[0] <= width - 10*scale_factor_x and 20*scale_factor_y <= mouse[1] <= 60*scale_factor_y:
            pygame.draw.rect(self.game.screen,color_light,[width - 150*scale_factor_x,20*scale_factor_y,140*scale_factor_x,40*scale_factor_y])
            hover = True
        else: 
            pygame.draw.rect(self.game.screen,color_dark,[width - 150*scale_factor_x,20*scale_factor_y,140*scale_factor_x,40*scale_factor_y])

        # Save Button
        if width - 150*scale_factor_x <= mouse[0] <= width - 10*scale_factor_x and 80*scale_factor_y <= mouse[1] <= 120*scale_factor_y:
            pygame.draw.rect(self.game.screen,color_light,[width - 150*scale_factor_x,80*scale_factor_y,140*scale_factor_x,40*scale_factor_y])
            hover = True
        else: 
            pygame.draw.rect(self.game.screen,color_dark,[width - 150*scale_factor_x,80*scale_factor_y,140*scale_factor_x,40*scale_factor_y])
        
        # Changes the cursor wheather or not the user is hovering an option to select
        if hover:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND) 
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW) 

        # Creates text boxes for the different options and the main manu page title
        exitText = self.font.render('EXIT', True, (255, 255, 255))
        playText = self.font.render('PLAY', True, (255, 255, 255))
        rulesText = self.font.render('RULES', True, (255, 255, 255))
        loadSaveText = self.font.render('LOAD', True, (255, 255, 255))
        saveText = self.font.render('SAVE', True, (255, 255, 255))
        text = self.font.render("Main Menu", True, (255, 255, 255))

        # Shows and scales the text boxes based on the scale factors
        self.game.screen.blit(exitText, (width/2-39*scale_factor_x,height/2+36*scale_factor_y))
        self.game.screen.blit(playText, (width/2-39*scale_factor_x,height/2-84*scale_factor_y))
        self.game.screen.blit(rulesText, (width/2-56*scale_factor_x,height/2-23*scale_factor_y))
        self.game.screen.blit(text, (10, 10))
        self.game.screen.blit(loadSaveText, (width-127*scale_factor_x, 17*scale_factor_y))
        self.game.screen.blit(saveText, (width-127*scale_factor_x, 77*scale_factor_y))

# Function that is a child of the Scene Class to make the Game Menu of the Application
class GameScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        gameSetup() # Sets up the shuffled list of numbers for the game

    # Handles Events for the game scene
    def handle_events(self, events):
        for event in events:

            # Gets the current height and width of the window
            width = screen1.get_width()
            height = screen1.get_height()
            
            # Sets the scale factors based on the current size of the screen and the inital size
            global scale_factor_x, scale_factor_y, currentTurn
            scale_factor_x = self.game.screen.get_width() / base_screen_width
            scale_factor_y = self.game.screen.get_height() / base_screen_height

            # Gets the position of the mouse
            mouse = pygame.mouse.get_pos()

            # Based on the events and the locaton / other event decide what to do
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Main Menu Button
                if 75*scale_factor_x <= mouse[0] <= 215*scale_factor_x and height-100*scale_factor_y <= mouse[1] <= height-60*scale_factor_y:
                    # Go back to the main menu
                    self.game.change_scene(MenuScene(self.game))
                
                # Next Turn Button
                elif 75*scale_factor_x <= mouse[0] <= 215*scale_factor_x and 250*scale_factor_y <= mouse[1] <= 290*scale_factor_y:
                    # Increment the currentTurn counter if its possible, if not output an error to the user.
                    if currentTurn < 74:
                        currentTurn+=1
                    else:
                        Tk().wm_withdraw()
                        messagebox.showinfo('Game Ended', f"The game has concluded as all balls have been drawn. To play again restart the application.")

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Go back to the main menu
                    self.game.change_scene(MenuScene(self.game))


    def update(self):
        pass
    
    # Displays the user interface of the scene
    def draw(self):

        # Background Colour
        self.game.screen.fill((18,18,18))

        # Gets the current height and width of the window
        width = screen1.get_width()
        height = screen1.get_height()

        # Gets the current position of the mouse
        mouse = pygame.mouse.get_pos()

        # Helps in checking if the user is hovering something that is clickable
        hover = False

        # Sets the scale factors based on the current size of the screen and the inital size
        global scale_factor_x, scale_factor_y, board, boardText
        scale_factor_x = self.game.screen.get_width() / base_screen_width
        scale_factor_y = self.game.screen.get_height() / base_screen_height
        
        # Sets the font size based on the scale factors for the button options
        self.font = pygame.font.SysFont('Verdana',int(24*(scale_factor_x+scale_factor_y)/2))

        # Next Turn Button
        if 45*scale_factor_x <= mouse[0] <= 185*scale_factor_x and 250*scale_factor_y <= mouse[1] <= 290*scale_factor_y:
            pygame.draw.rect(self.game.screen,color_light,[45*scale_factor_x,250*scale_factor_y,140*scale_factor_x,40*scale_factor_y]) 
            hover = True        
        else:
            pygame.draw.rect(self.game.screen,color_dark,[45*scale_factor_x,250*scale_factor_y,140*scale_factor_x,40*scale_factor_y])

        # Main Menu Button
        if 45*scale_factor_x <= mouse[0] <= 185*scale_factor_x and height-100*scale_factor_y <= mouse[1] <= height-60*scale_factor_y:
            pygame.draw.rect(self.game.screen,color_light,[45*scale_factor_x,height-100*scale_factor_y,140*scale_factor_x,40*scale_factor_y])  
            hover = True         
        else:
            pygame.draw.rect(self.game.screen,color_dark,[45*scale_factor_x,height-100*scale_factor_y,140*scale_factor_x,40*scale_factor_y])
        
        # Changes the cursor wheather or not the user is hovering an option to select
        if hover:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND) 
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW) 

        # Creates variables that can be changed depending on the next BINGO draw
        nextStatement = f""
        blankImage = Image.open('resources/Blank.png') # Blank image if no turns have been made yet
        currentRoll = pygame.image.fromstring(blankImage.tobytes(), blankImage.size, blankImage.mode)
        nextColour = (255,255,255)
        global currentTurn

        # Opens the images for the different BINGO ball colours
        blueCircImg = Image.open('resources/BlueCirc.png')
        greenCircImg = Image.open('resources/GreenCirc.png')
        orangeCircImg = Image.open('resources/OrangeCirc.png')
        redCircImg = Image.open('resources/RedCirc.png')
        whiteCircImg = Image.open('resources/WhiteCirc.png').convert("RGBA")

        # Loads the images for the different BINGO ball colours from Pillow to a Pygame image
        blueCirc = pygame.image.fromstring(blueCircImg.tobytes(), blueCircImg.size, blueCircImg.mode)
        greenCirc = pygame.image.fromstring(greenCircImg.tobytes(), greenCircImg.size, greenCircImg.mode)
        orangeCirc = pygame.image.fromstring(orangeCircImg.tobytes(), orangeCircImg.size, orangeCircImg.mode)
        redCirc = pygame.image.fromstring(redCircImg.tobytes(), redCircImg.size, redCircImg.mode)
        whiteCirc = pygame.image.fromstring(whiteCircImg.tobytes(), whiteCircImg.size, whiteCircImg.mode)

        # First checks if a ball has been drawn yet
        if currentTurn >= 0:

            # Checks what colour the next ball is and sets the nextStatement, currentRoll and nextColour variables accordingly
            if 1 <= numbers[currentTurn] <= 15:
                nextStatement = f"B{numbers[currentTurn]}"
                currentRoll = blueCirc
                nextColour = (255,255,255)
            elif 16 <= numbers[currentTurn] <= 30:
                nextStatement = f"I{numbers[currentTurn]}"
                currentRoll = whiteCirc
                nextColour = (0,0,0)
            elif 31 <= numbers[currentTurn] <= 45:
                nextStatement = f"N{numbers[currentTurn]}"
                currentRoll = redCirc
                nextColour = (255,255,255)
            elif 46 <= numbers[currentTurn] <= 60:
                nextStatement = f"G{numbers[currentTurn]}"
                currentRoll = greenCirc
                nextColour = (255,255,255)
            elif 61 <= numbers[currentTurn] <= 75:
                nextStatement = f"O{numbers[currentTurn]}"
                currentRoll = orangeCirc
                nextColour = (255,255,255)

            # Sets the list to be blank
            board = []
            boardText = []

            # Creates lists of blank images and blank text
            for i in range(75):
                board.append(pygame.image.fromstring(blankImage.tobytes(), blankImage.size, blankImage.mode))
                boardText.append("")
            
            # For each draw up to now add the numbers that have been drawn to a list of drawn numbers in their numerical order (boardText list)
            #  and add the corresponding coloured ball to its numerical location in the board list.
            for i in range(currentTurn+1):
                boardText[numbers[i]-1] = numbers[i]
                if 1 <= numbers[i] <= 15:
                    board[numbers[i]-1] = blueCirc
                elif 16 <= numbers[i] <= 30:
                    board[numbers[i]-1] = whiteCirc
                elif 31 <= numbers[i] <= 45:
                    board[numbers[i]-1] = redCirc
                elif 46 <= numbers[i] <= 60:
                    board[numbers[i]-1] = greenCirc
                elif 61 <= numbers[i] <= 75:
                    board[numbers[i]-1] = orangeCirc    

            # Displays the balls that have already been drawn
            # Displays the first 15 balls for B
            for i in range(15):
                board[i] = pygame.transform.scale(board[i], (40*scale_factor_x, 40*scale_factor_y))
                self.game.screen.blit(board[i], ((310+i*50)*scale_factor_x, 100*scale_factor_y))
                boardText[i] = self.font.render(str(boardText[i]), True, (255, 255, 255))
                if i <= 9:
                    size = 0
                else :
                    size = 5
                self.game.screen.blit(boardText[i], ((320+i*50-size)*scale_factor_x, 105*scale_factor_y))
            
            # Displays the second 15 balls for I
            for i in range(15,30):
                board[i] = pygame.transform.scale(board[i], (40*scale_factor_x, 40*scale_factor_y))
                self.game.screen.blit(board[i], ((310+(i-15)*50)*scale_factor_x, 200*scale_factor_y))
                boardText[i] = self.font.render(str(boardText[i]), True, (0, 0, 0))
                self.game.screen.blit(boardText[i], ((320+(i-15)*50-size)*scale_factor_x, 205*scale_factor_y))

            # Displays the third 15 balls for N
            for i in range(30,45):
                board[i] = pygame.transform.scale(board[i], (40*scale_factor_x, 40*scale_factor_y))
                self.game.screen.blit(board[i], ((310+(i-30)*50)*scale_factor_x, 300*scale_factor_y))
                boardText[i] = self.font.render(str(boardText[i]), True, (255, 255, 255))
                self.game.screen.blit(boardText[i], ((320+(i-30)*50-size)*scale_factor_x, 305*scale_factor_y))
            
            # Displays the fourth 15 balls for G
            for i in range(45,60):
                board[i] = pygame.transform.scale(board[i], (40*scale_factor_x, 40*scale_factor_y))
                self.game.screen.blit(board[i], ((310+(i-45)*50)*scale_factor_x, 400*scale_factor_y))
                boardText[i] = self.font.render(str(boardText[i]), True, (255, 255, 255))
                self.game.screen.blit(boardText[i], ((320+(i-45)*50-size)*scale_factor_x, 405*scale_factor_y))
            
            # Displays the fifth 15 balls for O
            for i in range(60,75):
                board[i] = pygame.transform.scale(board[i], (40*scale_factor_x, 40*scale_factor_y))
                self.game.screen.blit(board[i], ((310+(i-60)*50)*scale_factor_x, 500*scale_factor_y))
                boardText[i] = self.font.render(str(boardText[i]), True, (255, 255, 255))
                self.game.screen.blit(boardText[i], ((320+(i-60)*50-size)*scale_factor_x, 505*scale_factor_y))
        
        # If no balls have been drawn yet display the blank board
        else:
            nextStatement = f""

        # Change the size of the currently rolled ball
        currentRoll = pygame.transform.scale(currentRoll, (80*scale_factor_x, 80*scale_factor_y))
        
        # Create the text for the buttons on the scene
        text = self.font.render("Main Menu", True, (255, 255, 255))
        nextText = self.font.render('Next Turn', True, (255, 255, 255))

        # Increase the size of the font and create a header for the Past Draws section
        self.font = pygame.font.SysFont('Verdana',int(35*(scale_factor_x+scale_factor_y)/2))
        title = self.font.render('PAST DRAWS', True, (255, 255, 255))

        # Increase the size of the font more and create text for the B I N G O parts of the Past Draws section
        self.font = pygame.font.SysFont('Verdana',int(55*(scale_factor_x+scale_factor_y)/2))
        titleB = self.font.render('B', True, (255, 255, 255))
        titleI = self.font.render('I', True, (255, 255, 255))
        titleN = self.font.render('N', True, (255, 255, 255))
        titleG = self.font.render('G', True, (255, 255, 255))
        titleO = self.font.render('O', True, (255, 255, 255))

        # Display the text on the screen
        self.game.screen.blit(text, (48*scale_factor_x,height-95*scale_factor_y))
        self.game.screen.blit(nextText, (48*scale_factor_x,250*scale_factor_y))
        self.game.screen.blit(title, (500*scale_factor_x,25*scale_factor_y))

        self.game.screen.blit(titleB, (245*scale_factor_x,85*scale_factor_y))
        self.game.screen.blit(titleI, (245*scale_factor_x,185*scale_factor_y))
        self.game.screen.blit(titleN, (245*scale_factor_x,285*scale_factor_y))
        self.game.screen.blit(titleG, (245*scale_factor_x,385*scale_factor_y))
        self.game.screen.blit(titleO, (245*scale_factor_x,485*scale_factor_y))

        # Display the currently rolled ball colour image and the BINGO letter and Number of that ball
        self.game.screen.blit(currentRoll, (75*scale_factor_x,80*scale_factor_y))
        self.font = pygame.font.SysFont('Verdana',int(35*(scale_factor_x+scale_factor_y)/2))
        next = self.font.render(nextStatement, True, nextColour)
        self.game.screen.blit(next, (80*scale_factor_x,100*scale_factor_y))

# Function that is a child of the Scene Class to make the Rules Page of the Application
class RulesScene(Scene):
    def __init__(self, game):
        super().__init__(game)

    # Handles Events for the rules scene
    def handle_events(self, events):
        for event in events:

            # Gets the current height and width of the window
            width = screen1.get_width()
            height = screen1.get_height()
            
            # Sets the scale factors based on the current size of the screen and the inital size
            global scale_factor_x, scale_factor_y, currentTurn, webbrowser
            scale_factor_x = self.game.screen.get_width() / base_screen_width
            scale_factor_y = self.game.screen.get_height() / base_screen_height

            # Gets the position of the mouse
            mouse = pygame.mouse.get_pos()

            # Based on the events and the locaton / other event decide what to do
            if event.type == pygame.KEYDOWN:
                # If the escape key is pressed go the the main menu
                if event.key == pygame.K_ESCAPE:
                    self.game.change_scene(MenuScene(self.game))

            # If the mouse is clicked on the main menu button go to the main menu scene
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if 45*scale_factor_x <= mouse[0] <= 185*scale_factor_x and height-100*scale_factor_y <= mouse[1] <= height-60*scale_factor_y:
                    # Go back to the main menu
                    self.game.change_scene(MenuScene(self.game))

                # If the mouse is clicked on the link to the GitHub go to the GitHub page
                elif linkRect.collidepoint(mouse):
                    webbrowser.open(r"https://github.com/NinePiece2/BingoGame")

               

    def update(self):
        pass

    # Displays the user interface of the rules scene
    def draw(self):

        # Background Colour
        self.game.screen.fill((18,18,18))

        # Gets the current height and width of the window
        width = screen1.get_width()
        height = screen1.get_height()

        # Gets the position of the mouse
        mouse = pygame.mouse.get_pos()
        
        # Helps in checking if the user is hovering something that is clickable
        hover = False

        # Sets the scale factors based on the current size of the screen and the inital size
        global scale_factor_x, scale_factor_y, linkRect
        scale_factor_x = self.game.screen.get_width() / base_screen_width
        scale_factor_y = self.game.screen.get_height() / base_screen_height

        # Main Menu Button
        if 45*scale_factor_x <= mouse[0] <= 185*scale_factor_x and height-100*scale_factor_y <= mouse[1] <= height-60*scale_factor_y:
            pygame.draw.rect(self.game.screen,color_light,[45*scale_factor_x,height-100*scale_factor_y,140*scale_factor_x,40*scale_factor_y])  
            hover = True         
        else:
            pygame.draw.rect(self.game.screen,color_dark,[45*scale_factor_x,height-100*scale_factor_y,140*scale_factor_x,40*scale_factor_y])
        
        # Sets the font size based on the scale factors for the header
        self.font = pygame.font.SysFont('Verdana',int(35*(scale_factor_x+scale_factor_y)/2))
        text = self.font.render("Rules Menu", True, (255, 255, 255))

        # Sets the font size based on the scale factors for the button option to go to the main menu
        self.font = pygame.font.SysFont('Verdana',int(24*(scale_factor_x+scale_factor_y)/2))
        menu = self.font.render("Main Menu", True, (255, 255, 255))

        # Sets the font size based on the scale factors for the rules text
        self.font = pygame.font.SysFont('Verdana',int(20*(scale_factor_x+scale_factor_y)/2))
        
        # Lines of text to display the rules
        rulesText = self.font.render('After pressing the play button on the main menu, you will be taken to the Game Menu', True, (255, 255, 255))
        rulesText2 = self.font.render('where you can click on the next turn button that shows the next ball that has been', True, (255, 255, 255))
        rulesText3 = self.font.render('randomly drawn. This is done one turn at a time until someone fills up their bingo', True, (255, 255, 255))
        rulesText4 = self.font.render('card fully and the card is check against the past draws that have been made for', True, (255, 255, 255))
        rulesText5 = self.font.render('correctness. There are 75 balls that can be drawn from 1 to 75.', True, (255, 255, 255))

        # Setup for the link to the GitHub
        link_font = pygame.font.SysFont('Verdana', int(20*(scale_factor_x+scale_factor_y)/2))
        link_color = (0, 0, 238)

        # Creates a sentence that the link could be used in
        linkSentance = self.font.render('For more information visit the GitHub Repository', True, (255, 255, 255))

        # Displays the text on the screen
        self.game.screen.blit(menu, (48*scale_factor_x,height-95*scale_factor_y))
        self.game.screen.blit(text, (10, 10))
        self.game.screen.blit(rulesText, (95*scale_factor_x, 100*scale_factor_y))
        self.game.screen.blit(rulesText2, (95*scale_factor_x, 125*scale_factor_y))
        self.game.screen.blit(rulesText3, (95*scale_factor_x, 150*scale_factor_y))
        self.game.screen.blit(rulesText4, (95*scale_factor_x, 175*scale_factor_y))
        self.game.screen.blit(rulesText5, (95*scale_factor_x, 200*scale_factor_y))
        self.game.screen.blit(linkSentance, (width - 700*scale_factor_x, height-95*scale_factor_y))

        # Display the text for the clickable link to the GitHub
        linkRect = self.game.screen.blit(link_font.render("here.", True, link_color), (width - 200*scale_factor_x, height-95*scale_factor_y))

        # Checks if the user is hovering the link to the GitHub
        if linkRect.collidepoint(mouse):
            hover = True
        
        # Changes the cursor wheather or not the user is hovering an option to select
        if hover:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND) 
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)


# Fuction created to setup the game
def gameSetup():
    global numbers
    if len(numbers) == 0:
        # Make a list of 75 integers from 1-75
        numbers = list(range(1, 76))

        # Shuffle the list
        random.shuffle(numbers)

# Function that starts the application
if __name__ == "__main__":
    game = Game()
    game.run()

