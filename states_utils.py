from collections import defaultdict

from logs import *
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


def get_achievable_states(params, current_state):
    log_state(current_state)
    states_and_rates = defaultdict(float)

    state_config = get_state_config(params, current_state)
    log_state_config(state_config)

    arrival_handler(params, state_config, states_and_rates)
    leaving_handler(params, state_config, states_and_rates)

    return states_and_rates


def arrival_handler(params, state_config, states_and_rates):
    log_message('Поступление')
    arrival_handler_for_class(params, state_config, states_and_rates, 1)
    arrival_handler_for_class(params, state_config, states_and_rates, 2)


def arrival_handler_for_class(params, config, states_and_rates, class_id):
    if config[f"q{class_id}"] != config[f"capacity{class_id}"]:
        if config["free_devices_number"] < params.fragments_amounts[class_id - 1]:
            define_queue_state(config["q1"], config["q2"],
                               [config["devices"][0], config["devices"][1]],
                               params.lambda1, params.lambda2,
                               states_and_rates, class_id)
        else:
            define_devices_state(config["q1"], config["q2"],
                                 [config["devices"][0], config["devices"][1]],
                                 params.lambda1, params.lambda2,
                                 states_and_rates, params, class_id)
    else:
        log_message('Очередь заполнена - требование потерялось')


def define_queue_state(q1, q2, devices, lambda1, lambda2, states_and_rates, class_id):
    if class_id == 1:
        update_queue_state(q1 + 1, q2, devices, lambda1, states_and_rates, class_id)
    elif class_id == 2:
        update_queue_state(q1, q2 + 1, devices, lambda2, states_and_rates, class_id)


def update_queue_state(q1, q2, devices, lambda_, states_and_rates, class_id):
    state = create_state(q1, q2, devices[0], devices[1])
    log_arrival_in_queue(lambda_, state, class_id)
    states_and_rates[state] += lambda_


def define_devices_state(q1, q2, devices, lambda1, lambda2, states_and_rates, params, class_id):
    if class_id == 1:
        update_devices_state(q1, q2, devices, lambda1, states_and_rates, params, class_id)
    elif class_id == 2:
        update_devices_state(q1, q2, devices, lambda2, states_and_rates, params, class_id)


def update_devices_state(q1, q2, devices, lambda_, states_and_rates, params, class_id):
    upd_state = devices[class_id - 1]
    upd_state += (params.fragments_amounts[class_id - 1],)

    state = create_state(q1, q2, upd_state, devices[1]) if class_id == 1 \
        else create_state(q1, q2, devices[0], upd_state)

    log_arrival_on_devices(lambda_, state, class_id)
    states_and_rates[state] += lambda_


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


def get_state_config(params, current_state):
    return {
        "capacity1": params.queues_capacities[0],
        "capacity2": params.queues_capacities[1],
        "q1": current_state[0][0],
        "q2": current_state[0][1],
        "devices": current_state[1],
        "free_devices_number": get_number_of_free_devices_for_server_state(params, current_state[1])
    }
