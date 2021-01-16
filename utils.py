
def number_of_free_servers_for_server_state(params, server_state):
    number = params.devices_amount - \
             (len(server_state[0]) * params.fragments_amounts[0] +
              len(server_state[1]) * params.fragments_amounts[1])
    if number < 0:
        raise Exception("Number of free servers for states < 0, "
                        "it is not correct state")
    return number


def harmonic_sum(k: int):
    return sum(1 / i for i in range(1, k + 1))
