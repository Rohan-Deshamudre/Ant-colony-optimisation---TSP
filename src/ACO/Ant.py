import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import random
from src.Direction import Direction
from src.Route import Route

# Class that represents the ants functionality.
class Ant:

    # Constructor for ant taking a Maze and PathSpecification.
    # @param maze Maze the ant will be running in.
    # @param spec The path specification consisting of a start coordinate and an end coordinate.
    def __init__(self, maze, path_specification):
        self.maze = maze
        self.start = path_specification.get_start()
        self.end = path_specification.get_end()
        self.current_position = self.start
        self.maximum_loops = 100000000
        self.visited = list()

    # Method that performs a single run through the maze by the ant.
    # @return The route the ant found through the maze.
    def find_route(self):
        # list to add the visited coordinates to
        iterate = 0
        # while the ant didn't reach our destination, repeat
        while iterate < self.maximum_loops and not self.current_position == self.end:
            surrounding_pheromone = self.get_pheromone()

            # get a random value from the range representing all surrounding pheromones
            # range (0, pheromone in direction 0) represents going to direction 0
            # range (pheromone in direction 0, pheromone in direction 1) represents going to direction 1
            # etc.
            random_value = random.uniform(0, surrounding_pheromone.get_total_surrounding_pheromone())
            east = surrounding_pheromone.get(Direction(0))
            north = surrounding_pheromone.get(Direction(1))
            west = surrounding_pheromone.get(Direction(2))
            if random_value < east:
                direction = Direction(0)
            elif random_value < east+north:
                direction = Direction(1)
            elif random_value < east+north+west or surrounding_pheromone.get(Direction(3)) == 0:
                direction = Direction(2)
            else:
                direction = Direction(3)

            # add chosen direction to route, change current position in given direction
            self.visited.append(self.current_position)
            self.current_position = self.current_position.add_direction(direction)
            #print("ant position x:", str(self.current_position.get_x()), "y:", str(self.current_position.get_y()))
            iterate += 1
        if self.current_position == self.end:
            self.visited.append(self.current_position)
            route = self.create_route()
        else:
            print("Ant is not at the goal")
            route = Route(self.start)
        return route

    def get_pheromone(self):

        if len(self.visited) >= 1:

            # -1 means last element,
            # so we check whether the direction is going to the same direction as the ant came from.
            prev_pos = self.visited[-1]
            direction_back = self.current_position.coordinate_to_dir(prev_pos)
            get_visited = self.get_visited()
            # retrieve pheromone from the maze
            surrounding_pheromone = self.maze \
                .get_surrounding_pheromone_exclude(self.current_position, get_visited)

            # if dead end, go back
            if surrounding_pheromone.get_total_surrounding_pheromone() == 0:
                #print("dead end encountered")
                surrounding_pheromone = self.close_dead_end(surrounding_pheromone)
        else:
            # print("now: ",str(self.current_position.get_x()), str(self.current_position.get_y()))
            surrounding_pheromone = self.maze \
                .get_surrounding_pheromone(self.current_position)
        return surrounding_pheromone

    def get_visited(self):
        dirs = [Direction.east, Direction.north, Direction.west, Direction.south]
        dir_array = list()
        for i in dirs:
            check_pos = self.current_position.add_direction(i)
            if check_pos in self.visited:
                dir_array.append(i)
        return dir_array

    def create_route(self):
        route = Route(self.start)
        position = self.start
        # print("now: ",str(self.start.get_x()), str(self.start.get_y()))
        for i in range(1, len(self.visited)):
            # print("now: ",str(position.get_x()), str(position.get_y()))
            route.add(position.coordinate_to_dir(self.visited[i]))
            position = self.visited[i]

        return route

    def close_dead_end(self, surrounding_pheromone):
        #print("close dead end innitated: ", str(self.current_position.get_x()), str(self.current_position.get_y()))
        self.visited.append(self.current_position)
        # print(str(surrounding_pheromone.get_number_of_walls()))
        while surrounding_pheromone.get_number_of_walls() == 4:
            # print(str(surrounding_pheromone.get_number_of_walls()))
            self.one_step_back()
            surrounding_pheromone = self.maze.get_surrounding_pheromone(self.current_position)
        self.visited.pop()
        surrounding_pheromone = self.get_pheromone()
        return surrounding_pheromone

    def one_step_back(self):
        #print("step back: current pos:  (", str(self.current_position.get_x()), str(self.current_position.get_y()))
        if len(self.visited) >=2:
            #print("), prev pos", str(self.visited[-2].get_x()), str(self.visited[-2].get_y()))
            self.current_position = self.visited[-2]
            self.maze.set_zero(self.visited[-1])
            self.visited.pop()
        else:
            self.visited = list()
            self.current_position = self.start
