import numpy as np
from common.moead_utils import MoeadUtils
from common.operators import Operators
from common.population import Population
from common.individual import Individual

class OffspringGeneration:
    """
    Class used to generate offspring. It also retrains the Random Forest
    with the offspring data
    """

    def __init__(self, problem):
        """
        Class constructor
        :param problem: object of the Problem class
        """
        self.problem = problem
        self.genetic_operators = Operators(self.problem)
        self.moead_utils = MoeadUtils(self.problem)
        self.total_duplicated = np.zeros(self.problem.num_of_generations)
        self.total_entered = 0


    def create_children(self, population, neighborhoods, neighborhood_size, z, weight_vectors):
        """
        Create children and replace current individuals based on the Tchebycheff decomposition.
        :param population: current population
        :param neighborhoods: neighborhoods
        :param neighborhood_size: neighborhoods_size
        :param z: current reference point
        :return: None
        """

        child_pop = Population()
        for i in range(self.problem.num_of_individuals):
            k = np.random.randint(0, neighborhood_size)
            l = np.random.randint(0, neighborhood_size)
            while k == l:
                l = np.random.randint(0, neighborhood_size)
            pop_parent = [population.population[neighborhoods[i][k]], population.population[neighborhoods[i][l]]]

            child = self.genetic_operators.crossover_binary(pop_parent[0], pop_parent[1], population)

            self.genetic_operators.mutate_binary(child)


            self.problem.calculate_objectives(child)
            ind = Individual(directions=self.problem.directions)
            ind.objectives = child.objectives
            ind.features = child.features
            child_pop.append(ind)

            self.moead_utils.update_reference_point(child, z)

            for j in range(neighborhood_size):
                if self.moead_utils.Tchebycheff(child, weight_vectors[neighborhoods[i][j]], z) < self.moead_utils.Tchebycheff(population.population[neighborhoods[i][j]],
                                                                                     weight_vectors[neighborhoods[i][j]], z):
                    population.population[neighborhoods[i][j]] = child



