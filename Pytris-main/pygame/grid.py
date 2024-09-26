from settings import *
import math # Might be redundant
from tetromino import Tetromino
import pygame.freetype as ft

class Text:
    def __init__(self,main):
        self.main = main
        self.font = ft.Font(FONT_PATH)

    # Texts on display screen
    def draw(self):
        self.font.render_to(self.main.screen, (WINDOW_W * 0.05 , WINDOW_H * 0.02),
                           text='PYTRIS', fgcolor=ORANGE,
                           size=TILE_SIZE * 1.65)
        
        self.font.render_to(self.main.screen, (WINDOW_W * 0.765, WINDOW_H * 0.22),
                            text='NEXT', fgcolor=BLUE,
                            size=TILE_SIZE * 1.4)
        
        self.font.render_to(self.main.screen, (WINDOW_W * 0.75, WINDOW_H * 0.67),
                           text='SCORE', fgcolor=PINK,
                           size=TILE_SIZE * 1.4)
        
        self.font.render_to(self.main.screen, (WINDOW_W * 0.785, WINDOW_H * 0.8),
                           text=f'{self.main.grid.score}', fgcolor=PURPLE,
                           size=TILE_SIZE * 1.4, bgcolor=BLACK)
        

class Grid:
    def __init__ (self, main):
        # Pass properties of Main Class
        self.main = main
        self.sprite_group = pg.sprite.Group()
        self.field_array = self.grid_field_array()
        # Create instance of Tetromino Class
        self.tetromino = Tetromino(self)
        self.next_tetromino = Tetromino(self, current=False)

        # Score dictionary based off cleared lines
        self.score = 0
        self.full_lines = 0
        self.points_per_lines = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500, 5: 3100, 6: 6300}


    # Add to score depending on the numebr of lines cleared
    def get_score(self):
        if self.full_lines > 0:
            self.score += self.points_per_lines[self.full_lines]
            self.full_lines = 0

    def check_full_lines(self):
        row = DISPLAY_H - 1  # Start from the bottom of the grid
        cleared_lines = 0  # Count of cleared lines

        for y in range(DISPLAY_H - 1, -1, -1):  # Loop from bottom to top
            # Check if the current row is full
            if all(self.field_array[y][x] is not None for x in range(DISPLAY_W)):
                # Clear the full row and mark blocks as dead
                for x in range(DISPLAY_W):
                    if self.field_array[y][x]:  # If a block exists
                        self.field_array[y][x].alive = False  # Optional: mark as dead
                        self.field_array[y][x] = None  # Clear the block

                cleared_lines += 1  # Increment cleared lines count

            else:
                # Move non-full lines down to the cleared row
                for x in range(DISPLAY_W):
                    if self.field_array[y][x] is not None:
                        # Move the block down and update its position
                        self.field_array[row][x] = self.field_array[y][x]
                        self.field_array[row][x].pos = vec(x, row)
                    else:
                        self.field_array[row][x] = None  # Clear the space if no block

                row -= 1  # Move down to the next row

        # Clear remaining rows above the last filled row
        for r in range(row + 1):
            for x in range(DISPLAY_W):
                self.field_array[r][x] = None  # Set empty rows to None

        # Update score based on cleared lines
        if cleared_lines > 0:
            self.full_lines += cleared_lines
            self.get_score()

    # store positions of blocks in the array
    def id_block_pos_in_array(self):
        for block in self.tetromino.blocks:
            x, y = int(block.pos.x), int(block.pos.y)
        # Ensure x and y are within grid boundaries before placing the block
            if 0 <= x < DISPLAY_W and 0 <= y < DISPLAY_H:
                self.field_array[y][x] = block



    # assign 0's to every tile in the 20 x 10 grid
    def grid_field_array(self):
        return [[None for x in range(DISPLAY_W)] for y in range(DISPLAY_H)]


    
    # Check if tetromino exceeds the height of the grid which is a y value of 0
    def game_over(self):
    # Check if any block of the tetromino is at or above the top of the grid (y <= 0)
        for block in self.tetromino.blocks:
            if block.pos.y <= BLOCK_POS_OFFSET[1]:
                pg.time.wait(200)
                return True
        return False

    # Create next tetromino if the previous one has landed
    def check_tetromino_landing(self):
        if self.tetromino.landing:
            # Only check if tetromino is above y value of 0 when the block has landed/ collided
            if self.game_over():
                self.__init__(self.main)
            else:
                self.id_block_pos_in_array()
                # Once it lands
                self.next_tetromino.current = True
                # Change the next tetromino to the current one
                self.tetromino = self.next_tetromino
                # Create new tetromino for the next one
                self.next_tetromino = Tetromino(self, current=False)


    # Player key press controls
    def control(self,pressed_key):
        if pressed_key == pg.K_LEFT:
            self.tetromino.move(direction='left')
        elif pressed_key == pg.K_RIGHT:
            self.tetromino.move(direction='right')
        # Move down two tiles every arrow down
        elif pressed_key == pg.K_DOWN:
            self.tetromino.move(direction='down')
            self.tetromino.move(direction='down')
        elif pressed_key == pg.K_UP:
            self.tetromino.rotate()

    # Draws the borders of the grid for every tile
    def draw_grid(self):
        for x in range(DISPLAY_W):
            for y in range(DISPLAY_H):
                pg.draw.rect(self.main.screen, CREAM,
                             ((x * TILE_SIZE + GRID_POS_OFFSET[0]), (y * TILE_SIZE), TILE_SIZE, TILE_SIZE), 1, border_radius = 2)


    def update(self):
        # Check if there is user event caused animation
        if self.main.animation_trigger:
            self.check_full_lines()
            self.tetromino.update()
            self.check_tetromino_landing()
            self.get_score()
        self.sprite_group.update()

    def draw(self):
        self.draw_grid()
        self.sprite_group.draw(self.main.screen)