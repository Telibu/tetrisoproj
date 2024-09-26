import sys
import pygame as pg
from settings import *
from grid import Grid, Text

class Main:
    # Initialise game
    def __init__(self):
        pg.init()
        # Title
        pg.display.set_caption('PYTRIS')
        # Dispaly window resolution
        self.screen = pg.display.set_mode(WINDOW_RES)
        # Timer
        self.clock = pg.time.Clock()
        # Used for animation speed
        self.set_timer()
        # Create instance of Grid 
        self.grid = Grid(self)
        # Create instance of Text 
        self.text = Text(self)

    def set_timer(self):
        self.user_event = pg.USEREVENT + 0
        self.animation_trigger = False
        pg.time.set_timer(self.user_event, ANIMATION_TIME_INTERVAL)

    
    def update(self):
        # FPS 
        self.clock.tick(FPS)
        # Grid update
        self.grid.update()


    def draw(self):
        # Colour for Display window
        self.screen.fill(color = DISPLAY_BACKGROUND_COLOUR)
        # Colour for grid rectangle background
        self.screen.fill(color = DISPLAY_COLOUR, rect=(GRID_POS_OFFSET[0], 0, *DISPLAY_RES))
        # Grid draw
        self.grid.draw()
        self.text.draw()
        # Updates screen 
        pg.display.flip()

    # Event based
    def check_events(self):
        self.animation_trigger = False
        for event in pg.event.get():
            # Quit Game when windows 'X' key is pressed or upon escape key being pressed down
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_x):
                pg.quit()
                sys.exit()
            # Detect key press for player gameplay controls
            elif event.type == pg.KEYDOWN:
                self.grid.control(pressed_key=event.key)
            # Detect user event and pass animation trigger value 
            elif event.type == self.user_event:
                self.animation_trigger = True


    # Main game loop
    def game_loop(self):
        # Infinite loop
        while True:
            # Calling UDF
            self.check_events()
            self.update()
            self.draw()


if __name__ == "__main__":
    main = Main()
    main.game_loop()