from common.problem import Problem
from algorithms.moead import Moead_Rfts
from filemanager.csv_exporter import CsvExporter
from figurehandler.figure_exporter import FigureExporter
from metrics.metrics import Metrics
import random

"""
Contains a working example of MOEA/D-RFTS on the Binary Multi-Objective Unconstrained
Combinatorial Optimization Problem (BIN_MUCOP). Fore more information on the algorithm please refer to the paper:

M. B. De Moraes and G. P. Coelho, "A Random Forest-Assisted
Decomposition-Based Evolutionary Algorithm for Multi-Objective
Combinatorial Optimization Problems,"
2022 IEEE Congress on Evolutionary Computation (CEC), 2022,
pp. 1-8, doi: 10.1109/CEC55065.2022.9870412.

"""

#optimization parameters
num_of_variables = 50
num_of_individuals = 100
generations = 10
directions = ["max", "max"]

#Get the profit vector from the instance file
def get_profit_vector(number, num_of_variables):
    profits = []
    with open("instances/bin_mucop_" + str(num_of_variables) + "_" + str(number) + "_.txt", "rt") as f:
        for line in f:
            currentline = line.split(",")
            profits.append(int(currentline[0]))
    return profits

# Calculates the individual profit based on profit assigned
# for that particular position in that particular knapsack (given by the profits vector)
def get_individual_profit(individual, profits):
    weight, profit = 0, 0
    for (item, data) in zip(individual, profits):
        if item != 0:
            profit += data

    return profit

# F1 function: calculates the profits of an individual based on the first instance
def f1(individual):

    profits = get_profit_vector(number=0, num_of_variables=num_of_variables)
    return get_individual_profit(individual,profits)

# F2 function: calculates the profits of an individual based on the second instance
def f2(individual):
    profits = get_profit_vector(number=1, num_of_variables=num_of_variables)
    return get_individual_profit(individual,profits)



# Class to control the problem parameters
problem = Problem(num_of_variables=num_of_variables,
                  num_of_individuals=num_of_individuals,
                  objectives=[f1, f2],
                  variables_range=[0, 1],
                  mutation=(1/num_of_variables),
                  expand=False,
                  num_of_generations=generations,
                  directions=directions)

#MOEA/D-RFTS hyper-parameters
num_of_neighborhoods = 5

random.seed()

#Calls the algorithm and sets the parameters
iteration = Moead_Rfts(problem=problem,
                       num_of_neighborhoods=num_of_neighborhoods)
#Runs the optimization
best_individuals, best_per_iteration = iteration.run()
csv_handler = CsvExporter()

#Create a result file with the best individuals of each generation
for i in range(generations):
    csv_handler.result_to_csv(best_individuals=best_per_iteration[i], num_of_variables=num_of_variables, num_of_objectives=len(directions), filename='results_gen_' + str(i+1))

#Calculate the metrics of IGD and HV for each generation
metrics = Metrics()
all_igds = metrics.calc_igd(num_of_variables=num_of_variables, num_of_objectives=len(directions), num_of_generations=generations)
all_hvs = metrics.calc_hv(num_of_variables=num_of_variables, num_of_objectives=len(directions), num_of_generations=generations)

#Create figures with the results of IGD and HV
fig_exporter = FigureExporter()
fig_exporter.export_figure(all_igds, type="IGD")
fig_exporter.export_figure(all_hvs, type="HV")





