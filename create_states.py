import itertools
import numpy as np
from collections import defaultdict

empty_set_str = u"\u2205"


def pretty_server_state(server_state):
    elements = []
    for s in server_state:
        if len(s) == 0:
            elements.append(empty_set_str)
        else:
            elements.append(str(s))
    # склеиваем все вместе и заменяем скобки list на фигурные для множества
    return '(' + \
           ', '.join(elements).replace('(', '{').replace(',)', '}').replace(')', '}') \
           + ')'


def pretty_state(state):
    queue_state = state[0]
    server_state = state[1]
    return '(' + str(queue_state) + ': ' + pretty_server_state(server_state) + ')'


# не понимаю из названия предназначение функции
def get_lots_of_fragments(amount_of_demands, fragments_in_class):
    return list(itertools.combinations_with_replacement(range(1, fragments_in_class + 1), amount_of_demands))


def get_all_state_with_queues(server_states: set, queue_capacity: list, M, a, b):
    states = []
    queue_states = set(itertools.product(range(queue_capacity[0] + 1), range(queue_capacity[1] + 1)))

    for q_state in queue_states:
        for server_state in server_states:
            # вы же понимаете, что это не самый оптимальный метод генерации
            # гененируется слишком много лишних состояний, которые потом фильтруем
            # но пусть пока будет так
            if is_possible_state(q_state, server_state, M, a, b):
                states.append((q_state, server_state))
    return states


def is_possible_state(q_state, state, M, a, b):
    number_of_free_servers = number_of_free_servers_for_server_state(state, M, a, b)
    if q_state[0] and number_of_free_servers >= a:
        return False
    if q_state[1] and number_of_free_servers >= b:
        return False
    return True


# возвращает словарь {состояние: интенсивность перехода}
def get_achievable_states(current_state: tuple, M: int, a: int, b: int, queue_capacity: list,
                          lambda1: float, lambda2: float, mu: float):
    # лучше взять именно дефолтовый словарь,  а не обычный, пояснения в остальных комментариях
    states_and_rates = defaultdict(float)

    print('#' * 100)
    print('Рассмотрим состояние ' + pretty_state(current_state))

    capacity1 = queue_capacity[0]
    capacity2 = queue_capacity[1]

    # получаем различные характеристики состояния
    q1 = current_state[0][0]
    print('q1 = ', q1)
    q2 = current_state[0][1]
    print('q2 = ', q2)
    server_state = current_state[1]
    print('server_state = ', server_state)

    number_of_free_servers = number_of_free_servers_for_server_state(server_state, M, a, b)
    print("Число свободных приборов", number_of_free_servers)

    # ПОСТУПЛЕНИЕ
    # первый класс - поступление требований
    # если приборов не хватает, то идем в очередь, если размер очереди позволяет
    print("ПОСТУПЛЕНИЕ")
    if q1 != capacity1:
        # идем в очередь
        if number_of_free_servers < a:
            new_state = create_state(q1 + 1, q2, server_state[0], server_state[1])
            print(f'Поступление требования первого класса в очередь с интенсивностью {lambda1} и переход в стояние ',
                  pretty_state(new_state))
            # плюсуем интенсивность, так как может быть такая ситуация, что мы перейдем  одно состояние (new_state)
            # из-за нескольких
            # событий (интесивности при это будут складываться),  а если мы будем каждый раз просто приравнивать,
            # то потеряем часть интенсивностей
            # также именно здесь проявляется удобство  defaultdict - если не было состояния,
            # то дефолтовое значение будет
            # равно нулю
            # аналогичное добавление в словарь производим для всех событий
            states_and_rates[new_state] += lambda1
        # идем на приборы - добавление во множество новое требование - т.е. новое количество фрагментов
        else:
            updated_second_demands_tasks = server_state[0]
            updated_second_demands_tasks = updated_second_demands_tasks + (a,)
            new_state = create_state(q1, q2, updated_second_demands_tasks, server_state[1])
            print(f'Поступление требования первого класса с интенсивностью {lambda1} и немедленное начало его '
                  'обслуживания и переход в состояние ', pretty_state(new_state))
            states_and_rates[new_state] += lambda1
    else:
        print("Очередь заполнена - требование потерялось")

    if q2 != capacity2:
        # идем в очередь
        if number_of_free_servers < b:
            new_state = create_state(q1, q2 + 1, server_state[0], server_state[1])
            print(f'Поступление требования второго класса в очередь с интенсивностью {lambda2} и переход в стояние ',
                  pretty_state(new_state))
            states_and_rates[new_state] += lambda2
        # идем на приборы - добавление во множество новое требование - т.е. новое количество фрагментов
        else:
            updated_second_demands_tasks = server_state[1]
            updated_second_demands_tasks = updated_second_demands_tasks + (b,)
            new_state = create_state(q1, q2, server_state[0], updated_second_demands_tasks)
            print(f'Поступление требования второго класса с интенсивностью {lambda2} и немедленное начало его '
                  ' обслуживания и переход в состояние ', pretty_state(new_state))
            states_and_rates[new_state] += lambda2
    else:
        print("Очередь заполнена - требование потерялось")

    # ЗАВЕРШЕНИЕ ОБСЛУЖИВАНИЯ
    print('УХОД')
    # 1й класс
    for state_id, number_of_lost_tasks_in_demand in enumerate(server_state[0]):
        updated_first_demands_tasks = list(server_state[0])
        copy_q1 = q1
        if number_of_lost_tasks_in_demand == 1:
            updated_first_demands_tasks.pop(state_id)
            if q1:
                updated_first_demands_tasks = updated_first_demands_tasks + [a]
                copy_q1 = q1 - 1
            new_state = create_state(copy_q1, q2, tuple(updated_first_demands_tasks), server_state[1])
            print(f'Завершение обслуживания всего требования первого класса с интенсивностью {mu}',
                  'и переход в состояние ', pretty_state(new_state))
            states_and_rates[new_state] += mu

        else:
            leave_intensity = mu * updated_first_demands_tasks[state_id]
            updated_first_demands_tasks[state_id] -= 1
            new_state = create_state(q1, q2, tuple(updated_first_demands_tasks), server_state[1])
            print(f'Завершение обслуживания фрагмента требования первого класса с интенсивностью {leave_intensity}',
                  'и переход в состояние ', pretty_state(new_state))
            states_and_rates[new_state] += leave_intensity

    # 2й класс
    for state_id, number_of_lost_tasks_in_demand in enumerate(server_state[1]):
        updated_second_demands_tasks = list(server_state[1])
        copy_q2 = q2
        if number_of_lost_tasks_in_demand == 1:
            updated_second_demands_tasks.pop(state_id)
            if q2:
                updated_second_demands_tasks = updated_second_demands_tasks + [b]
                copy_q2 = q2 - 1
            new_state = create_state(q1, copy_q2, server_state[0], tuple(updated_second_demands_tasks))
            print(f'Завершение обслуживания всего требования второго класса с интенсивностью {mu}',
                  'и переход в состояние ', pretty_state(new_state))
            states_and_rates[new_state] += mu

        else:
            leave_intensity = mu * updated_second_demands_tasks[state_id]
            updated_second_demands_tasks[state_id] -= 1
            new_state = create_state(q1, q2, server_state[0], tuple(updated_second_demands_tasks))
            print(f'Завершение обслуживания фрагмента требования второго класса с интенсивностью {leave_intensity}',
                  'и переход в состояние ', pretty_state(new_state))
            states_and_rates[new_state] += leave_intensity

    return states_and_rates


def create_generator(states: list,
                     M: int, a: int, b: int, queue_capacity: list,
                     lambda1: float, lambda2: float, mu: float):
    n = len(states)
    Q = np.zeros((n, n))
    # проходим по каждому состоянию и смотрим на его смежные
    for i, current_state in enumerate(states):
        # давайте засунем это все уже в какой-ниюудь класс, такой длинный список переменных  = путь к ошибке
        states_and_rates = get_achievable_states(current_state, M, a, b, queue_capacity, lambda1, lambda2, mu)
        for state, rate in states_and_rates.items():
            # текущее состояние имеет номер i, смотрим на номер j смежного состояния
            j = states.index(state)
            # снова делаем += а не просто равно, чтобы не перетереть результаты перехода
            Q[i, j] += rate

    # мы должны получить генератор цепи Маркова, по диагонали должна стоять сумма всех элементов с минусом
    # нужно это дописать
    return Q


def number_of_free_servers_for_server_state(server_state, M, a, b):
    number = M - (len(server_state[0]) * a + len(server_state[1]) * b)
    if number < 0:
        raise Exception("Number of free servers for states < 0, it is not correct state")
    return number


def create_state(q1, q2, first_class, second_class):
    return (q1, q2), (first_class, second_class)


def main():
    server_states = set()
    # число приборов
    M = 3  # int(input("M = "))
    # число фрагментов в 1м классе
    a = 2  # int(input("a = "))
    # число фрагментов во 2м классе
    b = 1  # int(input("b = "))
    # максимальное число требований 1го класса, которое может быть на приборах
    x = M // a
    print('Максимальное число требований 1го класса = ', x)
    # максимальное число требований 2го класса, которое может быть на приборах
    y = M // b
    print('Максимальное число требований 2го класса = ', y)

    # вместимость очереди 1го класса
    capacity1 = 5
    # вместимость очереди 2го класса
    capacity2 = 5

    lambda1 = 1
    lambda2 = 2
    mu = 3

    queue_capacity = [capacity1, capacity2]

    # следует вынести в отдельную функцию
    for i in range(x + 1):
        for j in range(y + 1):
            # общее число фрагментов в системе
            total_number_of_tasks = a * i + b * j
            if M < total_number_of_tasks:
                continue
            X = sorted(get_lots_of_fragments(i, a))
            Y = sorted(get_lots_of_fragments(j, b))
            server_states.update(itertools.product(X, Y))

    print("Состояния фрагментов на системах (не включая очереди):")

    # enumerate создает пары - номер и элемент чего-то
    for state_id, state in enumerate(server_states):
        print('S' + str(state_id), '= ', pretty_server_state(state))

    states = get_all_state_with_queues(server_states, queue_capacity, M, a, b)
    print("\nСостояния системы вместе с очередями:")

    for state_id, state in enumerate(states):
        print('S' + str(state_id), '= ', pretty_state(state))

    Q = create_generator(states, M, a, b, queue_capacity, lambda1, lambda2, mu)

    print('Q = ', Q)
    # нужно будет проверить кооректность заполнения матрицы,
    # удобно скопировать в excel
    # и применить условное форматирование
    np.savetxt("Q.txt", Q, fmt='%0.0f')


if __name__ == '__main__':
    main()
