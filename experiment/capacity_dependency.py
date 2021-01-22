from experiment.experiment import Experiment


class CapacityDependency(Experiment):
    def __init__(self, init_value=5, final_value=21, step=3):
        self.name = "capacity"
        self.init_value = init_value
        self.final_value = final_value

        self.capacities = range(init_value, final_value, step)

        super().__init__(self.name, len(self.capacities))

    def save_results(self):
        super().save(self.capacities)
