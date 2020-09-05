class PerfomanceMeasures:

    def __init__(self):
        # м.о. длит. пребывания (общее)
        self.RT = None
        # м.о. длит. пребывания треб. 1-класса
        self.RT1 = None
        # м.о. длит. пребывания треб. 2-класса
        self.RT2 = None
        # вероятность отказа (общая)
        self.PF = None
        # вероятность отказа треб. 1-класса
        self.PF1 = None
        # вероятность отказа треб. 2-класса
        self.PF2 = None
        # м.о. числа треб. очереди 1-класса
        self.Q1 = None
        # м.о. числа треб. очереди 2-класса
        self.Q2 = None

    def __str__(self):
        return  f"RT = {self.RT} \n"\
                f"RT1 = {self.RT1} \n" \
                f"RT2 = {self.RT2} \n" \
                f"PF = {self.PF} \n" \
                f"PF1 = {self.PF1} \n" \
                f"PF2 = {self.PF2} \n" \
                f"Q1 = {self.Q1} \n" \
                f"Q2 = {self.Q2} \n"
