import numpy as np

from experiment.experiment import Experiment


class IntensityDependency(Experiment):

    __NAME = "intensity"

    def __init__(self, k=20, init_value=.5, final_value=2.5):
        self.init_value = init_value
        self.final_value = final_value

        self.lambdas = list(np.linspace(init_value, final_value, k))

        super().__init__(IntensityDependency.__NAME, k)

    def save_results(self):
        super().save(self.lambdas)

    def draw_rt(self):
        x_data = {
            "values": self.lambdas,
            "label": "lambda1",
        }
        # фиксируется значение лямбды [2]
        y_data = {
            "data": {
                "values": [[rt[2] for rt in self.response_time], self.response_time[2]],
                "legend1": "Class 1",
                "legend2": "Class 2",
            },
            "label": "response time"
        }

        title = "Зависимость response time от lambda1 по классам"
        self.drawer.draw_compare_graphics(x_data, y_data, title)

    def draw_fp(self):
        x_data = {
            "values": self.lambdas,
            "label": "lambda1",
        }
        # фиксируется значение лямбды [2]
        y_data = {
            "data": {
                "values": [[fp[2] for fp in self.failure_prob], self.failure_prob[2]],
                "legend1": "Class 1",
                "legend2": "Class 2",
            },
            "label": "failure probability"
        }

        title = "Зависимость failure probability от lambda1 по классам"
        self.drawer.draw_compare_graphics(x_data, y_data, title)

