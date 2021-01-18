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


def get_all_state_with_queues(server_states: set, queues_capacities: list, params):
    states = []
    queue_states = set(itertools.product(range(queues_capacities[0] + 1),
                                         range(queues_capacities[1] + 1)))

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

    state_config = {
        "capacity1": params.queues_capacities[0],
        "capacity2": params.queues_capacities[1],
        "q1": current_state[0][0],
        "q2": current_state[0][1],
        "devices": current_state[1],
        "free_devices_number": get_number_of_free_devices_for_server_state(params, current_state[1])
    }

    # capacity1 = params.queues_capacities[0]
    # capacity2 = params.queues_capacities[1]
    # q1 = current_state[0][0]
    # q2 = current_state[0][1]
    # server_state = current_state[1]
    # free_devices_number = \
    #     get_number_of_free_devices_for_server_state(params, server_state)
    #
    # logger.debug(f'q1 = {q1}')
    # logger.debug(f'q2 = {q2}')
    # logger.debug(f'server_state = {server_state}')
    # logger.debug(f"Число свободных приборов {free_devices_number}")

    arrival_handler(params, state_config, states_and_rates)
    leaving_handler(params, state_config, states_and_rates)

    return states_and_rates


def arrival_handler(params, state_config, states_and_rates):
    logger.debug("ПОСТУПЛЕНИЕ")

    if state_config["q1"] != state_config["capacity1"]:
        if state_config["free_devices_number"] < params.fragments_amounts[0]:
            new_state = create_state(state_config["q1"] + 1, state_config["q2"],
                                     state_config["devices"][0],
                                     state_config["devices"][1])

            # TODO: move to logs
            logger.debug(f'Поступление требования первого класса в '
                         f'очередь с интенсивностью {params.lambda1} и '
                         f'переход в стояние  {pretty_state(new_state)}')

            states_and_rates[new_state] += params.lambda1
        else:
            updated_first_demands_tasks = state_config["devices"][0]
            updated_first_demands_tasks += (params.fragments_amounts[0],)
            new_state = create_state(state_config["q1"], state_config["q2"],
                                     updated_first_demands_tasks,
                                     state_config["devices"][1])

            # TODO: move to logs
            logger.debug(f'Поступление требования первого класса с '
                         f'интенсивностью {params.lambda1} и '
                         f'немедленное начало его'
                         f' обслуживания и переход в состояние {pretty_state(new_state)}')

            states_and_rates[new_state] += params.lambda1
    else:
        logger.debug("Очередь заполнена - требование потерялось")

    if state_config["q2"] != state_config["capacity2"]:
        if state_config["free_devices_number"] < params.fragments_amounts[1]:
            new_state = create_state(state_config["q1"], state_config["q2"] + 1,
                                     state_config["devices"][0],
                                     state_config["devices"][1])

            # TODO: move to logs
            logger.debug(f'Поступление требования второго класса в очередь с '
                         f'интенсивностью {params.lambda2} и '
                         f'переход в стояние  {pretty_state(new_state)}')

            states_and_rates[new_state] += params.lambda2
        else:
            updated_second_demands_tasks = state_config["devices"][1]
            updated_second_demands_tasks += (params.fragments_amounts[1],)
            new_state = create_state(state_config["q1"], state_config["q2"], state_config["devices"][0],
                                     updated_second_demands_tasks)

            # TODO: move to logs
            logger.debug(f'Поступление требования второго класса с '
                         f'интенсивностью {params.lambda2} и '
                         f'немедленное начало его обслуживания и '
                         f'переход в состояние {pretty_state(new_state)}')

            states_and_rates[new_state] += params.lambda2
    else:
        logger.debug("Очередь заполнена - требование потерялось")


def leaving_handler(params, state_config, states_and_rates):
    logger.debug('УХОД')
    # 1й класс
    for index, number_of_lost_tasks_in_demand in \
            enumerate(state_config["devices"][0]):
        updated_first_demands_tasks = list(state_config["devices"][0])
        updated_second_demands_tasks = list(state_config["devices"][1])
        copy_q1 = state_config["q1"]
        copy_q2 = state_config["q2"]
        copy_number_of_free_servers = state_config["free_devices_number"]
        # требование уйдет полностью, если остался один фрагмент
        if number_of_lost_tasks_in_demand == 1:
            updated_first_demands_tasks.pop(index)
            if state_config["q1"]:
                while copy_number_of_free_servers + \
                        params.fragments_amounts[0] >= \
                        params.fragments_amounts[0] and copy_q1:
                    updated_first_demands_tasks += [params.fragments_amounts[0]]
                    copy_q1 -= 1
                    copy_number_of_free_servers -= params.fragments_amounts[0]
            if state_config["q2"]:
                while copy_number_of_free_servers + \
                        params.fragments_amounts[0] >= \
                        params.fragments_amounts[1] and copy_q2:
                    updated_second_demands_tasks += [params.fragments_amounts[1]]
                    copy_q2 -= 1
                    copy_number_of_free_servers -= params.fragments_amounts[1]
            new_state = create_state(copy_q1, copy_q2,
                                     updated_first_demands_tasks,
                                     updated_second_demands_tasks)

            # TODO: move to logs
            logger.debug(f'Завершение обслуживания всего требования '
                         f'первого класса с интенсивностью {params.mu}, и '
                         f'переход в состояние {pretty_state(new_state)}')

            states_and_rates[new_state] += params.mu

        else:
            leave_intensity = params.mu * number_of_lost_tasks_in_demand
            updated_first_demands_tasks[index] -= 1
            new_state = create_state(state_config["q1"], state_config["q2"], updated_first_demands_tasks,
                                     state_config["devices"][1])

            # TODO: move to logs
            logger.debug(f'Завершение обслуживания фрагмента '
                         f'требования первого класса с '
                         f'интенсивностью {leave_intensity}'
                         f" переход в состояние {pretty_state(new_state)}")

            states_and_rates[new_state] += leave_intensity

    # 2й класс
    for index, number_of_lost_tasks_in_demand in \
            enumerate(state_config["devices"][1]):
        updated_first_demands_tasks = list(state_config["devices"][0])
        updated_second_demands_tasks = list(state_config["devices"][1])
        copy_q1 = state_config["q1"]
        copy_q2 = state_config["q2"]
        copy_number_of_free_servers = state_config["free_devices_number"]
        if number_of_lost_tasks_in_demand == 1:
            updated_second_demands_tasks.pop(index)
            if state_config["q1"]:
                while copy_number_of_free_servers + params.fragments_amounts[1] >= \
                        params.fragments_amounts[0] and copy_q1:
                    updated_first_demands_tasks += [params.fragments_amounts[0]]
                    copy_q1 -= 1
                    copy_number_of_free_servers -= params.fragments_amounts[0]
            if state_config["q2"]:
                while copy_number_of_free_servers + params.fragments_amounts[1] >= \
                        params.fragments_amounts[1] and copy_q2:
                    updated_second_demands_tasks += [params.fragments_amounts[1]]
                    copy_q2 -= 1
                    copy_number_of_free_servers -= params.fragments_amounts[1]
            new_state = create_state(copy_q1, copy_q2,
                                     updated_first_demands_tasks,
                                     updated_second_demands_tasks)

            # TODO: move to logs
            logger.debug(f'Завершение обслуживания всего требования '
                         f'второго класса с интенсивностью {params.mu}'
                         f'и переход в состояние {pretty_state(new_state)}')

            states_and_rates[new_state] += params.mu

        else:
            leave_intensity = params.mu * number_of_lost_tasks_in_demand
            updated_second_demands_tasks[index] -= 1
            new_state = create_state(state_config["q1"], state_config["q2"], state_config["devices"][0],
                                     updated_second_demands_tasks)
            logger.debug(f'Завершение обслуживания фрагмента '
                         f'требования второго класса с '
                         f'интенсивностью {leave_intensity} '
                         f'и переход в состояние {pretty_state(new_state)}')
            states_and_rates[new_state] += leave_intensity



