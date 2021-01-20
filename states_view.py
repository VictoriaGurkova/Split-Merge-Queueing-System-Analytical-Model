import logging

empty_set_str = u"\u2205"

logger = logging.getLogger()


def print_states(states, func):
    for state_id, state in enumerate(states):
        logger.debug(f'S {state_id}= {func(state)}')


def pretty_devices_state(devices_state):
    elements = []
    for s in devices_state:
        if len(s) == 0:
            elements.append(empty_set_str)
        else:
            elements.append(str(s))
    return '(' + \
           ', '.join(elements).replace('(', '{').replace(',)', '}').replace(')', '}') \
           + ')'


def pretty_state(state):
    queues_state = state[0]
    devices_state = state[1]
    return '(' + str(queues_state) + ': ' + \
           pretty_devices_state(devices_state) + ')'
