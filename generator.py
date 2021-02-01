import os

import numpy as np
from scipy.linalg import expm

from handlers import get_achievable_states
from logs import log_message


def create_generator(states, params):
    n = len(states)
    generator = np.zeros((n, n))
    for i, current_state in enumerate(states):
        states_and_rates = get_achievable_states(params, current_state)
        for state, rate in states_and_rates.items():
            j = states.index(state)
            generator[i, j] += rate

    for i, row in enumerate(generator):
        generator[i, i] = -sum(row)

    return generator


def get_stationary_distribution(states, params):
    generator = create_generator(states, params)
    log_message(f'Q = {generator}')
    np.savetxt("output/generator/Q.txt", generator, fmt='%0.0f')
    return expm(generator * 100000000000)[0]
