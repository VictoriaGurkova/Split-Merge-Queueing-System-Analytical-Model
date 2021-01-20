from characteristics import Characteristics
from data_store import PerformanceMeasures
from generator import get_stationary_distribution
from states_utils import *
from states_view import *


class QueueingSystem:

    def __init__(self, params):
        self.params = params
        self.data = PerformanceMeasures()
        self.characters = Characteristics()

        self.x = params.devices_amount // params.fragments_amounts[0]
        self.y = params.devices_amount // params.fragments_amounts[1]

    # TODO: simplify/rewrite this
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
        self.calculate_data()

    def calculate_characters(self, distribution, states):
        for state, state_prob in enumerate(distribution):
            log_message(f'P[{pretty_state(states[state])}] = {state_prob}')
            self.calculate_avg_queue(states, state, state_prob)
            self.calculate_avg_free_devices(states, state, state_prob)
            self.calculate_avg_free_devices_if_queues_not_empty(states, state, state_prob)
            self.calculate_avg_demands_on_devices(states, state, state_prob)
            self.calculate_failure_prob(states, state, state_prob)

    def calculate_data(self):
        norm_const = self.get_norm_const()

        self.data.demands_count1 = self.characters.avg_queue1
        self.data.demands_count2 = self.characters.avg_queue2

        effective_lambda1 = self.params.lambda1 * (1 - self.characters.failure_prob1)
        effective_lambda2 = self.params.lambda2 * (1 - self.characters.failure_prob2)

        queue_waiting1 = self.characters.avg_queue1 / effective_lambda1
        queue_waiting2 = self.characters.avg_queue2 / effective_lambda2

        # solution 1
        self.data.response_time1 = queue_waiting1 + harmonic_sum(self.params.fragments_amounts[0]) / self.params.mu
        self.data.response_time2 = queue_waiting2 + harmonic_sum(self.params.fragments_amounts[1]) / self.params.mu

        # solution 2
        # self.data.response_time1 = (self.data.demands_count1 + self.characters.avg_demands_on_devices1) / (
        #     effective_lambda1)
        # self.data.response_time2 = (self.data.demands_count2 + self.characters.avg_demands_on_devices2) / (
        #     effective_lambda2)

        self.data.response_time = (self.data.demands_count1 + self.data.demands_count2 +
                                   self.characters.avg_demands_on_devices1 +
                                   self.characters.avg_demands_on_devices2) / (effective_lambda1 + effective_lambda2)

        self.data.failure_prob = self.characters.failure_prob
        self.data.failure_prob1 = self.characters.failure_prob1
        self.data.failure_prob2 = self.characters.failure_prob2

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
        # begin ???
        class1_prob = self.params.lambda1 / (self.params.lambda1 + self.params.lambda2)
        class2_prob = 1 - class1_prob
        queue_waiting_prob1 = class1_prob * (1 - self.characters.failure_prob1)
        queue_waiting_prob2 = class2_prob * (1 - self.characters.failure_prob2)
        return 1 / (queue_waiting_prob1 + queue_waiting_prob2)
        # end ???
