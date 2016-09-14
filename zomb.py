"""
Student portion of Zombie Apocalypse mini-project
"""

import random
import poc_grid
import poc_queue
import poc_zombie_gui

# global constants
EMPTY = 0 
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = 5
HUMAN = 6
ZOMBIE = 7


class Apocalypse(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None, 
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        self.grid_height = grid_height
        self.grid_width = grid_width
        self.obstacle_list = obstacle_list
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if self.obstacle_list != None:
            for cell in self.obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)  
        else:
            self._human_list = []
        
    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        poc_grid.Grid.clear(self)
        self._zombie_list = []
        self._human_list = []
        
    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append((row, col))
        
    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)   
          
    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        for zombie in self._zombie_list:
            yield zombie

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append((row, col))
        
    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)
    
    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        for human in self._human_list:
            yield human
        
    def compute_distance_field(self, entity_type):
        """
        Function computes and returns a 2D distance field
        Distance at member of entity_list is zero
        Shortest paths avoid obstacles and use four-way distances
        """
        four_neighbors = poc_grid.Grid.four_neighbors
        if entity_type == HUMAN:
            entity_type = self._human_list
        if entity_type == ZOMBIE:
            entity_type = self._zombie_list
        
        visited = [[EMPTY for row in range(self.grid_width)] \
                     for col in range(self.grid_height)]
        
        distance_field = [[self.grid_width * self.grid_height \
                           for row in range(self.grid_width)] \
                            for col in range(self.grid_height)]
        
        if self.obstacle_list != None:
            for row,col in self.obstacle_list:
                visited[row][col] = FULL
                    
        
        boundary = poc_queue.Queue()
        for entity in entity_type:
            boundary.enqueue(entity)
            row,col = entity
            visited[row][col] = FULL
            distance_field[row][col] = 0
            
        while len(boundary) != 0:
            current_cell  =  boundary.dequeue()
            for row,col in four_neighbors(self,*current_cell):
                if visited[row][col] == EMPTY:
                    distance_field[row][col] = distance_field[current_cell[0]][current_cell[1]] + 1
                    visited[row][col] = FULL
                    boundary.enqueue((row,col))
                    
        return distance_field
    
    def move_humans(self, zombie_distance_field):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        for human in self._human_list:
            field = zombie_distance_field
            eight_neighbors = poc_grid.Grid.eight_neighbors
            
            #Create dictionary for referencing
            neighbor_distance = {}
            for row,col in eight_neighbors(self,*human):
                if poc_grid.Grid.is_empty(self,row,col) == True: #Checks if cell is empty and thus a valid move
                    neighbor_distance[(row,col)] = field[row][col]
            
            #Find greatest distance for current human from zombies
            max_distance = max(neighbor_distance.values())
            for key,value in neighbor_distance.items():
                if value == max_distance:
                    move_to = key
                    
            #Move Humans
            self._human_list[self._human_list.index(human)] = move_to
                
            
    
    def move_zombies(self, human_distance_field):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        for zombie in self._zombie_list:
            field = human_distance_field
            four_neighbors = poc_grid.Grid.four_neighbors
            
            #Create dictionary for referencing
            neighbor_distance = {}
            for row,col in four_neighbors(self,*zombie):
                if poc_grid.Grid.is_empty(self,row,col) == True: #Checks if cell is empty and thus a valid move
                    neighbor_distance[(row,col)] = field[row][col]
            
            #Find minimum distance for current zombie to human
            min_distance = min(neighbor_distance.values())
            for key,value in neighbor_distance.items():
                if value == min_distance:
                    move_to = key
                    
            #Move Zombie
            self._zombie_list[self._zombie_list.index(zombie)] = move_to

# Start up gui for simulation - You will need to write some code above
# before this will work without errors

poc_zombie_gui.run_gui(Apocalypse(30, 40))
#ap = Apocalypse(5,5)
#ap.move_humans(ap.compute_distance_field([(2,2)]))
#print ap.obstacle_list