class Statistics:

    def __init__(self, lambdas: list):
        self.lambdas = lambdas

        self.response1 = []
        self.response2 = []

        self.failure_probability1 = []
        self.failure_probability2 = []

    def save_response_time(self, name: str):
        file = open(name, 'w')
        for i in range(len(self.lambdas)):
            file.write(str(self.lambdas[i]) + ' ' + str(self.response1[i]) + ' ' + str(self.response2[i]))
            file.write('\n')
        file.close()

    def show_failure_probability(self):
        for i in range(len(self.lambdas)):
            print(self.lambdas[i], self.failure_probability1[i], self.failure_probability2[i])

    def show(self):
        for i in range(len(self.lambdas)):
            print(self.lambdas[i], self.response1[i], self.response2[i],
                  self.failure_probability1[i], self.failure_probability2[i])

    def clear(self):
        self.response1.clear()
        self.response2.clear()
        self.failure_probability1.clear()
        self.failure_probability2.clear()
