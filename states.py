import numpy as np
from scipy.linalg import expm

from data_store import PerformanceMeasures
from states_utils import *
from states_view import *

logger = logging.getLogger()


class QueueingSystem:

    def __init__(self, params):
        self.params = params
        self.data = PerformanceMeasures()

        self.x = params.devices_amount // params.fragments_amounts[0]
        self.y = params.devices_amount // params.fragments_amounts[1]

    # TODO: simplify/rewrite this
    def calculate(self):
        server_states = get_server_states(self.x, self.y, self.params)
        logger.debug("Состояния фрагментов на системах (не включая очереди):")
        for state_id, state in enumerate(server_states):
            logger.debug(f'S {state_id}= {pretty_server_state(state)}')

        states = get_all_state_with_queues(server_states, self.params.queues_capacities, self.params)

        logger.debug("\nСостояния системы вместе с очередями:")
        for state_id, state in enumerate(states):
            logger.debug(f'S{state_id} = {pretty_state(state)}')

        Q = self.create_generator(states)

        logger.debug(f'Q = {Q}')
        np.savetxt("output/Q.txt", Q, fmt='%0.0f')

        distr = expm(Q * 100000000000)[0]

        average_queue1 = 0
        average_queue2 = 0

        average_free_servers = 0
        average_free_servers_if_queues_not_empty = 0

        average_demands_on_devices1 = 0
        average_demands_on_devices2 = 0

        average_demands_on_devices = 0

        probability_of_failure = 0
        probability_of_failure1 = 0
        probability_of_failure2 = 0

        logger.debug(f'Стационарное распределение P_i: {distr}')
        for i, p_i in enumerate(distr):
            logger.debug(f'P[{pretty_state(states[i])}] = {p_i}')
            average_queue1 += states[i][0][0] * p_i
            average_queue2 += states[i][0][1] * p_i

            # м.о. числа свободных приборов в системе
            average_free_servers += \
                (self.params.devices_amount -
                 (len(states[i][1][0]) * self.params.fragments_amounts[0] +
                  len(states[i][1][1]) * self.params.fragments_amounts[1])) * p_i

            # м.о. числа свободных приборов в системе при условии,
            # что хотя бы одна очередь не пуста
            if states[i][0][0] + states[i][0][1] != 0:
                average_free_servers_if_queues_not_empty += \
                    (self.params.devices_amount -
                     (len(states[i][1][0]) * self.params.fragments_amounts[0] +
                      len(states[i][1][1]) * self.params.fragments_amounts[1])) * p_i

            # м.о. числа требований на приборах для каждого класса
            average_demands_on_devices1 += \
                (len(states[i][1][0]) * self.params.fragments_amounts[0] * p_i) / \
                self.params.fragments_amounts[0]
            average_demands_on_devices2 += \
                (len(states[i][1][1]) * self.params.fragments_amounts[1] * p_i) / \
                self.params.fragments_amounts[1]

            # м.о. числа требований на приборах для обоих классов
            average_demands_on_devices += \
                ((len(states[i][1][0]) * self.params.fragments_amounts[0] +
                  len(states[i][1][1]) * self.params.fragments_amounts[1]) * p_i) / \
                (self.params.fragments_amounts[0] + self.params.fragments_amounts[1])

            # Вероятности отказа
            if states[i][0][0] == self.params.queues_capacities[0]:
                probability_of_failure1 += p_i
            if states[i][0][1] == self.params.queues_capacities[1]:
                probability_of_failure2 += p_i
            if states[i][0][0] == self.params.queues_capacities[0] or \
                    states[i][0][1] == self.params.queues_capacities[1]:
                probability_of_failure += p_i

        logger.debug(f"Check sum P_i: {sum(distr)}")

        p_first = self.params.lambda1 / (self.params.lambda1 + self.params.lambda2)
        p_second = 1 - p_first

        self.data.demands_count1 = average_queue1
        self.data.demands_count2 = average_queue2

        effective_lambda1 = self.params.lambda1 * (1 - probability_of_failure1)
        effective_lambda2 = self.params.lambda2 * (1 - probability_of_failure2)

        queue_waiting1 = average_queue1 / effective_lambda1
        queue_waiting2 = average_queue2 / effective_lambda2

        self.data.response_time1 = (self.data.demands_count1 + average_demands_on_devices1) / (
            effective_lambda1)
        # self.data.RT1 = queue_waiting1 + harmonic_sum(self.a) / self.mu

        self.data.response_time2 = (self.data.demands_count2 + average_demands_on_devices2) / (
            effective_lambda2)
        # self.data.RT2 = queue_waiting2 + harmonic_sum(self.b) / self.mu

        queue_waiting_prob1 = p_first * (1 - probability_of_failure1)
        queue_waiting_prob2 = p_second * (1 - probability_of_failure2)
        norm_const = 1 / (queue_waiting_prob1 + queue_waiting_prob2)

        self.data.response_time = (self.data.demands_count1 + self.data.demands_count2 + average_demands_on_devices1 + average_demands_on_devices2) / (
                effective_lambda1 + effective_lambda2)

        self.data.failure_probability = probability_of_failure
        self.data.failure_probability1 = probability_of_failure1
        self.data.failure_probability2 = probability_of_failure2

    # TODO: where to move?
    def create_generator(self, states: list):
        n = len(states)
        Q = np.zeros((n, n))
        # проходим по каждому состоянию и смотрим на его смежные
        for i, current_state in enumerate(states):
            states_and_rates = get_achievable_states(self.params, current_state)
            for state, rate in states_and_rates.items():
                # текущее состояние имеет номер i,
                # смотрим на номер j смежного состояния
                j = states.index(state)
                # снова делаем += а не просто равно,
                # чтобы не перетереть результаты перехода
                Q[i, j] += rate

        for i, row in enumerate(Q):
            Q[i, i] = -sum(row)

        return Q