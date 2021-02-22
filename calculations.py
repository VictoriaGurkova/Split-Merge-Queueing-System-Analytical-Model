from characteristics import Characteristics
from generator import get_stationary_distribution
from logs import log_network_configuration, log_message
from network_params import Params
from states_view import print_states, pretty_devices_state, pretty_state
from utils import get_devices_states, get_all_state_with_queues, harmonic_sum


class Calculations:

    def __init__(self, params: Params):
        self.params = params
        self.characters = Characteristics()

        self.x = params.servers_number // params.fragments_numbers[0]
        self.y = params.servers_number // params.fragments_numbers[1]

    def calculate(self):
        log_network_configuration(self.params)

        log_message('Fragment states on devices (not including queues):')
        devices_states = get_devices_states(self.x, self.y, self.params)
        print_states(devices_states, pretty_devices_state)

        log_message('\nSystem states along with queues:')
        states = get_all_state_with_queues(devices_states, self.params.queues_capacities, self.params)
        print_states(states, pretty_state)

        distribution = get_stationary_distribution(states, self.params)

        log_message(f'Stationary distribution P_i:\n {distribution}')
        log_message(f'Check sum P_i: {sum(distribution)}')

        self.calculate_characters(distribution, states)

    def calculate_characters(self, distribution, states):
        for state, state_probability in enumerate(distribution):
            log_message(f'P[{pretty_state(states[state])}] = {state_probability}')
            self.calculate_avg_queue(states, state, state_probability)
            self.calculate_avg_free_devices(states, state, state_probability)
            self.calculate_avg_free_devices_if_queues_not_empty(states, state, state_probability)
            self.calculate_avg_demands_on_devices(states, state, state_probability)
            self.calculate_failure_probability(states, state, state_probability)

        self.calculate_response_time()

    def calculate_response_time(self):
        effective_lambda1 = self.params.lambda1 * (1 - self.characters.failure_probability1)
        effective_lambda2 = self.params.lambda2 * (1 - self.characters.failure_probability2)

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
            self.params.fragments_numbers[0]) / self.params.mu
        self.characters.response_time2 = queue_waiting2 + harmonic_sum(
            self.params.fragments_numbers[1]) / self.params.mu

    def calculate_response_time_solution2(self, effective_lambda1, effective_lambda2):
        self.characters.response_time1 = (self.characters.avg_queue1 + self.characters.avg_demands_on_devices1) / (
            effective_lambda1)
        self.characters.response_time2 = (self.characters.avg_queue2 + self.characters.avg_demands_on_devices2) / (
            effective_lambda2)

    def calculate_avg_queue(self, states, state, state_probability):
        self.characters.avg_queue1 += states[state][0][0] * state_probability
        self.characters.avg_queue2 += states[state][0][1] * state_probability

    def calculate_avg_free_devices(self, states, state, state_probability):
        self.characters.avg_free_devices += \
            (self.params.servers_number -
             (len(states[state][1][0]) * self.params.fragments_numbers[0] +
              len(states[state][1][1]) * self.params.fragments_numbers[1])) * state_probability

    def calculate_avg_free_devices_if_queues_not_empty(self, states, state, state_probability):
        if states[state][0][0] + states[state][0][1] != 0:
            self.characters.avg_free_devices_if_queues_not_empty += \
                (self.params.servers_number -
                 (len(states[state][1][0]) * self.params.fragments_numbers[0] +
                  len(states[state][1][1]) * self.params.fragments_numbers[1])) * state_probability

    def calculate_avg_demands_on_devices(self, states, state, state_probability):
        self.characters.avg_demands_on_devices1 += \
            (len(states[state][1][0]) * self.params.fragments_numbers[0] * state_probability) / \
            self.params.fragments_numbers[0]

        self.characters.avg_demands_on_devices2 += \
            (len(states[state][1][1]) * self.params.fragments_numbers[1] * state_probability) / \
            self.params.fragments_numbers[1]

        self.characters.avg_demands_on_devices += \
            ((len(states[state][1][0]) * self.params.fragments_numbers[0] +
              len(states[state][1][1]) * self.params.fragments_numbers[1]) * state_probability) / \
            (self.params.fragments_numbers[0] + self.params.fragments_numbers[1])

    def calculate_failure_probability(self, states, state, state_probability):
        if states[state][0][0] == self.params.queues_capacities[0]:
            self.characters.failure_probability1 += state_probability

        if states[state][0][1] == self.params.queues_capacities[1]:
            self.characters.failure_probability2 += state_probability

        if states[state][0][0] == self.params.queues_capacities[0] or \
                states[state][0][1] == self.params.queues_capacities[1]:
            self.characters.failure_probability += state_probability

    def get_norm_const(self):
        class1_probability = self.params.lambda1 / (self.params.lambda1 + self.params.lambda2)
        class2_probability = 1 - class1_probability
        queue_waiting_probability1 = class1_probability * (1 - self.characters.failure_probability1)
        queue_waiting_probability2 = class2_probability * (1 - self.characters.failure_probability2)
        return 1 / (queue_waiting_probability1 + queue_waiting_probability2)
