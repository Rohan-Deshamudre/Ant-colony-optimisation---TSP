import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import random
import numpy as np
from src.TSPData import TSPData


# TSP problem solver using genetic algorithms.
class GeneticAlgorithm:

    # Constructs a new 'genetic algorithm' object.
    # @param generations the amount of generations.
    # @param popSize the population size.
    def __init__(self, generations, pop_size):
        self.generations = generations
        self.pop_size = pop_size

    # Knuth-Yates shuffle, reordering a array randomly
    # @param chromosome array to shuffle.
    def shuffle(self, chromosome):
        n = len(chromosome)
        for i in range(n):
            r = i + int(random.uniform(0, 1) * (n - i))
            swap = chromosome[r]
            chromosome[r] = chromosome[i]
            chromosome[i] = swap
        return chromosome

    # Gets the total fitness of the population
    def get_total_fitness(self, tsp_data, population):
        start_to_product = tsp_data.get_start_distances()
        product_to_product = tsp_data.get_distances()
        product_to_end = tsp_data.get_end_distances()
        fitness = []

        for chromosome in population:
            steps = 0
            steps += start_to_product[chromosome[0]]
            for i in range(len(chromosome)-1):
                current = chromosome[i]
                next = chromosome[i + 1]
                steps += product_to_product[current][next]

            steps += product_to_end[chromosome[len(chromosome) - 1]] + len(chromosome)
            fitness.append(steps)

        total_fitness = sum(fitness)
        return total_fitness

    def get_fitness_ratio(self, tsp_data, chromosome, population):
        start_to_product = tsp_data.get_start_distances()
        product_to_product = tsp_data.get_distances()
        product_to_end = tsp_data.get_end_distances()

        fitness = start_to_product[chromosome[0]]
        for i in range(len(chromosome) - 1):
            frm = chromosome[i]
            to = chromosome[i + 1]
            fitness += product_to_product[frm][to]

        fitness += product_to_end[chromosome[len(chromosome) - 1]] + len(chromosome)

        fitness_ratio = fitness/self.get_total_fitness(tsp_data, population)

        return fitness_ratio

    # Gets the fittest two parents from the population for creating offspring.
    def selection(self, tsp_data, population):
        parent_one_fitness = self.get_total_fitness(tsp_data, population)
        parent_two_fitness = self.get_total_fitness(tsp_data, population)
        parent_one = None
        parent_two = None

        for chromosome in population:
            fitness_ratio = self.get_fitness_ratio(tsp_data, chromosome, population)
            if fitness_ratio < parent_one_fitness:
                parent_one_fitness = fitness_ratio
                parent_one = chromosome
            elif fitness_ratio < parent_two_fitness:
                parent_two_fitness = fitness_ratio
                parent_two = chromosome

        return [parent_one, parent_two]

    # Crossover of two candidate chromosomes.
    def crossover(self, parent_one, parent_two, pc):
        offspring_one = []
        offspring_two = []
        if np.random.uniform(0, 1) < pc:
            crossover_point = np.random.randint(0, 17)

            for i in range(crossover_point):
                offspring_one.append(parent_one[i])
                offspring_two.append(parent_two[i])

            for j in range(crossover_point, 17):
                offspring_one.append(parent_two[j])
                offspring_two.append(parent_one[j])
        else:
            offspring_one = parent_one
            offspring_two = parent_two

        return [offspring_one, offspring_two]

    # TODO: figure out probabilities
    def mutation(self, offspring_one, offspring_two, pm):

        if np.random.uniform(0, 1) < pm:
            mutation_point_one = np.random.choice(17, 2)

            offspring1_element1 = offspring_one[mutation_point_one[0]]
            offspring1_element2 = offspring_one[mutation_point_one[1]]
            offspring_one[mutation_point_one[0]] = offspring1_element2
            offspring_one[mutation_point_one[1]] = offspring1_element1

            mutation_point_two = np.random.choice(17, 2)

            offspring2_element1 = offspring_two[mutation_point_two[0]]
            offspring2_element2 = offspring_two[mutation_point_two[1]]
            offspring_two[mutation_point_two[0]] = offspring2_element2
            offspring_two[mutation_point_two[1]] = offspring2_element1

        return [offspring_one, offspring_two]

    # Gets the least fittest chromosome in the population, to be replaced with offspring.
    def get_least_fittest_index(self, tsp_data, population):
        total_fitness = self.get_total_fitness(tsp_data, population)
        # least_fittest = None
        least_fittest_fitness = 0
        for i, chromosome in enumerate(population):
            fitness_ratio = self.get_fitness_ratio(tsp_data, chromosome, population)
            if fitness_ratio > least_fittest_fitness:
                least_fittest_fitness = fitness_ratio
                least_fittest = i

        return least_fittest

    def get_fittest_offspring(self, tsp_data, population, offspring):
        fitness_offspring_one = self.get_fitness_ratio(tsp_data, offspring[0], population)
        fitness_offspring_two = self.get_fitness_ratio(tsp_data, offspring[1], population)

        if fitness_offspring_one < fitness_offspring_two:
            return offspring[0]
        else:
            return offspring[1]

    # Replaces least fittest chromosome by fittest offspring.
    def add_fittest_offspring(self, tsp_data, population, fittest):
        index_least_fittest = self.get_least_fittest_index(tsp_data, population)

        population[index_least_fittest] = fittest

        return population

    # This method should solve the TSP.
    # @param pd the TSP data.
    # @return the optimized product sequence.
    def solve_tsp(self, tsp_data):
        path = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 16, 17]
        population = []
        for i in range(self.pop_size):
            population.append(self.shuffle(path))

        stop = 0
        # TODO: while loop until convergence criteria is met
        while stop < generations:
            parents = self.selection(tsp_data, population)
            offspring = self.crossover(parents[0], parents[1], 0.7)

            offspring = self.mutation(offspring[0], offspring[1], 0.005)

            fittest = self.get_fittest_offspring(tsp_data, population, offspring)

            population = self.add_fittest_offspring(tsp_data, population, fittest)

            print(stop)
            stop += 1

        return path


# Assignment 2.b
if __name__ == "__main__":
    # parameters
    population_size = 20
    generations = 20
    persistFile = "./../data/productMatrixDist"

    # setup optimization
    tsp_data = TSPData.read_from_file(persistFile)
    ga = GeneticAlgorithm(generations, population_size)

    # run optimzation and write to file
    solution = ga.solve_tsp(tsp_data)
    tsp_data.write_action_file(solution, "./../data/TSP solution.txt")