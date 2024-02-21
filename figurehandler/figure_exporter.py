import matplotlib.pyplot as plt
class FigureExporter():

    def export_figure(self, all_igds, type):
        abspath_figures = "/home/mbdemoraes/Github/moead/figures/"

        x_axis = [i for i in range(1,len(all_igds)+1)]
        fig = plt.figure(figsize=(10, 5), dpi=100)
        plt.plot(x_axis, all_igds)
        if type=="IGD":
            filename = abspath_figures + "igd" + ".pdf"
            plt.ylabel("IGD", weight='bold')
        elif type=="HV":
            filename = abspath_figures + "hv" + ".pdf"
            plt.ylabel("HV", weight='bold')
        plt.xlabel("Iteration", weight='bold', labelpad=15)
        plt.tight_layout()
        plt.savefig(filename)
