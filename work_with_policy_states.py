import itertools
from pprint import pprint

from network_params import Params


def get_policed_states(states: list, params: Params) -> list:
    max_fragments_number = max(params.fragments_numbers)
    class_index_with_max_fragments_number = params.fragments_numbers.index(max_fragments_number)

    last_fragment = 1
    policed_states = []
    for state in states:
        all_queues_not_empty = state[0][0] and state[0][1]
        last_fragment_of_any_demand = last_fragment in state[1][0] or last_fragment in state[1][1]
        if all_queues_not_empty and last_fragment_of_any_demand:
            free_servers_number = params.servers_number - (
                    len(state[1][0]) * params.fragments_numbers[0] +
                    len(state[1][1]) * params.fragments_numbers[1])
            # если уходит больший класс, то есть управление
            if last_fragment in state[1][class_index_with_max_fragments_number]:
                policed_states.append(state)
            # если уходит меньший класс и есть свободные приборы, то есть управление
            else:
                leaving_fragments_number = min(params.fragments_numbers)
                if free_servers_number + leaving_fragments_number >= max_fragments_number:
                    policed_states.append(state)

    [print(state) for state in policed_states]
    get_strategy(policed_states)
    
    return policed_states


def get_strategy(states: list):
    states_number = len(states)
    strategies = list(itertools.product([0, 1], repeat=states_number))
    pprint(strategies)
    print(len(strategies))

    return strategies
