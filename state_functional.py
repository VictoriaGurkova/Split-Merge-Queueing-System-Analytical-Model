from dataclasses import dataclass

from network_params import Params


@dataclass
class StateConfig:
    capacity1: int
    capacity2: int
    q1: int
    q2: int
    devices: list
    free_devices_number: int

    def get_q_by_class_id(self, class_id: int) -> int:
        return self.q1 if class_id == 1 else self.q2

    def get_capacity_by_class_id(self, class_id: int) -> int:
        return self.capacity1 if class_id == 1 else self.capacity2


@dataclass
class UpdateState:
    devices_state_class1: list
    devices_state_class2: list
    q1: int
    q2: int
    free_devices_number: int

    def get_q_by_class_id(self, class_id: int) -> int:
        return self.q1 if class_id == 1 else self.q2

    def update_q_by_class_id(self, class_id: int) -> None:
        if class_id == 1:
            self.q1 -= 1
        else:
            self.q2 -= 1

    def get_devices_state_by_class_id(self, class_id: int) -> list:
        return self.devices_state_class1 if class_id == 1 else self.devices_state_class2

    def update_devices_state_by_class_id(self, class_id: int, value: list) -> None:
        if class_id == 1:
            self.devices_state_class1 += value
        else:
            self.devices_state_class2 += value

    def device_state_by_class_id_pop(self, class_id, index):
        if class_id == 1:
            self.devices_state_class1.pop(index)
        else:
            self.devices_state_class2.pop(index)


def define_queue_state(q1: int, q2: int, devices: list, lambda1: float, lambda2: float,
                       states_and_rates: dict, class_id: int) -> None:
    if class_id == 1:
        update_queue_state(q1 + 1, q2, devices, lambda1, states_and_rates, class_id)
    else:
        update_queue_state(q1, q2 + 1, devices, lambda2, states_and_rates, class_id)


def update_queue_state(q1: int, q2: int, devices: list, lambda_: float, states_and_rates: dict, class_id: int) -> None:
    from logs import log_arrival_in_queue

    state = create_state(q1, q2, devices[0], devices[1])
    log_arrival_in_queue(lambda_, state, class_id)
    states_and_rates[state] += lambda_


def define_devices_state(q1: int, q2: int, devices: list, lambda1: float, lambda2: float,
                         states_and_rates: dict, params: Params, class_id: int) -> None:
    if class_id == 1:
        update_devices_state(q1, q2, devices, lambda1, states_and_rates, params, class_id)
    else:
        update_devices_state(q1, q2, devices, lambda2, states_and_rates, params, class_id)


def update_devices_state(q1: int, q2: int, devices: list, rate: float,
                         states_and_rates: dict, params: Params, class_id: int) -> None:
    from logs import log_arrival_on_devices

    update_state = devices[class_id - 1]
    update_state += (params.fragments_numbers[class_id - 1],)

    state = create_state(q1, q2, update_state, devices[1]) if class_id == 1 \
        else create_state(q1, q2, devices[0], update_state)

    log_arrival_on_devices(rate, state, class_id)
    states_and_rates[state] += rate


def update_system_state(state_config: StateConfig, update_state: UpdateState,
                        params: Params, class_id: int, id: int) -> None:
    if state_config.get_q_by_class_id(id):
        while update_state.free_devices_number + \
                params.fragments_numbers[class_id - 1] >= \
                params.fragments_numbers[id - 1] and update_state.get_q_by_class_id(id):
            update_state.update_devices_state_by_class_id(id, [params.fragments_numbers[id - 1]])
            update_state.update_q_by_class_id(id)
            update_state.free_devices_number -= params.fragments_numbers[id - 1]


def create_state(q1: int, q2: int, first_class: list, second_class: list) -> tuple:
    return (q1, q2), (tuple(sorted(first_class)),
                      tuple(sorted(second_class)))


def get_state_config(params: Params, current_state: list) -> StateConfig:
    from calculations import get_number_of_free_devices_for_server_state
    state_config = StateConfig(
        capacity1=params.queues_capacities[0],
        capacity2=params.queues_capacities[1],
        q1=current_state[0][0],
        q2=current_state[0][1],
        devices=current_state[1],
        free_devices_number=get_number_of_free_devices_for_server_state(params, current_state[1])
    )
    return state_config


def get_update_state(state_config: StateConfig) -> UpdateState:
    update_state = UpdateState(
        devices_state_class1=list(state_config.devices[0]),
        devices_state_class2=list(state_config.devices[1]),
        q1=state_config.q1,
        q2=state_config.q2,
        free_devices_number=state_config.free_devices_number
    )
    return update_state
