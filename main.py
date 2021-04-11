from pprint import pprint

from calculations import Calculations
from network_params import Params
from states_policy import StatesPolicy
from states_policy import get_policed_states, get_strategy

if __name__ == '__main__':
    params = Params(mu=3, lambda1=.5, lambda2=1,
                    servers_number=5,
                    fragments_numbers=[2, 3],
                    queues_capacities=[1, 1])
    calculations = Calculations(params)

    all_states = calculations.get_all_states()
    states_with_policy = get_policed_states(all_states, params)
    print("All states where policy is possible:")
    pprint(states_with_policy)

    strategies = get_strategy(states_with_policy)
    print("\nVarious combinations of policies:")
    pprint(strategies)

    states_policy = StatesPolicy(tuple(), states_with_policy, params)

    for strategy in strategies[-1:]:
        states_policy.strategy = strategy
        print(strategy)
        calculations = Calculations(params)
        calculations.calculate(states_policy)
        performance_measures = calculations.performance_measures
        print(performance_measures, "\n")
    # записать в файл
    # стратегия -> характеристики (и так для каждой страетигии)

    print("executed")
