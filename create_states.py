import itertools

empty_set_str = u"\u2205"


def pretty_server_state(server_state):
    elements = []
    for s in server_state:
        if len(s) == 0:
            elements.append(empty_set_str)
        else:
            elements.append(str(s))
    # склеиваем все вместе и заменяем скобки list на фигурные для множества
    return '(' + \
           ', '.join(elements).replace('(', '{').replace(',)', '}').replace(')', '}') \
           + ')'


def pretty_state(state):
    queue_state = state[0]
    server_state = state[1]
    return '(' + str(queue_state) + ': ' + pretty_server_state(server_state) + ')'


# не понимаю из названия предназначение функции
def get_lots_of_fragments(amount_of_demands, fragments_in_class):
    return list(itertools.combinations_with_replacement(range(1, fragments_in_class + 1), amount_of_demands))


def get_all_state_with_queues(server_states: set,
                              queue_capacity: list,
                              M, a, b):
    states = []
    # так симпатичнее
    queue_states = set(itertools.product(range(queue_capacity[0] + 1), range(queue_capacity[0] + 1)))

    for q_state in queue_states:
        for server_state in server_states:
            # вы же понимаете, что это не самый оптимальный метод генерации
            # гененируется слишком много лишних состояний, которые потом фильтруем
            # но пусть пока будет так
            if is_possible_state(q_state, server_state, M, a, b):
                # зачем тут был dict? для красоты вывода на консоль?
                states.append((q_state, server_state))
    return states


def is_possible_state(q_state, state, M, a, b):
    number_of_free_servers = number_of_free_servers_for_server_state(state, M, a, b)
    if q_state[0] and number_of_free_servers >= a:
        return False
    if q_state[1] and number_of_free_servers >= b:
        return False
    return True


def get_achievable_states(current_state: tuple,
                          M: int,
                          a: int, b: int,
                          queue_capacity: list):
    print('#' * 100)
    print('Рассмотрим состояние ' + pretty_state(current_state))
    # не будем делать никаких проверок, это снова слишком долго
    # быстрее построить эти состояние перебирая все события, которые могут произойти
    # не стал разбивать на отдельные функции из-за необходимости таскать кучу параметров
    # так как все парметры не в классе
    capacity1 = queue_capacity[0]
    capacity2 = queue_capacity[1]

    # получаем различные характеристики состояния
    q1 = current_state[0][0]
    print('q1 = ', q1)
    q2 = current_state[0][1]
    print('q1 = ', q2)
    server_state = current_state[1]
    print('server_state = ', server_state)

    number_of_free_servers = number_of_free_servers_for_server_state(server_state, M, a, b)
    print("Число свободных приборов", number_of_free_servers)

    # ПОСТУПЛЕНИЕ
    # первый класс - поступление требований
    # есть приборов не хватает, то идем в очередь, если размер очереди позволят
    print("ПОСТУПЛЕНИЕ")
    if q1 != capacity1:
        # идем в очередь
        if number_of_free_servers < a:
            new_state = create_state(q1 + 1, q2, server_state[0], server_state[1])
            print('Поступление требования первого класса в очередь  с какой-то интенсивностью и переход в стояние ',
                  new_state, "  pretty-form = ", pretty_state(new_state))
        # идем на приборы - добавление во множество новое требование - т.е. новое количество фрагментов
        else:
            updated_first_demands_tasks = server_state[0]
            updated_first_demands_tasks = updated_first_demands_tasks + (a,)
            new_state = create_state(q1, q2, updated_first_demands_tasks, server_state[1])
            print('Поступление требования первого класса и немедленное начало его обслуживания'
                  '  с какой-то интенсивностью и переход в стояние ',
                  new_state, "  pretty-form = ", pretty_state(new_state))
    else:
        print("Очередь заполнена - требование потерялось")

    # ЗАВЕРШЕНИЕ ОБСЛУЖИВАНИЯ
    # первый класс - завершение обслуживания одного из фрагментов или даже целого требования
    # на приборах есть несколько требований первого класса,
    # в каждом требовании фрагменты, если на приборах
    print('УХОД')
    for number_of_lost_tasks_in_demand in server_state[0]:
        # обнаружил требование первого класса, в нем активны tasks фрагментов
        if number_of_lost_tasks_in_demand == 1:
            print('Остался один фрагмент - нужно удалить все требование после того как фрагмент уйдет')
        else:
            print('Остался не единственный фрагмент - можно просто убрать один и уменьшить их число на единицу')

    return


def number_of_free_servers_for_server_state(server_state, M, a, b):
    number = M - len(server_state[0]) * a + len(server_state[1]) * b
    if number < 0:
        raise Exception("Number of free servers for states < 0, it is not correct state")
    return number


def create_state(q1, q2, first_class, second_class):
    return (q1, q2), (first_class, second_class)


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
    server_states = set()
    # число приборов
    M = 5  # int(input("M = "))
    # число фрагментов в 1м классе
    a = 2  # int(input("a = "))
    # число фрагментов во 2м классе
    b = 1  # int(input("b = "))
    # максимальное число требований 1го класса, которое может быть на приборах
    x = M // a
    print('Максимальное число требований 1го класса = ', x)
    # максимальное число требований 2го класса, которое может быть на приборах
    y = M // b
    print('Максимальное число требований 2го класса = ', y)

    # вместимость очереди 1го класса
    capacity1 = 2
    # вместимость очереди 2го класса
    capacity2 = 2

    lambda1 = 1
    lambda2 = 2
    mu = 3

    queue_capacity = [capacity1, capacity2]

    # следует вынести в отдельную функцию
    for i in range(x + 1):
        for j in range(y + 1):
            # общее число фрагментов в системе
            total_number_of_tasks = a * i + b * j
            if M < total_number_of_tasks:
                continue
            X = sorted(get_lots_of_fragments(i, a))
            Y = sorted(get_lots_of_fragments(j, b))
            server_states.update(itertools.product(X, Y))

    print("Состояния фрагментов на системах (не включая очереди): (вывожу в красивом и не очень виде, чтобы понимать"
          "используемые структуры данных в состоянии "
          "(кортеж или лист или что-то еще, всегда понимаю что и где лежит и по какому индексу могу найти)  ")
    # Это слишком сложный вариант вывода
    # for state in all_states:
    #     print(f"S{list(all_states).index(state)} =", state)

    # enumerate создает пары - номер и элемент чего-то
    for state_id, state in enumerate(server_states):
        print('S' + str(state_id), '= ', pretty_server_state(state), '|    \t', state)

    states = get_all_state_with_queues(server_states, queue_capacity, M, a, b)
    print("\nСостояния системы вместе с очередями:")

    # pprint(all_state_with_queues)
    for state_id, state in enumerate(states):
        print('S' + str(state_id), '= ', pretty_state(state), '|    \t', state)

    for state in states:
        get_achievable_states(state, M, a, b, queue_capacity)


if __name__ == '__main__':
    main()
