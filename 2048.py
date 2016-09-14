"""
Clone of 2048 game.
"""

import poc_2048_gui
import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
    setup_line = line[:]
    new_line = []
    for num in setup_line:
        if num == 0:
            setup_line.remove(0)
            setup_line.append(0)
            
    setup_line.append(0)
    setup_line.append(0)
    setup_line.append(0)
    setup_line.append(0)
    
    for itr in range(len(line)):
        if setup_line[0] == setup_line[1] and setup_line[0] != 0:
            new_line.append(setup_line[0] * 2)
            setup_line.remove(setup_line[0])
            setup_line.remove(setup_line[0])
        else:
            new_line.append(setup_line[0])
            setup_line.remove(setup_line[0])
    new_line.append(0)
    
    for itr in range(len(new_line)):
        for num in new_line[len(line):]:
            if num == 0:
                new_line.remove(0)
    
    return new_line

class TwentyFortyEight(object):
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        self.height = grid_height
        self.width = grid_width
        self.board = [[0 for i in range(self.width)]
                      for i in range(self.height)]

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        self.board = [[0 for i in range(self.width)]
                      for i in range(self.height)]
        self.new_tile()
        self.new_tile()

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        return str(self.board)

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self.height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self.width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        direc = list(OFFSETS[direction])
        line = []
        dummy_board = self.board[:]
        if  direction == 3:
            for i in range(self.height):
                self.board[i] = merge(self.board[i])
            self.compare(dummy_board)
            return self.board
        
        elif direction == 4:
            for i in range(self.height):
                line = self.board[i][::-1]
                self.board[i] = merge(line)
                self.board[i] = self.board[i][::-1]
            self.compare(dummy_board)
            return self.board
        
        
        elif direction == 1 or 2:
            dummy_board = str(self.board[:])
            if direction == 1:
                tile = [0,0]
            elif direction == 2:
                tile = [self.height - 1, 0]
            for i in range(self.width):
                tile2 = tile[:]
                while len(line) < self.height:
                    line.append(self.get_tile(*tile2))
                    tile2 = [x+y for x,y in zip(direc, tile2)]
                line = merge(line)
                tile2 = tile[:]
                for i in range(self.height):
                    self.set_tile(*(tile2+[line[0]]))
                    line.remove(line[0])
                    tile2 = [x+y for x,y in zip(direc, tile2)]
                tile = [x+y for x,y in zip(tile, [0,1])]
            if dummy_board != self.__str__():
                self.new_tile()
            return self.board
        
    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        rand_x = random.randrange(self.width)
        rand_y = random.randrange(self.height)
        while self.get_tile(rand_y, rand_x) != 0:
            rand_x = random.randrange(self.width)
            rand_y = random.randrange(self.height)
        value = random.choice([2,2,2,2,2,2,2,2,2,4])
        del self.board[rand_y][rand_x]
        self.board[rand_y].insert(rand_x,value)
        return self.board
        
    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        del self.board[row][col]
        self.board[row].insert(col,value)
        return self.board

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        value = self.board[row][col]
        return value
    
    def compare(self, dummy):
        """
        See if the dummy input and current board are the same
        """
        equality = []
        for i in range(self.height):
            if self.board[i] != dummy[i]:
                equality.append(False)
            else:
                equality.append(True)
        if False in equality:
            self.new_tile()

poc_2048_gui.run_gui(TwentyFortyEight(4, 4))