import logging
from collections import defaultdict

from states_view import *
from utils import *

logger = logging.getLogger()


def create_state(q1, q2, first_class, second_class):
    return (q1, q2), (tuple(sorted(first_class)),
                      tuple(sorted(second_class)))


def get_server_states(x, y, params):
    server_states = set()
    for i in range(x + 1):
        for j in range(y + 1):
            total_number_of_tasks = params.fragments_amounts[0] * i + \
                                    params.fragments_amounts[1] * j
            if params.devices_amount < total_number_of_tasks:
                continue
            X = sorted(get_fragments_lots(i, params.fragments_amounts[0]))
            Y = sorted(get_fragments_lots(j, params.fragments_amounts[1]))
            server_states.update(itertools.product(X, Y))
    return server_states


def get_all_state_with_queues(server_states: set, queue_capacity: list, params):
    states = []
    queue_states = set(itertools.product(range(queue_capacity[0] + 1),
                                         range(queue_capacity[1] + 1)))

    for q_state in queue_states:
        for server_state in server_states:
            if check_possible_state(q_state, server_state, params):
                states.append((q_state, server_state))
    return states


def check_possible_state(q_state, state, params):
    free_devices_number = \
        get_number_of_free_devices_for_server_state(params, state)
    if q_state[0] and free_devices_number >= params.fragments_amounts[0]:
        return False
    if q_state[1] and free_devices_number >= params.fragments_amounts[1]:
        return False
    return True


# TODO: simplify
def get_achievable_states(params, current_state):
    states_and_rates = defaultdict(float)

    # TODO: move to logs
    logger.debug('#' * 100)
    logger.debug('Рассмотрим состояние ' + pretty_state(current_state))

    capacity1 = params.queues_capacities[0]
    capacity2 = params.queues_capacities[1]

    # получаем различные характеристики состояния
    q1 = current_state[0][0]
    logger.debug(f'q1 = {q1}')
    q2 = current_state[0][1]
    logger.debug(f'q2 = {q2}')
    server_state = current_state[1]
    logger.debug(f'server_state = {server_state}')

    number_of_free_servers = \
        get_number_of_free_devices_for_server_state(params, server_state)
    logger.debug(f"Число свободных приборов {number_of_free_servers}")

    logger.debug("ПОСТУПЛЕНИЕ")
    if q1 != capacity1:
        if number_of_free_servers < params.fragments_amounts[0]:
            new_state = create_state(q1 + 1, q2,
                                     server_state[0],
                                     server_state[1])
            logger.debug(f'Поступление требования первого класса в '
                         f'очередь с интенсивностью {params.lambda1} и '
                         f'переход в стояние  {pretty_state(new_state)}')
            states_and_rates[new_state] += params.lambda1
        else:
            updated_first_demands_tasks = server_state[0]
            updated_first_demands_tasks += (params.fragments_amounts[0],)
            new_state = create_state(q1, q2,
                                     updated_first_demands_tasks,
                                     server_state[1])
            logger.debug(f'Поступление требования первого класса с '
                         f'интенсивностью {params.lambda1} и '
                         f'немедленное начало его'
                         f' обслуживания и переход в состояние {pretty_state(new_state)}')
            states_and_rates[new_state] += params.lambda1
    else:
        logger.debug("Очередь заполнена - требование потерялось")

    if q2 != capacity2:
        if number_of_free_servers < params.fragments_amounts[1]:
            new_state = create_state(q1, q2 + 1,
                                     server_state[0],
                                     server_state[1])
            logger.debug(f'Поступление требования второго класса в очередь с '
                         f'интенсивностью {params.lambda2} и '
                         f'переход в стояние  {pretty_state(new_state)}')
            states_and_rates[new_state] += params.lambda2
        else:
            updated_second_demands_tasks = server_state[1]
            updated_second_demands_tasks += (params.fragments_amounts[1],)
            new_state = create_state(q1, q2, server_state[0],
                                     updated_second_demands_tasks)
            logger.debug(f'Поступление требования второго класса с '
                         f'интенсивностью {params.lambda2} и '
                         f'немедленное начало его обслуживания и '
                         f'переход в состояние {pretty_state(new_state)}')
            states_and_rates[new_state] += params.lambda2
    else:
        logger.debug("Очередь заполнена - требование потерялось")

    logger.debug('УХОД')
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
                        params.fragments_amounts[0] >= \
                        params.fragments_amounts[0] and copy_q1:
                    updated_first_demands_tasks += [params.fragments_amounts[0]]
                    copy_q1 -= 1
                    copy_number_of_free_servers -= params.fragments_amounts[0]
            if q2:
                while copy_number_of_free_servers + \
                        params.fragments_amounts[0] >= \
                        params.fragments_amounts[1] and copy_q2:
                    updated_second_demands_tasks += [params.fragments_amounts[1]]
                    copy_q2 -= 1
                    copy_number_of_free_servers -= params.fragments_amounts[1]
            new_state = create_state(copy_q1, copy_q2,
                                     updated_first_demands_tasks,
                                     updated_second_demands_tasks)
            logger.debug(f'Завершение обслуживания всего требования '
                         f'первого класса с интенсивностью {params.mu}, и '
                         f'переход в состояние {pretty_state(new_state)}')
            states_and_rates[new_state] += params.mu

        else:
            leave_intensity = params.mu * number_of_lost_tasks_in_demand
            updated_first_demands_tasks[index] -= 1
            new_state = create_state(q1, q2, updated_first_demands_tasks,
                                     server_state[1])
            logger.debug(f'Завершение обслуживания фрагмента '
                         f'требования первого класса с '
                         f'интенсивностью {leave_intensity}'
                         f" переход в состояние {pretty_state(new_state)}")
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
                while copy_number_of_free_servers + params.fragments_amounts[1] >= \
                        params.fragments_amounts[0] and copy_q1:
                    updated_first_demands_tasks += [params.fragments_amounts[0]]
                    copy_q1 -= 1
                    copy_number_of_free_servers -= params.fragments_amounts[0]
            if q2:
                while copy_number_of_free_servers + params.fragments_amounts[1] >= \
                        params.fragments_amounts[1] and copy_q2:
                    updated_second_demands_tasks += [params.fragments_amounts[1]]
                    copy_q2 -= 1
                    copy_number_of_free_servers -= params.fragments_amounts[1]
            new_state = create_state(copy_q1, copy_q2,
                                     updated_first_demands_tasks,
                                     updated_second_demands_tasks)
            logger.debug(f'Завершение обслуживания всего требования '
                         f'второго класса с интенсивностью {params.mu}'
                         f'и переход в состояние {pretty_state(new_state)}')
            states_and_rates[new_state] += params.mu

        else:
            leave_intensity = params.mu * number_of_lost_tasks_in_demand
            updated_second_demands_tasks[index] -= 1
            new_state = create_state(q1, q2, server_state[0],
                                     updated_second_demands_tasks)
            logger.debug(f'Завершение обслуживания фрагмента '
                         f'требования второго класса с '
                         f'интенсивностью {leave_intensity} '
                         f'и переход в состояние {pretty_state(new_state)}')
            states_and_rates[new_state] += leave_intensity

    return states_and_rates

