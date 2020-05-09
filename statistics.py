
class Stat:
    def __init__(self, lambdas: list):
        self.lambdas: list = lambdas

        self.response1: list = list()
        self.response2: list = list()

        self.probability_of_failure1: list = list()
        self.probability_of_failure2: list = list()

    def save_RT(self, name):
        file = open(name, 'w')
        for i in range(len(self.lambdas)):
            file.write(str(self.lambdas[i]) + ' ' + str(self.response1[i]) + ' ' + str(self.response2[i]))
            file.write('\n')
        file.close()

    def show_PF(self):
        for i in range(len(self.lambdas)):
            print(self.lambdas[i], self.probability_of_failure1[i], self.probability_of_failure2[i])

    def show(self):
        for i in range(len(self.lambdas)):
            print(self.lambdas[i], self.response1[i], self.response2[i],
                  self.probability_of_failure1[i], self.probability_of_failure2[i])

    def clear(self):
        self.response1.clear()
        self.response2.clear()
        self.probability_of_failure1.clear()
        self.probability_of_failure2.clear()