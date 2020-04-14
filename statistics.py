
class Stat:
    def __init__(self, lambdas1: list):
        self.lambdas1: list = lambdas1

        self.response1: list = list()
        self.response2: list = list()

        self.probability_of_failure1: list = list()
        self.probability_of_failure2: list = list()

    def show(self):
        for i in range(len(self.lambdas1)):
            print(self.lambdas1[i], self.response1[i], self.response2[i],
                  self.probability_of_failure1[i], self.probability_of_failure2[i])
