from logs import log_arrival_in_queue, log_arrival_on_devices
from network_params import Params


def define_queue_state(q1: int, q2: int, devices: list, lambda1: float, lambda2: float,
                       states_and_rates: dict, class_id: int) -> None:
    if class_id == 1:
        update_queue_state(q1 + 1, q2, devices, lambda1, states_and_rates, class_id)
    else:
        update_queue_state(q1, q2 + 1, devices, lambda2, states_and_rates, class_id)


def update_queue_state(q1: int, q2: int, devices: list, lambda_: float, states_and_rates: dict, class_id: int) -> None:
    state = create_state(q1, q2, devices[0], devices[1])
    log_arrival_in_queue(lambda_, state, class_id)
    states_and_rates[state] += lambda_


def define_devices_state(q1: int, q2: int, devices: list, lambda1: float, lambda2: float,
                         states_and_rates: dict, params: Params, class_id: int) -> None:
    if class_id == 1:
        update_devices_state(q1, q2, devices, lambda1, states_and_rates, params, class_id)
    else:
        update_devices_state(q1, q2, devices, lambda2, states_and_rates, params, class_id)


def update_devices_state(q1: int, q2: int, devices: list, lambda_: float,
                         states_and_rates: dict, params: Params, class_id: int) -> None:
    upd_state = devices[class_id - 1]
    upd_state += (params.fragments_numbers[class_id - 1],)

    state = create_state(q1, q2, upd_state, devices[1]) if class_id == 1 \
        else create_state(q1, q2, devices[0], upd_state)

    log_arrival_on_devices(lambda_, state, class_id)
    states_and_rates[state] += lambda_


def update_system_state(config: dict, upd: dict, params: Params, class_id: int, class_id_str: str) -> None:
    if config["q" + class_id_str]:
        while upd["free_devices_number"] + \
                params.fragments_numbers[class_id - 1] >= \
                params.fragments_numbers[int(class_id_str) - 1] and upd["q" + class_id_str]:
            upd["devices_state_class" + class_id_str] += [params.fragments_numbers[int(class_id_str) - 1]]
            upd["q" + class_id_str] -= 1
            upd["free_devices_number"] -= params.fragments_numbers[int(class_id_str) - 1]


def create_state(q1: int, q2: int, first_class: list, second_class: list) -> tuple:
    return (q1, q2), (tuple(sorted(first_class)),
                      tuple(sorted(second_class)))


def get_state_config(params: Params, current_state: list) -> dict:
    from calculations import get_number_of_free_devices_for_server_state
    return {
        "capacity1": params.queues_capacities[0],
        "capacity2": params.queues_capacities[1],
        "q1": current_state[0][0],
        "q2": current_state[0][1],
        "devices": current_state[1],
        "free_devices_number": get_number_of_free_devices_for_server_state(params, current_state[1])
    }


def get_upd_variables(state_config: dict) -> dict:
    return {
        "devices_state_class1": list(state_config["devices"][0]),
        "devices_state_class2": list(state_config["devices"][1]),
        "q1": state_config["q1"],
        "q2": state_config["q2"],
        "free_devices_number": state_config["free_devices_number"]
    }
