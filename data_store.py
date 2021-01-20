class PerformanceMeasures:

    def __init__(self):
        self.response_time = None
        self.response_time1 = None
        self.response_time2 = None
        self.failure_prob = None
        self.failure_prob1 = None
        self.failure_prob2 = None
        self.demands_count1 = None
        self.demands_count2 = None

    def __str__(self):
        return f"RT = {self.response_time} \n"\
               f"RT1 = {self.response_time1} \n" \
               f"RT2 = {self.response_time2} \n" \
               f"FP = {self.failure_prob} \n" \
               f"FP1 = {self.failure_prob1} \n" \
               f"FP2 = {self.failure_prob2} \n" \
               f"Q1 = {self.demands_count1} \n" \
               f"Q2 = {self.demands_count2} \n"
