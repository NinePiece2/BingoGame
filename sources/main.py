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
import shutil
from sys import exit

#import pyautogui
#from pyscreeze import pixel

screen1 = pygame.display.set_mode((1000, 600), pygame.RESIZABLE)
numbers = []
currentTurn = 0
configFolder='settings'
configFile='settings/config.ini'
savesFolder='saves'
framerate = 60

base_screen_width = 1000
base_screen_height = 600

scale_factor_x = 1
scale_factor_y = 1

#Check if the configFile and saves folder exists, if it doesn't make the config file
if not os.path.exists(configFolder):
    os.makedirs(configFolder)
if not os.path.exists(savesFolder):
    os.makedirs(savesFolder)
if not os.path.exists("sources/resources/"):
    os.makedirs("sources/resources/")
    shutil.copy("bingo_icon.svg", "sources/resources/")
    shutil.copy("bingo_icon.ico", "sources/resources/")

    

def configFileExists():
    try:
        with open(configFile, 'r') as f:
            return True
    except:
        return False

if configFileExists() == False:
    with open(configFile, 'w') as f:
        f.write('')


#Check if the configFile is empty
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
        

# Create the Tkinter root window
root = Tk()
root.withdraw()  # Hide the root window

# Font
#smallfont = pygame.font.SysFont('Verdana',35)

# light shade of the button
color_light = (42,42,42) # Grey

# dark shade of the button
color_dark = (76,175,80) # Green

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1000, 600), pygame.RESIZABLE)

        # print(self.screen.get_width())

        # Setting the name and logo of the window
        pygame.display.set_caption('BINGO')
        Icon = pygame.image.load('sources/resources/bingo_icon.svg')
        pygame.display.set_icon(Icon)
        self.clock = pygame.time.Clock()
        self.scenes = []
        self.current_scene = None


    def run(self):
        self.scenes.append(MenuScene(self))
        self.scenes.append(GameScene(self))
        self.current_scene = self.scenes[0]

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


class Scene:
    def __init__(self, game):
        self.game = game

    def handle_events(self, events):
        pass

    def update(self):
        pass

    def draw(self):
        pass

class MenuScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        #self.font = pygame.font.Font(None, 36)
        self.font = pygame.font.SysFont('Verdana',int(35*(scale_factor_x+scale_factor_y)/2))

    def handle_events(self, events):
        for event in events:
            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_SPACE:
            #         self.game.change_scene(GameScene(self.game))

            width = screen1.get_width()
            height = screen1.get_height()
            
            global scale_factor_x, scale_factor_y
            scale_factor_x = self.game.screen.get_width() / base_screen_width
            scale_factor_y = self.game.screen.get_height() / base_screen_height

            mouse = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if width/2-70*scale_factor_x <= mouse[0] <= width/2+70*scale_factor_x and height/2-80*scale_factor_y <= mouse[1] <= height/2-40*scale_factor_y:
                    self.game.change_scene(GameScene(self.game))
                    #gameSetup()
                elif width/2-70*scale_factor_x <= mouse[0] <= width/2+70*scale_factor_x and height/2+40*scale_factor_y <= mouse[1] <= height/2+80*scale_factor_y:
                    pygame.quit()
                    exit()
                elif width - 150*scale_factor_x <= mouse[0] <= width - 10*scale_factor_x and 20*scale_factor_y <= mouse[1] <= 60*scale_factor_y:
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

                


    def draw(self):
        width = screen1.get_width()
        height = screen1.get_height()
        mouse = pygame.mouse.get_pos()

        global scale_factor_x, scale_factor_y
        scale_factor_x = self.game.screen.get_width() / base_screen_width
        scale_factor_y = self.game.screen.get_height() / base_screen_height

        self.font = pygame.font.SysFont('Verdana',int(35*(scale_factor_x+scale_factor_y)/2))

        self.game.screen.fill((18,18,18))
               
        if width/2-70*scale_factor_x <= mouse[0] <= width/2+70*scale_factor_x and height/2-20*scale_factor_y <= mouse[1] <= height/2+20*scale_factor_y:
            pygame.draw.rect(self.game.screen,color_light,[width/2-70*scale_factor_x,height/2-20*scale_factor_y,140*scale_factor_x,40*scale_factor_y])           
        else:
            pygame.draw.rect(self.game.screen,color_dark,[width/2-70*scale_factor_x,height/2-20*scale_factor_y,140*scale_factor_x,40*scale_factor_y])

        if width/2-70*scale_factor_x <= mouse[0] <= width/2+70*scale_factor_x and height/2-80*scale_factor_y <= mouse[1] <= height/2-40*scale_factor_y:
            pygame.draw.rect(self.game.screen,color_light,[width/2-70*scale_factor_x,height/2-80*scale_factor_y,140*scale_factor_x,40*scale_factor_y])
        else:
            pygame.draw.rect(self.game.screen,color_dark,[width/2-70*scale_factor_x,height/2-80*scale_factor_y,140*scale_factor_x,40*scale_factor_y])

        if width/2-70*scale_factor_x <= mouse[0] <= width/2+70*scale_factor_x and height/2+40*scale_factor_y <= mouse[1] <= height/2+80*scale_factor_y:
            pygame.draw.rect(self.game.screen,color_light,[width/2-70*scale_factor_x,height/2+40*scale_factor_y,140*scale_factor_x,40*scale_factor_y])
        else: 
            pygame.draw.rect(self.game.screen,color_dark,[width/2-70*scale_factor_x,height/2+40*scale_factor_y,140*scale_factor_x,40*scale_factor_y])

        if width - 150*scale_factor_x <= mouse[0] <= width - 10*scale_factor_x and 20*scale_factor_y <= mouse[1] <= 60*scale_factor_y:
            pygame.draw.rect(self.game.screen,color_light,[width - 150*scale_factor_x,20*scale_factor_y,140*scale_factor_x,40*scale_factor_y])
        else: 
            pygame.draw.rect(self.game.screen,color_dark,[width - 150*scale_factor_x,20*scale_factor_y,140*scale_factor_x,40*scale_factor_y])

        if width - 150*scale_factor_x <= mouse[0] <= width - 10*scale_factor_x and 80*scale_factor_y <= mouse[1] <= 120*scale_factor_y:
            pygame.draw.rect(self.game.screen,color_light,[width - 150*scale_factor_x,80*scale_factor_y,140*scale_factor_x,40*scale_factor_y])
        else: 
            pygame.draw.rect(self.game.screen,color_dark,[width - 150*scale_factor_x,80*scale_factor_y,140*scale_factor_x,40*scale_factor_y])
        

        exitText = self.font.render('EXIT', True, (255, 255, 255))
        playText = self.font.render('PLAY', True, (255, 255, 255))
        rulesText = self.font.render('RULES', True, (255, 255, 255))
        loadSaveText = self.font.render('LOAD', True, (255, 255, 255))
        saveText = self.font.render('SAVE', True, (255, 255, 255))
        text = self.font.render("Main Menu", True, (255, 255, 255))

        self.game.screen.blit(exitText, (width/2-39*scale_factor_x,height/2+36*scale_factor_y))
        self.game.screen.blit(playText, (width/2-39*scale_factor_x,height/2-84*scale_factor_y))
        self.game.screen.blit(rulesText, (width/2-56*scale_factor_x,height/2-23*scale_factor_y))
        self.game.screen.blit(text, (10, 10))
        self.game.screen.blit(loadSaveText, (width-127*scale_factor_x, 17*scale_factor_y))
        self.game.screen.blit(saveText, (width-127*scale_factor_x, 77*scale_factor_y))

class GameScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.player_x = 100
        self.player_y = 100

        gameSetup()

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.change_scene(MenuScene(self.game))
                elif event.key == pygame.K_LEFT:
                    self.player_x -= 10
                elif event.key == pygame.K_RIGHT:
                    self.player_x += 10
                elif event.key == pygame.K_UP:
                    self.player_y -= 10
                elif event.key == pygame.K_DOWN:
                    self.player_y += 10

    def update(self):
        pass

    def draw(self):
        self.game.screen.fill((255, 255, 255))
        pygame.draw.rect(self.game.screen, (255, 0, 0), (self.player_x, self.player_y, 50, 50))


def gameSetup():
    global numbers
    if len(numbers) == 0:
        # Make a list of 75 integers from 1-75
        numbers = list(range(1, 76))
        print (numbers)
        # Shuffle the list
        random.shuffle(numbers)
        print (numbers)
        # Set the length of the list to 75
        numbers = numbers[:75]
    print (numbers)
    print('')


if __name__ == "__main__":
    game = Game()
    game.run()

