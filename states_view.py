empty_set_str = u"\u2205"


def pretty_server_state(server_state):
    elements = []
    for s in server_state:
        if len(s) == 0:
            elements.append(empty_set_str)
        else:
            elements.append(str(s))
    return '(' + \
           ', '.join(elements).replace('(', '{').replace(',)', '}').replace(')', '}') \
           + ')'


def pretty_state(state):
    queue_state = state[0]
    server_state = state[1]
    return '(' + str(queue_state) + ': ' + \
           pretty_server_state(server_state) + ')'
