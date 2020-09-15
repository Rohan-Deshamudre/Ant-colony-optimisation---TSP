import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import time
from src.Ant import Ant
from src.Maze import Maze
from src.PathSpecification import PathSpecification
from src.Route import Route

# Class representing the first assignment. Finds shortest path between two points in a maze according to a specific
# path specification.
class AntColonyOptimization:

    # Constructs a new optimization object using ants.
    # @param maze the maze .
    # @param antsPerGen the amount of ants per generation.
    # @param generations the amount of generations.
    # @param Q normalization factor for the amount of dropped pheromone
    # @param evaporation the evaporation factor.
    def __init__(self, maze, ants_per_gen, generations, q, evaporation):
        self.maze = maze
        self.ants_per_gen = ants_per_gen
        self.generations = generations
        self.q = q
        self.evaporation = evaporation
        self.convergence = 2
        self.generation_shortest = []

    # Loop that starts the shortest path process
    # @param spec Specification of the route we wish to optimize
    # @return ACO optimized route
    def find_shortest_route(self, path_specification):
        if path_specification.start==path_specification.end:
            return Route(path_specification.start)
        self.maze.reset()
        new_ant = Ant(self.maze, path_specification)
        shortest = new_ant.find_route()
        for i in range (self.generations):
            routes = []
            print("gereration", str(i))
            for ant in range(self.ants_per_gen):
                # first initialize a path specification
                new_ant = Ant(self.maze, path_specification)
                route = new_ant.find_route()
                if route.size() == 0:
                    print("Ant took too many steps aco")
                else:
                    routes.append(route)
                    print("route length:", str(route.size()))
                    if route.size() < shortest.size():
                        shortest = route
            mean = 0
            if len(routes) > 0:
                # check convergence
                shortest_x = routes[0].size()
                for i in range(1, len(routes)):
                    shortest_x = min(shortest_x, routes[1].size())
                self.generation_shortest.append(shortest_x)
                check = True
                if len(self.generation_shortest) > 1:
                    if abs(self.generation_shortest[-1] - self.generation_shortest[-2]) > self.convergence:
                        check = False
                if check:
                    print("The route length converged with mean ", str(mean))
                    break
            # evaporate pheromone
            self.maze.evaporate(self.evaporation)
            # after all ants from given generation have finished, you have to update pheromones via maze
            self.maze.add_pheromone_routes(routes, self.q)

        return shortest


# Driver function for Assignment 1
if __name__ == "__main__":
    #parameters
    gen = 10
    no_gen = 10
    q = 16000
    evap = 0.1

    #construct the optimization objects
    maze = Maze.create_maze("./../data/hard maze.txt")
    spec = PathSpecification.read_coordinates("./../data/hard coordinates.txt")
    aco = AntColonyOptimization(maze, gen, no_gen, q, evap)

    #save starting time
    start_time = int(round(time.time() * 1000))

    #run optimization
    shortest_route = aco.find_shortest_route(spec)

    #print time taken
    print("Time taken: " + str((int(round(time.time() * 1000)) - start_time) / 1000.0))

    #save solution
    shortest_route.write_to_file("./../data/hard_solution.txt")

    #print route size
    print("Route size: " + str(shortest_route.size()))
