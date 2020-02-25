import itertools


def get_lots_of_fragments(amount_of_demands, fragments_in_class):
    return set(itertools.product(range(1, fragments_in_class + 1), repeat=amount_of_demands))


# число приборов
M = 10  # int(input("M = "))
# число фрагментов в 1м классе
a = 4  # int(input("a = "))
# число фрагментов во 2м классе
b = 3  # int(input("b = "))
# максимальное число требований 1го класса, которое может быть на приборах
x = M // a
# максимальное число требований 2го класса, которое может быть на приборах
y = M // b

X = set()
Y = set()
all_states = set()

for i in range(x + 1):
    for j in range(y + 1):
        # число фрагментов которое может находиться на обслуживании
        z = a * i + b * j
        if M < z:
            continue
        print('i =', i, 'j =', j)
        X = sorted(get_lots_of_fragments(i, a))
        print(X)
        Y = sorted(get_lots_of_fragments(j, b))
        print(Y)
        all_states.update(itertools.product(X, Y))

for state in all_states:
    print(state)
