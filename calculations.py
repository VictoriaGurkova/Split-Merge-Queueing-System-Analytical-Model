from characteristics import Characteristics
from generator import get_stationary_distribution
from utils import *
from states_view import *


class Calculations:

    def __init__(self, params):
        self.params = params
        self.characters = Characteristics()

        self.x = params.devices_amount // params.fragments_amounts[0]
        self.y = params.devices_amount // params.fragments_amounts[1]

    def calculate(self):

        log_message('Состояния фрагментов на системах (не включая очереди):')
        devices_states = get_devices_states(self.x, self.y, self.params)
        print_states(devices_states, pretty_devices_state)

        log_message('\nСостояния системы вместе с очередями:')
        states = get_all_state_with_queues(devices_states, self.params.queues_capacities, self.params)
        print_states(states, pretty_state)

        distribution = get_stationary_distribution(states, self.params)

        log_message(f'Стационарное распределение P_i: {distribution}')
        log_message(f'Check sum P_i: {sum(distribution)}')

        self.calculate_characters(distribution, states)

    def calculate_characters(self, distribution, states):
        for state, state_prob in enumerate(distribution):
            log_message(f'P[{pretty_state(states[state])}] = {state_prob}')
            self.calculate_avg_queue(states, state, state_prob)
            self.calculate_avg_free_devices(states, state, state_prob)
            self.calculate_avg_free_devices_if_queues_not_empty(states, state, state_prob)
            self.calculate_avg_demands_on_devices(states, state, state_prob)
            self.calculate_failure_prob(states, state, state_prob)

        self.calculate_response_time()

    def calculate_response_time(self):
        effective_lambda1 = self.params.lambda1 * (1 - self.characters.failure_prob1)
        effective_lambda2 = self.params.lambda2 * (1 - self.characters.failure_prob2)

        queue_waiting1 = self.characters.avg_queue1 / effective_lambda1
        queue_waiting2 = self.characters.avg_queue2 / effective_lambda2

        self.calculate_response_time_solution1(queue_waiting1, queue_waiting2)
        # self.calculate_response_time_solution2(effective_lambda1, effective_lambda2)

        self.characters.response_time = (self.characters.avg_queue1 + self.characters.avg_queue2 +
                                         self.characters.avg_demands_on_devices1 +
                                         self.characters.avg_demands_on_devices2) / (
                                                    effective_lambda1 + effective_lambda2)

    def calculate_response_time_solution1(self, queue_waiting1, queue_waiting2):
        self.characters.response_time1 = queue_waiting1 + harmonic_sum(
            self.params.fragments_amounts[0]) / self.params.mu
        self.characters.response_time2 = queue_waiting2 + harmonic_sum(
            self.params.fragments_amounts[1]) / self.params.mu

    def calculate_response_time_solution2(self, effective_lambda1, effective_lambda2):
        self.characters.response_time1 = (self.characters.avg_queue1 + self.characters.avg_demands_on_devices1) / (
            effective_lambda1)
        self.characters.response_time2 = (self.characters.avg_queue2 + self.characters.avg_demands_on_devices2) / (
            effective_lambda2)

    def calculate_avg_queue(self, states, state, state_prob):
        self.characters.avg_queue1 += states[state][0][0] * state_prob
        self.characters.avg_queue2 += states[state][0][1] * state_prob

    def calculate_avg_free_devices(self, states, state, state_prob):
        self.characters.avg_free_devices += \
            (self.params.devices_amount -
             (len(states[state][1][0]) * self.params.fragments_amounts[0] +
              len(states[state][1][1]) * self.params.fragments_amounts[1])) * state_prob

    def calculate_avg_free_devices_if_queues_not_empty(self, states, state, state_prob):
        if states[state][0][0] + states[state][0][1] != 0:
            self.characters.avg_free_devices_if_queues_not_empty += \
                (self.params.devices_amount -
                 (len(states[state][1][0]) * self.params.fragments_amounts[0] +
                  len(states[state][1][1]) * self.params.fragments_amounts[1])) * state_prob

    def calculate_avg_demands_on_devices(self, states, state, state_prob):
        self.characters.avg_demands_on_devices1 += \
            (len(states[state][1][0]) * self.params.fragments_amounts[0] * state_prob) / \
            self.params.fragments_amounts[0]

        self.characters.avg_demands_on_devices2 += \
            (len(states[state][1][1]) * self.params.fragments_amounts[1] * state_prob) / \
            self.params.fragments_amounts[1]

        self.characters.avg_demands_on_devices += \
            ((len(states[state][1][0]) * self.params.fragments_amounts[0] +
              len(states[state][1][1]) * self.params.fragments_amounts[1]) * state_prob) / \
            (self.params.fragments_amounts[0] + self.params.fragments_amounts[1])

    def calculate_failure_prob(self, states, state, state_prob):
        if states[state][0][0] == self.params.queues_capacities[0]:
            self.characters.failure_prob1 += state_prob

        if states[state][0][1] == self.params.queues_capacities[1]:
            self.characters.failure_prob2 += state_prob

        if states[state][0][0] == self.params.queues_capacities[0] or \
                states[state][0][1] == self.params.queues_capacities[1]:
            self.characters.failure_prob += state_prob

    def get_norm_const(self):
        class1_prob = self.params.lambda1 / (self.params.lambda1 + self.params.lambda2)
        class2_prob = 1 - class1_prob
        queue_waiting_prob1 = class1_prob * (1 - self.characters.failure_prob1)
        queue_waiting_prob2 = class2_prob * (1 - self.characters.failure_prob2)
        return 1 / (queue_waiting_prob1 + queue_waiting_prob2)
