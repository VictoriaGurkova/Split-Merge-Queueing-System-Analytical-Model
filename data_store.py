class Data:

    def __init__(self):
        # м.о. длит. пребывания (общее)
        self.RT = None
        # м.о. длит. пребывания треб. 1-класса
        self.RT1 = None
        # м.о. длит. пребывания треб. 2-класса
        self.RT2 = None
        # вероятность отказа (общаяя)
        self.PF = None
        # вероятность отказа треб. 1-класса
        self.PF1 = None
        # вероятность отказа треб. 2-класса
        self.PF2 = None
        # м.о. числа треб. очереди 1-класса
        self.Q1 = None
        # м.о. числа треб. очереди 2-класса
        self.Q2 = None

    def print_data(self):
        print("RT =", self.RT)
        print("RT1 =", self.RT1)
        print("RT2 =", self.RT2)

        print()

        print("PF =", self.PF)
        print("PF1 =", self.PF1)
        print("PF2 =", self.PF2)

        print()

        print("Q1 =", self.Q1)
        print("Q2 =", self.Q2)
