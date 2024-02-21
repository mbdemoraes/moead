import copy

from common.non_dominated_sort import Non_Dominated_Sort
from common.moead_utils import MoeadUtils
import numpy as np
from common.population import Population
from common.offspring_generation import OffspringGeneration
import matplotlib.pyplot as plt

class Moead_Rfts:
    """
    Implementation of MOEA/D algorithm based on the paper
    Q. Zhang and H. Li, "MOEA/D: A Multiobjective Evolutionary Algorithm Based on Decomposition,"
    in IEEE Transactions on Evolutionary Computation, vol. 11, no. 6, pp. 712-731, Dec. 2007, doi: 10.1109/TEVC.2007.892759
    """

    def __init__(self,
                 problem,
                 num_of_neighborhoods):
        """
        Class constructor
        :param problem: object of the Problem class
        :param num_of_neighborhoods: number of neighborhoods
        """

        self.problem = problem
        self.offspring = OffspringGeneration(self.problem)
        self.utils = MoeadUtils(problem)
        self.m = len(self.problem.objectives)
        self.population = None
        self.ndsort = Non_Dominated_Sort()
        self.external_population = Population()
        self.z = None
        self.visited_external = set()
        self.num_of_neighborhoods = num_of_neighborhoods
        self.best_individuals = []
        self.best_per_iteration = []


    def run(self):
        """
        Run the MOEA/D algorithm
        :return: None
        """
        #Set the weight vectors
        weights_vectors, self.problem.num_of_individuals= self.utils.simplex_lattice_design(self.problem.num_of_individuals, self.m)

        #Number of individuals in a neighborhood
        neighborhood_size = int(np.ceil(self.problem.num_of_individuals / self.num_of_neighborhoods))


        #Neighborhood definition
        neighborhoods = self.utils.set_neighborhoods(weights_vectors, self.problem.num_of_individuals, self.m, neighborhood_size)

        #Initial population
        self.population = self.problem.create_initial_population()

        #Get the initial reference point
        self.z = self.utils.find_initial_reference_point(self.population)


        plt.ion()
        fig = plt.figure()
        for i in range(self.problem.num_of_generations):
            print("Generation = " + str(i))

            #Creates offspring and retrain the RF
            self.offspring.create_children(self.population, neighborhoods, neighborhood_size, self.z, weights_vectors)

            #Non-dominated sorting to identify the non-dominated solutions
            #on the current population
            self.ndsort.fast_nondominated_sort(self.population)
            for individual in self.population.fronts[0]:
                #avoids replacing the same individual in the external population
                if tuple(individual.features) not in self.visited_external:
                    self.visited_external.add(tuple(individual.features))
                    self.external_population.append(individual)
            #lst = []
            #lst_x = []
            #lst_y = []
            self.best_individuals = []


            #Non-dominated sorting to identify the non_dominated solutions
            #of the external population
            self.ndsort.fast_nondominated_sort(self.external_population)
            for individual in self.external_population.fronts[0]:
                new_dict = {}
                new_dict['decision_vector'] = individual.features
                new_dict['objective_functions'] = individual.objectives
                self.best_individuals.append(new_dict)
                # lst.append(individual.objectives)
                # lst_x.append(individual.objectives[0])
                # lst_y.append(individual.objectives[1])

            self.best_per_iteration.append(copy.deepcopy(self.best_individuals))
            # Plot the non-dominated solutions found so far during the optimization
            lst_x = [d['objective_functions'][0] for d in self.best_individuals]
            lst_y = [d['objective_functions'][1] for d in self.best_individuals]
            plt.scatter(lst_x, lst_y, marker='o', color='#0139DD', s=17)
            plt.title("Non-dominated solutions found so far")
            plt.xlabel('f1 (max)')
            plt.ylabel('f2 (max)')
            plt.show()
            plt.draw()
            plt.pause(0.003)
            plt.clf()

        plt.close()

        return self.best_individuals,self.best_per_iteration


