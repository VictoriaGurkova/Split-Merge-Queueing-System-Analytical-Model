import matplotlib.pyplot as plt


class Drawer:

    def __init__(self):
        self.colors = ['tab:red', 'tab:blue', 'tab:green', 'tab:orange']

    def draw_compare_graphics(self, x_data, y_data, title):

        plt.plot(x_data["values"], y_data["data"]["values"][0], label=y_data["data"]["legend1"],
                 lw=1.5, color=self.colors[0])
        plt.plot(x_data["values"], y_data["data"]["values"][1], label=y_data["data"]["legend2"],
                 lw=1.5, color=self.colors[1])
        plt.xlabel(x_data["label"])
        plt.ylabel(y_data["label"])
        plt.legend()

        # Decorations
        plt.tick_params(axis="both", which="both", bottom=False, top=False,
                        labelbottom=True, left=False, right=False, labelleft=True)

        # Lighten borders
        plt.gca().spines["top"].set_alpha(.3)
        plt.gca().spines["bottom"].set_alpha(.3)
        plt.gca().spines["right"].set_alpha(.3)
        plt.gca().spines["left"].set_alpha(.3)

        plt.title(title, fontsize=14)
        plt.grid()
        plt.show()
