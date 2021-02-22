from dataclasses import dataclass


@dataclass
class Characteristics:
    response_time: float = 0
    response_time1: float = 0
    response_time2: float = 0

    failure_probability: float = 0
    failure_probability1: float = 0
    failure_probability2: float = 0

    avg_queue1: float = 0
    avg_queue2: float = 0

    avg_demands_on_devices: float = 0
    avg_demands_on_devices1: float = 0
    avg_demands_on_devices2: float = 0

    avg_free_devices: float = 0
    avg_free_devices_if_queues_not_empty: float = 0

    def __str__(self):
        return f"response_time = {self.response_time} \n" \
               f"response_time1 = {self.response_time1} \n" \
               f"response_time2 = {self.response_time2} \n" \
               f"failure_prob = {self.failure_probability} \n" \
               f"failure_prob1 = {self.failure_probability1} \n" \
               f"failure_prob2 = {self.failure_probability2} \n" \
               f"avg_queue1 = {self.avg_queue1} \n" \
               f"avg_queue2 = {self.avg_queue2} \n" \
               f"avg_queue1: {self.avg_queue1}\n" \
               f"avg_queue2: {self.avg_queue2}\n" \
               f"avg_demands_on_devices: {self.avg_demands_on_devices}\n" \
               f"avg_demands_on_devices1: {self.avg_demands_on_devices1}\n" \
               f"avg_demands_on_devices2: {self.avg_demands_on_devices2}\n" \
               f"avg_free_devices: {self.avg_free_devices}\n" \
               f"avg_free_devices_if_queues_not_empty: {self.avg_free_devices_if_queues_not_empty}\n"
