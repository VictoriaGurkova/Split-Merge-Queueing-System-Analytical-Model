class Characteristics:

    def __init__(self):
        self.response_time = 0
        self.response_time1 = 0
        self.response_time2 = 0
        self.failure_prob = 0
        self.failure_prob1 = 0
        self.failure_prob2 = 0

        self.avg_queue1 = 0
        self.avg_queue2 = 0
        self.avg_demands_on_devices = 0
        self.avg_demands_on_devices1 = 0
        self.avg_demands_on_devices2 = 0
        self.avg_free_devices = 0
        self.avg_free_devices_if_queues_not_empty = 0

    def show_all(self):
        print(f"response_time: {self.response_time}\n"
              f"response_time1: {self.response_time1}\n"
              f"response_time2: {self.response_time2}\n"
              f"failure_prob: {self.failure_prob}\n"
              f"failure_prob1: {self.failure_prob1}\n"
              f"failure_prob2: {self.failure_prob2}\n"
              f"avg_queue1: {self.avg_queue1}\n"
              f"avg_queue2: {self.avg_queue2}\n"
              f"avg_demands_on_devices: {self.avg_demands_on_devices}\n"
              f"avg_demands_on_devices1: {self.avg_demands_on_devices1}\n"
              f"avg_demands_on_devices2: {self.avg_demands_on_devices2}\n"
              f"avg_free_devices: {self.avg_free_devices}\n"
              f"avg_free_devices_if_queues_not_empty: {self.avg_free_devices_if_queues_not_empty}\n")

    def __str__(self):
        return f"response_time = {self.response_time} \n" \
               f"response_time1 = {self.response_time1} \n" \
               f"response_time2 = {self.response_time2} \n" \
               f"failure_prob = {self.failure_prob} \n" \
               f"failure_prob1 = {self.failure_prob1} \n" \
               f"failure_prob2 = {self.failure_prob2} \n" \
               f"avg_queue1 = {self.avg_queue1} \n" \
               f"avg_queue2 = {self.avg_queue2} \n"

