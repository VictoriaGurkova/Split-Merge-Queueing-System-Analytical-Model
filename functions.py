import itertools

empty_set_str = u"\u2205"


def pretty_server_state(server_state):
    elements = []
    for s in server_state:
        if len(s) == 0:
            elements.append(empty_set_str)
        else:
            elements.append(str(s))

    return '(' + \
           ', '.join(elements).replace('(', '{').\
               replace(',)', '}').replace(')', '}') \
           + ')'


def pretty_state(state):
    queue_state = state[0]
    server_state = state[1]
    return '(' + str(queue_state) + ': ' + \
           pretty_server_state(server_state) + ')'


def get_lots_of_fragments(amount_of_demands,
                          fragments_in_class):
    return list(itertools.
                combinations_with_replacement(
        range(1, fragments_in_class + 1), amount_of_demands))


def create_state(q1, q2, first_class, second_class):
    return (q1, q2), (tuple(sorted(first_class)),
                      tuple(sorted(second_class)))


def harmonic_sum(k: int):
    return sum(1 / i for i in range(1, k + 1))

