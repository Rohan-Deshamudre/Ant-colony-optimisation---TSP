import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import traceback
from src.Direction import Direction
from src.Coordinate import Coordinate
from src.SurroundingPheromone import SurroundingPheromone

# Class that holds all the maze data. This means the pheromones, the open and blocked tiles in the system as
# well as the starting and end coordinates.
class Maze:

    # Constructor of a maze
    # @param walls int array of tiles accessible (1) and non-accessible (0)
    # @param width width of Maze (horizontal)
    # @param length length of Maze (vertical)
    def __init__(self, walls, width, length):
        self.walls = walls
        self.length = length
        self.width = width
        self.pheromones = []
        self.initialize_pheromones()

    def get_pher(self):
        return self.pheromones

    # Initialize pheromones to a start value.
    def initialize_pheromones(self):
        self.pheromones = []
        for i in range(self.width):  # row
            self.pheromones.append([])
        for i in range(self.width):
            for j in range(self.length):
                self.pheromones[i].append(self.walls[i][j])
        return

    # Reset the maze for a new shortest path problem.
    def reset(self):
        self.initialize_pheromones()

    # Update the pheromones along a certain route according to a certain Q
    # @param r The route of the ants
    # @param Q Normalization factor for amount of dropped pheromone (int)
    # Ola did this method. It goes over the given route and updates the pheromone.
    # You shouldn't call this method, call add_pheromone_routes
    def add_pheromone_route(self, route, q):
        factor = q/route.size()
        start = route.get_start()
        path = route.get_route()
        for i in range(len(path)):
            a = path[i]
            start = start.add_direction(Direction(a))
            self.pheromones[start.get_x()][start.get_y()] += factor
        return

    # Update pheromones for a list of routes
    # @param routes A list of routes
    # @param Q Normalization factor for amount of dropped pheromone
    def add_pheromone_routes(self, routes, q):
        for r in routes:
            self.add_pheromone_route(r, q)

    # Evaporate pheromone
    # @param rho evaporation factor
    # Ola did this method.
    # It updates all cells in pheromones array. It doesn't return anything.
    def evaporate(self, rho):
        for i in range(self.width):
            for j in range(self.length):
                x = self.pheromones[i][j]
                self.pheromones[i][j] = (1-rho)*x
        return

    # Width getter
    # @return width of the maze
    def get_width(self):
        return self.width

    # Length getter
    # @return length of the maze
    def get_length(self):
        return self.length

    # Returns a the amount of pheromones on the neighbouring positions (N/S/E/W).
    # @param position The Coordinates of position to check the neighbours of.
    # @return SurroundingPheromone class with the pheromones of the neighbouring positions.
    def get_surrounding_pheromone_exclude(self, position, directions):
        integer = 0
        east, north, south, west = 0, 0, 0, 0
        dir_prev = []
        for i in directions:
            dir_prev.append(Direction.dir_to_int(i))
        pos = [position.add_direction(Direction(0)), position.add_direction(Direction(1)),
               position.add_direction(Direction(2)), position.add_direction(Direction(3))]
        if self.in_bounds(pos[0])and 0 not in dir_prev:
            east = self.get_pheromone(pos[0])
        if self.in_bounds(pos[1]) and 1 not in dir_prev:
            north = self.get_pheromone(pos[1])
        if self.in_bounds(pos[2]) and 2 not in dir_prev:
            west = self.get_pheromone(pos[2])
        if self.in_bounds(pos[3]) and 3 not in dir_prev:
            south = self.get_pheromone(pos[3])
        return SurroundingPheromone(north, east, south, west)

    # Returns a the amount of pheromones on the neighbouring positions (N/S/E/W).
    # @param position The Coordinates of position to check the neighbours of.
    # @return SurroundingPheromone class with the pheromones of the neighbouring positions.
    def get_surrounding_pheromone(self, position):
        east, north, south, west = 0, 0, 0, 0
        pos = [position.add_direction(Direction(0)), position.add_direction(Direction(1)),
               position.add_direction(Direction(2)), position.add_direction(Direction(3))]
        if self.in_bounds(pos[0]):
            east = self.get_pheromone(pos[0])
        if self.in_bounds(pos[1]):
            north = self.get_pheromone(pos[1])
        if self.in_bounds(pos[2]):
            west = self.get_pheromone(pos[2])
        if self.in_bounds(pos[3]):
            south = self.get_pheromone(pos[3])
        return SurroundingPheromone(north, east, south, west)

    def set_zero(self, position):
        self.pheromones[position.get_x()][position.get_y()] = 0

    # Pheromone getter for a specific position. If the position is not in bounds returns 0
    # @param pos Position coordinate
    # @return pheromone at point
    def get_pheromone(self, pos):
        x = self.pheromones[pos.get_x()][pos.get_y()]
        return x

    # Check whether a coordinate lies in the current maze.
    # @param position The position to be checked
    # @return Whether the position is in the current maze
    def in_bounds(self, position):
        return position.x_between(0, self.width) and position.y_between(0, self.length)

    # Representation of Maze as defined by the input file format.
    # @return String representation
    def __str__(self):
        string = ""
        string += str(self.width)
        string += " "
        string += str(self.length)
        string += " \n"
        for y in range(self.length):
            for x in range(self.width):
                string += str(self.walls[x][y])
                string += " "
            string += "\n"
        return string

    # Method that builds a mze from a file
    # @param filePath Path to the file
    # @return A maze object with pheromones initialized to 0's inaccessible and 1's accessible.
    @staticmethod
    def create_maze(file_path):
        try:
            f = open(file_path, "r")
            lines = f.read().splitlines()
            dimensions = lines[0].split(" ")
            width = int(dimensions[0])
            length = int(dimensions[1])
            
            # make the maze_layout
            maze_layout = []
            for x in range(width):
                maze_layout.append([])
            
            for y in range(length):
                line = lines[y+1].split(" ")
                for x in range(width):
                    if line[x] != "":
                        state = int(line[x])
                        maze_layout[x].append(state)
            print("Ready reading maze file " + file_path)
            return Maze(maze_layout, width, length)
        except FileNotFoundError:
            print("Error reading maze file " + file_path)
            traceback.print_exc()
            sys.exit()