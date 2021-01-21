from collections import defaultdict

from utils import *


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
    arrival_handler_for_class(params, state_config, states_and_rates, class_id=1)
    arrival_handler_for_class(params, state_config, states_and_rates, class_id=2)


def leaving_handler(params, state_config, states_and_rates):
    log_message('УХОД')
    leaving_handler_for_class(state_config, states_and_rates, params, class_id=1)
    leaving_handler_for_class(state_config, states_and_rates, params, class_id=2)


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


def leaving_handler_for_class(state_config, states_and_rates, params, class_id):
    for index, unserved_fragments_number in \
            enumerate(state_config["devices"][class_id - 1]):
        upd = get_upd_variables(state_config)

        if unserved_fragments_number == 1:
            upd[f"devices_state_class{class_id}"].pop(index)
            update_system_state(state_config, upd, params, class_id, class_id_str="1")
            update_system_state(state_config, upd, params, class_id, class_id_str="2")

            new_state = create_state(upd["q1"], upd["q2"],
                                     upd["devices_state_class1"],
                                     upd["devices_state_class2"])

            log_leaving_demand(params.mu, new_state, class_id)

            states_and_rates[new_state] += params.mu

        else:
            leave_intensity = params.mu * unserved_fragments_number
            if class_id == 1:
                upd["devices_state_class1"][index] -= 1
            else:
                upd["devices_state_class2"][index] -= 1

            new_state = create_state(state_config["q1"], state_config["q2"],
                                     upd["devices_state_class1"],
                                     upd["devices_state_class2"])

            log_leaving_fragment(leave_intensity, new_state, class_id)

            states_and_rates[new_state] += leave_intensity
