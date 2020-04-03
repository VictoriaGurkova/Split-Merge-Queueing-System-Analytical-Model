import itertools
from math import fabs


def get_lots_of_fragments(amount_of_demands, fragments_in_class):
    return set(itertools.combinations_with_replacement(range(1, fragments_in_class + 1), amount_of_demands))


def get_achievable_states(all_states: set, current_state: tuple, a: int, b: int):
    achievable_states = set()
    for state in all_states:
        if can_achieve(current_state, state, a, b):
            achievable_states.add(state)
    return achievable_states


def can_achieve(current_state, state, a, b):
    difference1 = 0
    difference2 = 0
    # приход требования класса 1
    if len(state[0]) - len(current_state[0]) == 1 and state[0][-1] == a and len(state[1]) - len(current_state[1]) == 0:
        difference1 += 1
    # приход требования класса 2
    if len(state[1]) - len(current_state[1]) == 1 and state[1][-1] == b and len(state[0]) - len(current_state[0]) == 0:
        difference2 += 1
    # уход требования класса 1
    if len(current_state[0]) - len(state[0]) == 1 and current_state[1][:] == state[1][:]:
        if current_state[0][:-1] == state[0][:]:
            difference1 += 1
    # уход требования класса 2
    if len(current_state[1]) - len(state[1]) == 1 and current_state[0][:] == state[0][:]:
        if current_state[1][:-1] == state[1][:]:
            difference2 += 1
    # завершение обслуживания фргмента требований 1го класса
    if len(current_state[0]) == len(state[0]) and current_state[1][:] == state[1][:]:
        for i in range(len(state[0])):
            if current_state[0][i] - state[0][i] > 0:
                difference1 += 1
    # завершение обслуживания фргмента требований 2го класса
    if len(current_state[1]) == len(state[1]) and current_state[0][:] == state[0][:]:
        for i in range(len(state[1])):
            if current_state[1][i] - state[1][i] > 0:
                difference2 += 1

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

    for i in range(x + 1):
        for j in range(y + 1):
            # число фрагментов которое может находиться на обслуживании
            z = a * i + b * j
            if M < z:
                continue

            print('i =', i, 'j =', j)
            X = sorted(get_lots_of_fragments(i, a))
            Y = sorted(get_lots_of_fragments(j, b))
            all_states.update(itertools.product(X, Y))

    for state in all_states:
        print(f"S{list(all_states).index(state)} =", state)

    print(get_achievable_states(all_states, tuple(list(all_states)[0]), a, b))


if __name__ == '__main__':
    main()