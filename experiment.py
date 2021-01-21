class Experiment:

    def __init__(self, lambdas: list):
        self.lambdas = lambdas

        self.response_time1 = []
        self.response_time2 = []

        self.failure_prob1 = []
        self.failure_prob2 = []

    def save_response_time(self, name: str):
        file = open(name, 'w')
        for i in range(len(self.lambdas)):
            file.write(str(self.lambdas[i]) + ' ' + str(self.response_time1[i]) + ' ' + str(self.response_time2[i]))
            file.write('\n')
        file.close()

    def show_failure_prob(self):
        for i in range(len(self.lambdas)):
            print(self.lambdas[i], self.failure_prob1[i], self.failure_prob2[i])

    def show(self):
        for i in range(len(self.lambdas)):
            print(self.lambdas[i], self.response_time1[i], self.response_time2[i],
                  self.failure_prob1[i], self.failure_prob2[i])

    def clear(self):
        self.response_time1.clear()
        self.response_time2.clear()
        self.failure_prob1.clear()
        self.failure_prob2.clear()
