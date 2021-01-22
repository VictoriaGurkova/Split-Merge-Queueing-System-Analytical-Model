import numpy as np

from experiment.experiment import Experiment


class IntensityDependency(Experiment):

    def __init__(self, k=6, init_value=.5, final_value=2):
        self.name = "intensity"
        self.init_value = init_value
        self.final_value = final_value

        self.lambdas = list(np.linspace(init_value, final_value, k))

        super().__init__(self.name, k)

    def save_results(self):
        super().save(self.lambdas)
