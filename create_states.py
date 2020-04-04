import itertools
from pprint import pprint


def get_lots_of_fragments(amount_of_demands, fragments_in_class):
    return set(itertools.combinations_with_replacement(range(1, fragments_in_class + 1), amount_of_demands))


def get_all_state_with_queues(all_state: set, queue_capacity: list, M, a, b):
    all_state_with_queues = list()
    queue_state = set(itertools.product([x for x in range(queue_capacity[0] + 1)],
                                        [x for x in range(queue_capacity[1] + 1)]))

    for q_state in queue_state:
        for state in all_state:
            if possible_state(q_state, state, M, a, b):
                all_state_with_queues.append({q_state: state})

    return all_state_with_queues


def possible_state(q_state, state, M, a, b):
    number_of_occupied = len(state[0]) * a + len(state[1]) * b
    if q_state[0] and M - number_of_occupied >= a:
        return False
    if q_state[1] and M - number_of_occupied >= b:
        return False
    return True


def get_achievable_states(all_states: list, current_state: map, a: int, b: int):
    achievable_states = set()
    for state in all_states:
        if can_achieve(current_state, state, a, b):
            achievable_states.add(state)
    return achievable_states


def can_achieve(current_state: map, state: map, a: int, b: int):
    difference1 = 0
    difference2 = 0
    # приход требования класса 1
    if len(state[0]) - len(current_state[0]) == 1 and state[0][-1] == a and len(state[1]) - len(current_state[1]) == 0 \
            and current_state[1][:] == state[1][:]:
        difference1 += 1
    # приход требования класса 2
    if len(state[1]) - len(current_state[1]) == 1 and state[1][-1] == b and len(state[0]) - len(current_state[0]) == 0 \
            and current_state[0][:] == state[0][:]:
        difference2 += 1
    # уход требования класса 1
    if len(current_state[0]) - len(state[0]) == 1 and current_state[1][:] == state[1][:]:
        if current_state[0][:-1] == state[0][:]:
            difference1 += current_state[0][-1]
    # уход требования класса 2
    if len(current_state[1]) - len(state[1]) == 1 and current_state[0][:] == state[0][:]:
        if current_state[1][:-1] == state[1][:]:
            difference2 += current_state[1][-1]
    # завершение обслуживания фргмента требований 1го класса
    if len(current_state[0]) == len(state[0]) and current_state[1][:] == state[1][:]:
        for i in range(len(state[0])):
            if current_state[0][i] - state[0][i] > 0:
                difference1 += current_state[0][i] - state[0][i]
    # завершение обслуживания фргмента требований 2го класса
    if len(current_state[1]) == len(state[1]) and current_state[0][:] == state[0][:]:
        for i in range(len(state[1])):
            if current_state[1][i] - state[1][i] > 0:
                difference2 += current_state[1][i] - state[1][i]

    return (difference1 + difference2) == 1


def main():
    all_states = set()
    # число приборов
    M = 3  # int(input("M = "))
    # число фрагментов в 1м классе
    a = 2  # int(input("a = "))
    # число фрагментов во 2м классе
    b = 1  # int(input("b = "))
    # максимальное число требований 1го класса, которое может быть на приборах
    x = M // a
    # максимальное число требований 2го класса, которое может быть на приборах
    y = M // b

    # вместимость очереди 1го класса
    q1 = 2
    # вместимость очереди 2го класса
    q2 = 2

    queue_capacity = [q1, q2]

    for i in range(x + 1):
        for j in range(y + 1):
            # число фрагментов которое может находиться на обслуживании
            z = a * i + b * j
            if M < z:
                continue

            X = sorted(get_lots_of_fragments(i, a))
            Y = sorted(get_lots_of_fragments(j, b))
            all_states.update(itertools.product(X, Y))

    print("Состояния фрагментов на системах (не включая очереди):  ")
    for state in all_states:
        print(f"S{list(all_states).index(state)} =", state)

    all_state_with_queues = get_all_state_with_queues(all_states, queue_capacity, M, a, b)
    print("\nСостояния системы вместе с очередями:")

    # pprint(all_state_with_queues)
    count = 0
    for state in all_state_with_queues:
        print(f"S{count} =", state)
        count += 1

    # for state in all_state_with_queues:
    #     print(f"Текущее состояние S{count}:", state)
    #     pprint("Смежные состояния:", get_achievable_states(all_state_with_queues, state, a, b))


if __name__ == '__main__':
    main()
