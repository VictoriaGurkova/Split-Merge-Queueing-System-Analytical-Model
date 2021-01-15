class PerformanceMeasures:

    def __init__(self):
        # м.о. длит. пребывания (общее)
        self.RT = None
        # м.о. длит. пребывания треб. 1-класса
        self.RT1 = None
        # м.о. длит. пребывания треб. 2-класса
        self.RT2 = None
        # вероятность отказа (общая)
        self.FP = None
        # вероятность отказа треб. 1-класса
        self.FP1 = None
        # вероятность отказа треб. 2-класса
        self.FP2 = None
        # м.о. числа треб. очереди 1-класса
        self.Q1 = None
        # м.о. числа треб. очереди 2-класса
        self.Q2 = None

    def __str__(self):
        return f"RT = {self.RT} \n"\
               f"RT1 = {self.RT1} \n" \
               f"RT2 = {self.RT2} \n" \
               f"FP = {self.FP} \n" \
               f"FP1 = {self.FP1} \n" \
               f"FP2 = {self.FP2} \n" \
               f"Q1 = {self.Q1} \n" \
               f"Q2 = {self.Q2} \n"
