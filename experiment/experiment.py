# TODO: do something better
import os

import numpy as np


class Experiment:

    def __init__(self, name, k=6):
        self.k = k
        self.name = name

        self.response_time = np.random.sample((k, k))
        self.response_time1 = np.zeros((k, k))
        self.response_time2 = np.zeros((k, k))
        self.failure_prob = np.zeros((k, k))
        self.failure_prob1 = np.zeros((k, k))
        self.failure_prob2 = np.zeros((k, k))
        self.avg_queue1 = np.zeros((k, k))
        self.avg_queue2 = np.zeros((k, k))

    def save(self, dependence_param):
        self.save_response_time(dependence_param)
        self.save_failure_prob(dependence_param)
        self.save_avg_queue(dependence_param)

    def save_response_time(self, dependence_param):
        with open(f"{os.getcwd()}/output/experiment/{self.name}/response_time.txt", "w") as file:
            self.write_to_file(file, "Response time", self.response_time, dependence_param)
            self.write_to_file(file, "Response time 1", self.response_time1, dependence_param)
            self.write_to_file(file, "Response time 2", self.response_time2, dependence_param)

    def save_failure_prob(self, dependence_param):
        with open(f"{os.getcwd()}/output/experiment/{self.name}/failure_prob.txt", "w") as file:
            self.write_to_file(file, "Failure probability", self.failure_prob, dependence_param)
            self.write_to_file(file, "Failure probability 1", self.failure_prob1, dependence_param)
            self.write_to_file(file, "Failure probability 2", self.failure_prob2, dependence_param)

    def save_avg_queue(self, dependence_param):
        with open(f"{os.getcwd()}/output/experiment/{self.name}/avg_queue.txt", "w") as file:
            self.write_to_file(file, "Average queue size 1", self.avg_queue1, dependence_param)
            self.write_to_file(file, "Average queue size 2", self.avg_queue2, dependence_param)

    def write_to_file(self, file, title, data, dependence_param):
        file.write(f"==={title}\n")

        for value in dependence_param:
            file.write("%8.1f" % value)
        file.write("\n")

        for i in range(self.k):
            file.write(str(dependence_param[i]) + "\t")
            for j in range(self.k):
                file.write("|" + str(round(data[i][j], 4)) + "\t")
            file.write("\n" + "-" * 51 + "\n")

        file.write("=" * 51 + "\n\n")

    def clear(self):
        self.__init__(self.k)
