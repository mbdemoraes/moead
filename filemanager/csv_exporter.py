import csv
from pathlib import Path
import os
class CsvExporter:

    def result_to_csv(self, best_individuals, num_of_variables, num_of_objectives):
        # Get the absolute path of the project directory
        project_dir = os.path.abspath(os.path.dirname(__file__))

        # Navigate to the 'results' directory
        results_dir = os.path.join(project_dir, '..', 'results/')

        # If the 'results' directory doesn't exist, create it
        if not os.path.exists(results_dir):
            os.makedirs(results_dir)

        # Construct the absolute path of the directory inside the project
        directory_absolute_path = os.path.join(project_dir, results_dir)
        filename = directory_absolute_path + "results.csv"

        if not os.path.exists(filename):
            with open(filename, "a+") as file:
                header = ""
                for i in range(num_of_variables):
                    header += "var" + str(i) + ","

                for i in range(num_of_objectives):
                    if i==num_of_objectives-1:
                        header += "f" + str(i)
                    else:
                        header += "f" + str(i) + ","

                file.write(header + "\n")
        count = 0

        with open(filename, "a+") as file:
            for vector in best_individuals:
                decision_vector = vector['decision_vector']
                objective_functions = vector['objective_functions']
                str_vector = ','.join(map(str, decision_vector))
                str_vector += ','
                str_obj = ','.join(map(str, objective_functions))
                final_row = str_vector + str_obj
                file.write(final_row + "\n")
                count += 1