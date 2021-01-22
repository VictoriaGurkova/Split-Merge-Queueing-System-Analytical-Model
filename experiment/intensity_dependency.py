import numpy as np

from experiment.experiment import Experiment


class IntensityDependency(Experiment):

    __NAME = "intensity"

    def __init__(self, k=6, init_value=.5, final_value=2):
        self.init_value = init_value
        self.final_value = final_value

        self.lambdas = list(np.linspace(init_value, final_value, k))

        super().__init__(IntensityDependency.__NAME, k)

    def save_results(self):
        super().save(self.lambdas)
