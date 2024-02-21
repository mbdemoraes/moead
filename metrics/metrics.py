from pymoo.indicators.igd import IGD
from pymoo.indicators.hv import HV
import pandas as pd
import numpy as np
from pymoo.config import Config
Config.warnings['not_compiled'] = False

class Metrics:

    def calc_igd(self, num_of_variables, num_of_objectives, num_of_generations):
        abspath = "/home/mbdemoraes/Github/moead/refsets/"
        filename = abspath + "ref_set_bin_mucop_" + str(num_of_variables) + ".csv"
        df = pd.read_csv(filename)
        ref_objective_functions = df.iloc[:, -num_of_objectives:].values
        all_igds = []
        ind = IGD(ref_objective_functions)
        for i in range(1,num_of_generations+1):
            abspath_results = "/home/mbdemoraes/Github/moead/results/"
            results_filename = abspath_results + "results_gen_" + str(i)
            df_gen = pd.read_csv(results_filename)
            results_objective_functions = df_gen.iloc[:, -num_of_objectives:].values
            all_igds.append(ind(results_objective_functions))

        print("IGD values (per generation): " + str(all_igds))
        return all_igds

    def calc_hv(self, num_of_variables, num_of_objectives, num_of_generations):
        ref_point = np.array([1.0, 1.0])

        ind = HV(ref_point=ref_point)
        all_hvs = []
        for i in range(1, num_of_generations + 1):
            abspath_results = "/home/mbdemoraes/Github/moead/results/"
            results_filename = abspath_results + "results_gen_" + str(i)
            df_gen = pd.read_csv(results_filename)
            results_objective_functions = df_gen.iloc[:, -num_of_objectives:].values
            results_objective_functions = results_objective_functions * -1
            all_hvs.append(ind(results_objective_functions))
        print("HV values (per generation): " + str(all_hvs))
        return all_hvs
