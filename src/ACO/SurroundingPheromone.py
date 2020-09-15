import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from src.Direction import Direction
from random import uniform
from math import floor

# Class containing the pheromone information around a certain point in the maze
class SurroundingPheromone:

    # Creates a surrounding pheromone object.
    # @param north the amount of pheromone in the north.
    # @param east the amount of pheromone in the east.
    # @param south the amount of pheromone in the south.
    # @param west the amount of pheromone in the west.
    def __init__(self, north, east, south, west):
        self.north = north
        self.south = south
        self.west = west
        self.east = east
        self.total_surrounding_pheromone = east + north + south + west

    # Get the total amount of surrouning pheromone.
    # @return total surrounding pheromone
    def get_total_surrounding_pheromone(self):
        return self.total_surrounding_pheromone

    # Get a specific pheromone level
    # @param dir Direction of pheromone
    # @return Pheromone of dir
    def get(self, dir):
        if dir == Direction.north:
            return self.north
        elif dir == Direction.east:
            return self.east
        elif dir == Direction.west:
            return self.west
        elif dir == Direction.south:
            return self.south
        else:
            return None

    #check if direction is a wall
    def check_wall(self, direction):
        if direction == 0:
            return True

    def get_number_of_walls(self):
        num = 0
        dir_array = [self.east, self.west, self.north, self.south]
        for i in dir_array:
            if self.check_wall(i):
                num+=1
        return num

    def append_set(self, dir, value, highest, highest_dir):
        if value > highest:
            highest = value
            highest_dir = [dir]
        elif value == highest:
            highest_dir.append(dir)
        return highest, highest_dir

    def get_highest_pheromone(self):
        highest = self.north
        highest_dir = [Direction.north]
        highest, highest_dir = self.append_set(Direction.east, self.east, highest, highest_dir)
        highest, highest_dir = self.append_set(Direction.west, self.west, highest, highest_dir)
        highest, highest_dir = self.append_set(Direction.south, self.south, highest, highest_dir)
        if len(highest_dir) == 1:
            return highest_dir[0]
        else:
            random_value = (int(floor(uniform(0, len(highest_dir)))))
            if random_value == len(highest_dir):
                return highest_dir[random_value - 1]
            return highest_dir[random_value]
