from settings import *
import random

class Block(pg.sprite.Sprite):
    def __init__(self, tetromino, pos):
        # Pass properties of tetromino Class
        self.tetromino = tetromino
        # Change (0,0) grid to be at the offset pos, which is middle of display window
        self.pos = vec(pos) + BLOCK_POS_OFFSET
        # Change starting point of next-block info to be at the right of the display window (based of offset)
        self.next_pos = vec(pos) + NEXT_POS_OFFSET
        self.alive = True


        # Initialise from parent Tetromino class to add blocks to the sprite group
        super().__init__(tetromino.grid.sprite_group)
        # Create surface and rectangle for block
        self.image = pg.Surface([TILE_SIZE, TILE_SIZE])
        self.image.fill(TILE_BORDER_COLOUR)
        pg.draw.rect(self.image, GREEN, (1, 1, TILE_SIZE -2, TILE_SIZE -2), border_radius = 5) 
        self.rect = self.image.get_rect()

        # Visual Effect for line clear
        self.sfx_image = self.image.copy()
        # Transparency value
        self.sfx_image.set_alpha(110)
        # idk===========================================
        self.sfx_speed = random.uniform (0.2, 0.6)
        self.sfx_cycles = random.randrange(6, 8)
        self.cycle_counter = 0

    # Run the sfc until the number of cycles reaches the set number
    def sfx_duration(self):
        if self.tetromino.grid.main.animation_trigger:
            self.cycle_counter +=1 
            if self.cycle_counter > self.sfx_cycles:
                self.cycle_counter = 0
                return True

    # Makes image move upwards, rotate and slowly fade    
    def sfx(self):
        self.image = self.sfx_image
        self.pos.y -= self.sfx_speed
        self.image = pg.transform.rotate(self.image, pg.time.get_ticks() * self.sfx_speed)

    # To remove block from sprite group (for line clearing)
    def is_alive(self):
        if not self.alive:
            if not self.sfx_duration():
                self.sfx
            else:
                self.kill()


    # Rotatation of blocks by 90 degrees over pivot point
    def rotate(self,pivot_pt):
        translated = self.pos - pivot_pt
        rotated = translated.rotate(90)
        return rotated + pivot_pt



    # Used to pass over updated block positions due to gravity effect 
    def set_rect_pos(self):
        pos = [self.next_pos, self.pos][self.tetromino.current]
        # Adjust the block's position based on the offset so that it will fit the grid
        self.rect.topleft = (pos.x * TILE_SIZE + GRID_POS_OFFSET[0], pos.y * TILE_SIZE)



    def update(self):
        self.is_alive()
        self.set_rect_pos()

    # Check if blocks have is still in the grid and less than height of the display for the y-value AND
    # Check if there are other blocks in array or if block is above grid
    def collided(self,pos):
        x, y = int(pos.x), int(pos.y)
        if 0 <= x < DISPLAY_W and y < DISPLAY_H  and (
                y < 0 or not self.tetromino.grid.field_array[y][x]):
            return False
        return True


class Tetromino:
    def __init__(self, grid, current=True):
        # Pass properties of Grid Class
        self.grid = grid
        # Get different Tetromino configurations from dictionary
        self.shape = random.choice(list(TETROMINOES.keys()))
        # Create list of blocks according to the tetrominoes list position
        self.blocks = [Block(self, pos) for pos in TETROMINOES[self.shape]]
        # Landing attribute
        self.landing = False
        self.current = current
    

    def rotate(self):
        # Pivot pt always starts with 0
        pivot_pt = self.blocks[0].pos
        new_block_positions = [block.rotate(pivot_pt) for block in self.blocks]

        # Check if rotation caused collisions
        if not self.collided(new_block_positions):
            # Goes through every block that rotated and if there is no collision, assign new value to each block
            for i, block in enumerate(self.blocks):
                block.pos = new_block_positions[i]


    # Go through each block to check if any blocks has a collision
    def collided(self, block_position):
        return any(block.collided(pos) for block, pos in zip(self.blocks, block_position))



    def move(self, direction):
        move_direction = MOVE_DIRECTION[direction]
        new_block_positions = [block.pos + move_direction for block in self.blocks]

        if not self.collided(new_block_positions):
            # No collision; update the positions
            for block in self.blocks:
                block.pos += move_direction
        elif direction == 'down':
            # If it collides while moving down, mark landing
            self.landing = True
            self.grid.id_block_pos_in_array()  # Add blocks to grid
            self.grid.tetromino = Tetromino(self.grid)  # Create a new Tetromino



    def update(self):
        # Move tetromino down
        self.move(direction='down')