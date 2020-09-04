from collections import defaultdict

import numpy as np
from scipy.linalg import expm
import matplotlib.pyplot as plt
from functions import *


class StateSpace:
    def __init__(self, M, a, b, capacity1, capacity2, lambda1, lambda2, mu):
        self.M = M
        self.a = a
        self.b = b
        self.lambda1 = lambda1
        self.lambda2 = lambda2
        self.mu = mu
        self.queue_capacity = [capacity1, capacity2]

        self.x = M // a
        # print('Максимальное число требований 1го класса = ', self.x)
        self.y = M // b
        # print('Максимальное число требований 2го класса = ', self.y)

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

    def start(self):
        server_states = self.get_server_states()
        print("Состояния фрагментов на системах (не включая очереди):")
        for state_id, state in enumerate(server_states):
            print('S' + str(state_id), '= ', pretty_server_state(state))

        states = self.get_all_state_with_queues(server_states)

        print("\nСостояния системы вместе с очередями:")
        for state_id, state in enumerate(states):
            print('S' + str(state_id), '= ', pretty_state(state))

        Q = self.create_generator(states)

        print('Q = ', Q)
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

        print('Стационарное распределение P_i:', distr)
        for i, p_i in enumerate(distr):
            print('P[', pretty_state(states[i]), '] =', p_i)
            average_queue1 += states[i][0][0] * p_i
            average_queue2 += states[i][0][1] * p_i

            # м.о. числа свободных приборов в системе
            average_free_servers += \
                (self.M - (len(states[i][1][0]) * self.a +
                           len(states[i][1][1]) * self.b)) * p_i

            # м.о. числа свободных приборов в системе при условии,
            # что хотя бы одна очередь не пуста
            if states[i][0][0] + states[i][0][1] != 0:
                average_free_servers_if_queues_not_empty += \
                    (self.M - (len(states[i][1][0]) * self.a +
                               len(states[i][1][1]) * self.b)) * p_i

            # м.о. числа требований на приборах для каждого класса
            average_demands_on_devices1 += \
                (len(states[i][1][0]) * self.a * p_i) / self.a
            average_demands_on_devices2 += \
                (len(states[i][1][1]) * self.b * p_i) / self.b

            # м.о. числа требований на приборах для обоих классов
            average_demands_on_devices += \
                ((len(states[i][1][0]) * self.a +
                  len(states[i][1][1]) * self.b) * p_i) / (self.a + self.b)

            # Вероятности отказа
            if states[i][0][0] == self.queue_capacity[0]:
                probability_of_failure1 += p_i
            if states[i][0][1] == self.queue_capacity[1]:
                probability_of_failure2 += p_i
            if states[i][0][0] == self.queue_capacity[0] or \
                    states[i][0][1] == self.queue_capacity[1]:
                probability_of_failure += p_i

        print(sum(distr))

        p_first = self.lambda1 / (self.lambda1 + self.lambda2)
        p_second = 1 - p_first

        print('Expected Queue 1 = ', average_queue1)
        self.Q1 = average_queue1
        print('Expected Queue 2 = ', average_queue2)
        self.Q2 = average_queue2
        print()

        effective_lambda1 = self.lambda1 * (1 - probability_of_failure1)
        effective_lambda2 = self.lambda2 * (1 - probability_of_failure2)

        queue_waiting1 = average_queue1 / effective_lambda1
        queue_waiting2 = average_queue2 / effective_lambda2

        print('Expected Waiting Time 1 = ', queue_waiting1)
        print('Expected Waiting Time 2 = ', queue_waiting2)
        print()

        self.RT1 = queue_waiting1 + harmonic_sum(self.a) / self.mu
        self.RT2 = queue_waiting2 + harmonic_sum(self.b) / self.mu
        queue_waiting_prob1 = p_first * (1 - probability_of_failure1)
        queue_waiting_prob2 = p_second * (1 - probability_of_failure2)
        norm_const = 1 / (queue_waiting_prob1 + queue_waiting_prob2)

        self.RT = ((queue_waiting1 + harmonic_sum(self.a) / self.mu) *
                   queue_waiting_prob1
                   + (queue_waiting2 + harmonic_sum(self.b) / self.mu) *
                   queue_waiting_prob2) * norm_const

        print('Expected Response Time 1 = ', self.RT1)
        print('Expected Response Time 2 = ', self.RT2)
        print()

        print('Expected free servers = ', average_free_servers)
        print('Expected free servers if queues not empty = ',
              average_free_servers_if_queues_not_empty)
        print()

        print('Expected demands on devices 1 = ', average_demands_on_devices1)
        print('Expected demands on devices 2 = ', average_demands_on_devices2)
        print()

        print('Expected demands on devices = ', average_demands_on_devices)
        print()

        print('Expected service demand 1 = ', harmonic_sum(self.a))
        print('Expected service demand 2 = ', harmonic_sum(self.b))
        print()

        print('Probability of failure = ', probability_of_failure)
        self.PF = probability_of_failure
        print('Probability of failure 1 = ', probability_of_failure1)
        self.PF1 = probability_of_failure1
        print('Probability of failure 2 = ', probability_of_failure2)
        self.PF2 = probability_of_failure2

    def get_server_states(self):
        server_states = set()
        for i in range(self.x + 1):
            for j in range(self.y + 1):
                total_number_of_tasks = self.a * i + self.b * j
                if self.M < total_number_of_tasks:
                    continue
                X = sorted(get_lots_of_fragments(i, self.a))
                Y = sorted(get_lots_of_fragments(j, self.b))
                server_states.update(itertools.product(X, Y))
        return server_states

    def get_all_state_with_queues(self, server_states: set):
        states = []
        queue_states = set(itertools.product(range(self.queue_capacity[0] + 1),
                                             range(self.queue_capacity[1] + 1)))

        for q_state in queue_states:
            for server_state in server_states:
                if self.is_possible_state(q_state, server_state):
                    states.append((q_state, server_state))
        return states

    def is_possible_state(self, q_state, state):
        number_of_free_servers = \
            self.number_of_free_servers_for_server_state(state)
        if q_state[0] and number_of_free_servers >= self.a:
            return False
        if q_state[1] and number_of_free_servers >= self.b:
            return False
        return True

    # возвращает словарь {состояние: интенсивность перехода}
    def get_achievable_states(self, current_state: tuple):
        states_and_rates = defaultdict(float)

        print('#' * 100)
        print('Рассмотрим состояние ' + pretty_state(current_state))

        capacity1 = self.queue_capacity[0]
        capacity2 = self.queue_capacity[1]

        # получаем различные характеристики состояния
        q1 = current_state[0][0]
        print('q1 = ', q1)
        q2 = current_state[0][1]
        print('q2 = ', q2)
        server_state = current_state[1]
        print('server_state = ', server_state)

        number_of_free_servers = \
            self.number_of_free_servers_for_server_state(server_state)
        print("Число свободных приборов", number_of_free_servers)

        print("ПОСТУПЛЕНИЕ")
        if q1 != capacity1:
            if number_of_free_servers < self.a:
                new_state = create_state(q1 + 1, q2,
                                         server_state[0],
                                         server_state[1])
                print(f'Поступление требования первого класса в '
                      f'очередь с интенсивностью {self.lambda1} и '
                      f'переход в стояние ', pretty_state(new_state))
                states_and_rates[new_state] += self.lambda1
            else:
                updated_first_demands_tasks = server_state[0]
                updated_first_demands_tasks += (self.a,)
                new_state = create_state(q1, q2,
                                         updated_first_demands_tasks,
                                         server_state[1])
                print(f'Поступление требования первого класса с '
                      f'интенсивностью {self.lambda1} и '
                      f'немедленное начало его'
                      f' обслуживания и переход в состояние ',
                      pretty_state(new_state))
                states_and_rates[new_state] += self.lambda1
        else:
            print("Очередь заполнена - требование потерялось")

        if q2 != capacity2:
            if number_of_free_servers < self.b:
                new_state = create_state(q1, q2 + 1,
                                         server_state[0],
                                         server_state[1])
                print( f'Поступление требования второго класса в очередь с '
                       f'интенсивностью {self.lambda2} и '
                       f'переход в стояние ', pretty_state(new_state))
                states_and_rates[new_state] += self.lambda2
            else:
                updated_second_demands_tasks = server_state[1]
                updated_second_demands_tasks += (self.b,)
                new_state = create_state(q1, q2, server_state[0],
                                         updated_second_demands_tasks)
                print(f'Поступление требования второго класса с '
                      f'интенсивностью {self.lambda2} и '
                      f'немедленное начало его обслуживания и '
                      f'переход в состояние ', pretty_state(new_state))
                states_and_rates[new_state] += self.lambda2
        else:
            print("Очередь заполнена - требование потерялось")

        print('УХОД')
        # 1й класс
        for index, number_of_lost_tasks_in_demand in \
                enumerate(server_state[0]):
            updated_first_demands_tasks = list(server_state[0])
            updated_second_demands_tasks = list(server_state[1])
            copy_q1 = q1
            copy_q2 = q2
            copy_number_of_free_servers = number_of_free_servers
            # требование уйдет полностью, если остался один фрагмент
            if number_of_lost_tasks_in_demand == 1:
                updated_first_demands_tasks.pop(index)
                if q1:
                    while copy_number_of_free_servers + \
                            self.a >= self.a and copy_q1:
                        updated_first_demands_tasks += [self.a]
                        copy_q1 -= 1
                        copy_number_of_free_servers -= self.a
                if q2:
                    while copy_number_of_free_servers + \
                            self.a >= self.b and copy_q2:
                        updated_second_demands_tasks += [self.b]
                        copy_q2 -= 1
                        copy_number_of_free_servers -= self.b
                new_state = create_state(copy_q1, copy_q2,
                                         updated_first_demands_tasks,
                                         updated_second_demands_tasks)
                print(f'Завершение обслуживания всего требования '
                      f'первого класса с интенсивностью {self.mu}, и '
                      f'переход в состояние ', pretty_state(new_state))
                states_and_rates[new_state] += self.mu

            else:
                leave_intensity = self.mu * number_of_lost_tasks_in_demand
                updated_first_demands_tasks[index] -= 1
                new_state = create_state(q1, q2, updated_first_demands_tasks,
                                         server_state[1])
                print(f'Завершение обслуживания фрагмента '
                      f'требования первого класса с '
                      f'интенсивностью {leave_intensity}',
                      'и переход в состояние ', pretty_state(new_state))
                states_and_rates[new_state] += leave_intensity

        # 2й класс
        for index, number_of_lost_tasks_in_demand in \
                enumerate(server_state[1]):
            updated_first_demands_tasks = list(server_state[0])
            updated_second_demands_tasks = list(server_state[1])
            copy_q1 = q1
            copy_q2 = q2
            copy_number_of_free_servers = number_of_free_servers
            if number_of_lost_tasks_in_demand == 1:
                updated_second_demands_tasks.pop(index)
                if q1:
                    while copy_number_of_free_servers + self.b >= \
                            self.a and copy_q1:
                        updated_first_demands_tasks += [self.a]
                        copy_q1 -= 1
                        copy_number_of_free_servers -= self.a
                if q2:
                    while copy_number_of_free_servers + self.b >= \
                            self.b and copy_q2:
                        updated_second_demands_tasks += [self.b]
                        copy_q2 -= 1
                        copy_number_of_free_servers -= self.b
                new_state = create_state(copy_q1, copy_q2,
                                         updated_first_demands_tasks,
                                         updated_second_demands_tasks)
                print(f'Завершение обслуживания всего требования '
                      f'второго класса с интенсивностью {self.mu}',
                      'и переход в состояние ', pretty_state(new_state))
                states_and_rates[new_state] += self.mu

            else:
                leave_intensity = self.mu * number_of_lost_tasks_in_demand
                updated_second_demands_tasks[index] -= 1
                new_state = create_state(q1, q2, server_state[0],
                                         updated_second_demands_tasks)
                print(f'Завершение обслуживания фрагмента '
                      f'требования второго класса с '
                      f'интенсивностью {leave_intensity}',
                      'и переход в состояние ', pretty_state(new_state))
                states_and_rates[new_state] += leave_intensity

        return states_and_rates

    def create_generator(self, states: list):
        n = len(states)
        Q = np.zeros((n, n))
        # проходим по каждому состоянию и смотрим на его смежные
        for i, current_state in enumerate(states):
            states_and_rates = self.get_achievable_states(current_state)
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

    def number_of_free_servers_for_server_state(self, server_state):
        number = self.M - (len(server_state[0]) * self.a +
                           len(server_state[1]) * self.b)
        if number < 0:
            raise Exception("Number of free servers for states < 0, "
                            "it is not correct state")
        return number


if __name__ == '__main__':
    file = open('output/out.txt', 'w')

    _M = 4
    _a = 2
    _b = 3
    _capacity1 = 5
    _capacity2 = 5
    _lambda1 = 1
    _lambda2 = 1
    _mu = 3

    k = 6
    rt = np.zeros((k, k))
    rt1 = np.zeros((k, k))
    rt2 = np.zeros((k, k))
    pf = np.zeros((k, k))
    pf1 = np.zeros((k, k))
    pf2 = np.zeros((k, k))
    q1 = np.zeros((k, k))
    q2 = np.zeros((k, k))

    lambdas = list(np.linspace(0.5, 2, k))

    for i, lam1 in enumerate(lambdas):
        for j, lam2 in enumerate(lambdas):
            sp = StateSpace(_M, _a, _b, _capacity1, _capacity2,
                            lam1, lam2, _mu)
            sp.start()
            rt[i, j] = sp.RT
            rt1[i, j] = sp.RT1
            rt2[i, j] = sp.RT2
            pf[i, j] = sp.PF
            pf1[i, j] = sp.PF1
            pf2[i, j] = sp.PF2
            q1[i, j] = sp.Q1
            q2[i, j] = sp.Q2

    file.write('\nм.о. длительности пребывания (общее) от входящего потока')
    file.write('\nlambda2/lambda1:\n')
    for i, lam1 in enumerate(lambdas):
        for j, lam2 in enumerate(lambdas):
            s = "%8.4f" % (rt[i, j])
            file.write(s + '\t')
        file.write('\n')

    plt.plot(lambdas, rt[2], 'b')
    plt.plot(lambdas, [r[2] for r in rt], 'r')

    plt.plot(lambdas, rt[2], 'b')  # график зависимости от lambda1, lambda2 = 1.1
    plt.plot(lambdas, [r[2] for r in rt], 'r')  # график зависимости от lambda2, lambda1 = 1.1

    plt.title(f"Зависимость м.о. длит. преб. от интен. вход.")
    plt.xlabel("lambda")
    plt.ylabel("RT")
    plt.grid()
    plt.show()

    file.write('\nм.о. длительности пребывания (для 1-класса) от входящего потока')
    file.write('\nlambda2/lambda1:\n')
    for i, lam1 in enumerate(lambdas):
        for j, lam2 in enumerate(lambdas):
            s = "%8.4f" % (rt1[i, j])
            file.write(s + '\t')
        file.write('\n')

    file.write('\nм.о. длительности пребывания (для 2-класса) от входящего потока')
    file.write('\nlambda2/lambda1:\n')
    for i, lam1 in enumerate(lambdas):
        for j, lam2 in enumerate(lambdas):
            s = "%8.4f" % (rt2[i, j])
            file.write(s + '\t')
        file.write('\n')

    file.write('\nвероятность отказа (общая) от входящего потока')
    file.write('\nlambda2/lambda1:\n')
    for i, lam1 in enumerate(lambdas):
        for j, lam2 in enumerate(lambdas):
            s = "%8.4f" % (pf[i, j])
            file.write(s + '\t')
        file.write('\n')

    plt.plot(lambdas, pf[2], 'b')
    plt.plot(lambdas, [p[2] for p in pf], 'r')
    plt.title(f"Зависимость вероятности отказа")
    plt.xlabel("lambda")
    plt.ylabel("PF")
    plt.grid()
    plt.show()

    file.write('\nвероятность отказа (для 1-класса) от входящего потока')
    file.write('\nlambda2/lambda1:\n')
    for i, lam1 in enumerate(lambdas):
        for j, lam2 in enumerate(lambdas):
            s = "%8.4f" % (pf1[i, j])
            file.write(s + '\t')
        file.write('\n')

    file.write('\nвероятность отказа  (для 2-класса) от входящего потока')
    file.write('\nlambda2/lambda1:\n')
    for i, lam1 in enumerate(lambdas):
        for j, lam2 in enumerate(lambdas):
            s = "%8.4f" % (pf2[i, j])
            file.write(s + '\t')
        file.write('\n')

    file.write('\nм.о. числа треб. в очереди 1-класса от входящего потока')
    file.write('\nlambda2/lambda1:\n')
    for i, lam1 in enumerate(lambdas):
        for j, lam2 in enumerate(lambdas):
            s = "%8.4f" % (q1[i, j])
            file.write(s + '\t')
        file.write('\n')

    file.write('\nм.о. числа треб. в очереди 2-класса от входящего потока')
    file.write('\nlambda2/lambda1:\n')
    for i, lam1 in enumerate(lambdas):
        for j, lam2 in enumerate(lambdas):
            s = "%8.4f" % (q2[i, j])
            file.write(s + '\t')
        file.write('\n')

    # считаем теперь м.о. числа требований в очередях от размерности очередей
    capacitys = range(5, 21, 3)
    for i, cap1 in enumerate(capacitys):
        for j, cap2 in enumerate(capacitys):
            sp = StateSpace(_M, _a, _b, cap1, cap2, _lambda1, _lambda2, _mu)
            sp.start()
            q1[i, j] = sp.Q1
            q2[i, j] = sp.Q2

    file.write('\nм.о. числа треб. в очереди 1-класса от расмерности очередей')
    file.write('\ncap2/cap1:\n')
    for i, cap1 in enumerate(lambdas):
        for j, cap2 in enumerate(lambdas):
            s = "%8.4f" % (q1[i, j])
            file.write(s + '\t')
        file.write('\n')

    file.write('\nм.о. числа треб. в очереди 2-класса от расмерности очередей')
    file.write('\ncap2/cap1:\n')
    for i, cap1 in enumerate(lambdas):
        for j, cap2 in enumerate(lambdas):
            s = "%8.4f" % (q2[i, j])
            file.write(s + '\t')
        file.write('\n')

    file.close()
