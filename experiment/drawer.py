import matplotlib.pyplot as plt
import numpy as np


class Drawer:

    def __init__(self):
        self.colors = ['tab:red', 'tab:blue', 'tab:green', 'tab:orange']

    def draw_compare_graphics(self, x, y_data, value, title, label):
        index = x.index(value)

        plt.plot(x[index], y_data[0][index], lw=1.5, color=self.colors[0])
        plt.plot(x[index], y_data[1][index], lw=1.5, color=self.colors[1])
        plt.xlabel(label["x"])
        plt.ylabel(label["y"])

        # Decorations
        plt.tick_params(axis="both", which="both", bottom=False, top=False,
                        labelbottom=True, left=False, right=False, labelleft=True)

        # Lighten borders
        plt.gca().spines["top"].set_alpha(.3)
        plt.gca().spines["bottom"].set_alpha(.3)
        plt.gca().spines["right"].set_alpha(.3)
        plt.gca().spines["left"].set_alpha(.3)

        plt.title(title, fontsize=22)
        plt.grid()
        plt.show()
