import itertools

from network_params import Params


class StatesPolicy:
    def __init__(self, strategy: tuple, states_with_policy: list, params: Params):
        self.strategy: tuple = strategy
        self.states_with_policy: list = states_with_policy
        self.params: Params = params

        self.adjacent_states: dict = {state: self.define_adjacent_states(state) for state in states_with_policy}

        for state in self.adjacent_states.keys():
            print("\n", " " * 14, state)
            for i in self.adjacent_states[state]:
                print(i, end=" " * 10)
            print()

    def define_adjacent_states(self, state: tuple) -> list:
        last_fragment = 1
        adjacent_states = list()

        index = 0
        for server_state in state[1]:
            if last_fragment in server_state and self.have_a_choice(state, index):
                # generate state when first class is taken
                adjacent_states.append(self.get_state_after_leaving(state[0], state[1], index, 0))
                # generate state when second class is taken
                adjacent_states.append(self.get_state_after_leaving(state[0], state[1], index, 1))
                index = 0
                break
            index += 1

        return adjacent_states

    def have_a_choice(self, state: tuple, class_id: int) -> bool:
        return self.get_free_servers_after_leaving(state[1], class_id) >= max(self.params.fragments_numbers)

    def get_free_servers_after_leaving(self, server_state, class_id):
        return self.params.servers_number - (
                len(server_state[0]) * self.params.fragments_numbers[0] +
                len(server_state[1]) * self.params.fragments_numbers[1]) + \
               self.params.fragments_numbers[class_id]

    def get_state_after_leaving(self, queues_state, server_state, class_id_leave, class_id_take) -> tuple:
        if class_id_leave == 0:
            if class_id_take == 0:

                # TODO: export in def
                possible_demands_number_for_taking = \
                    self.get_free_servers_after_leaving(server_state, 0) // self.params.fragments_numbers[0]
                available_demands_number_for_taking = \
                    queues_state[0] if queues_state[0] <= possible_demands_number_for_taking \
                        else possible_demands_number_for_taking
                taken_demands = (self.params.fragments_numbers[0],) * available_demands_number_for_taking

                return tuple(((queues_state[0] - available_demands_number_for_taking, queues_state[1]),
                              ((*server_state[0][1:], *taken_demands), server_state[1])))
            else:

                possible_demands_number_for_taking = \
                    self.get_free_servers_after_leaving(server_state, 0) // self.params.fragments_numbers[1]
                available_demands_number_for_taking = \
                    queues_state[1] if queues_state[1] <= possible_demands_number_for_taking \
                        else possible_demands_number_for_taking
                taken_demands = (self.params.fragments_numbers[1],) * available_demands_number_for_taking

                return tuple(((queues_state[0], queues_state[1] - available_demands_number_for_taking),
                              ((server_state[0][1:]), (*server_state[1], *taken_demands))))
        else:
            if class_id_take == 0:

                possible_demands_number_for_taking = \
                    self.get_free_servers_after_leaving(server_state, 1) // self.params.fragments_numbers[0]
                available_demands_number_for_taking = \
                    queues_state[0] if queues_state[0] <= possible_demands_number_for_taking \
                        else possible_demands_number_for_taking
                taken_demands = (self.params.fragments_numbers[0],) * available_demands_number_for_taking

                return tuple(((queues_state[0] - available_demands_number_for_taking, queues_state[1]),
                              ((*server_state[0], *taken_demands), server_state[1][1:])))
            else:

                possible_demands_number_for_taking = \
                    self.get_free_servers_after_leaving(server_state, 1) // self.params.fragments_numbers[1]
                available_demands_number_for_taking = \
                    queues_state[1] if queues_state[1] <= possible_demands_number_for_taking \
                        else possible_demands_number_for_taking
                taken_demands = (self.params.fragments_numbers[1],) * available_demands_number_for_taking

                return tuple(((queues_state[0], queues_state[1] - available_demands_number_for_taking),
                              (server_state[0], (*server_state[1][1:], *taken_demands))))


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
            # policy is applied if a class with a large fragments number leaves
            if last_fragment in state[1][class_index_with_max_fragments_number]:
                policed_states.append(state)
            # policy is applied if a class with fewer fragments number leaves and there are free services
            else:
                leaving_fragments_number = min(params.fragments_numbers)
                if free_servers_number + leaving_fragments_number >= max_fragments_number:
                    policed_states.append(state)

    return policed_states


def get_strategy(states: list):
    states_number = len(states)
    strategies = list(itertools.product([0, 1], repeat=states_number))

    return strategies
