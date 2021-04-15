from calculations import Calculations
from experiment.capacity_dependency import CapacityDependency
from experiment.rate_dependency import RateDependency
from network_params import Params


if __name__ == '__main__':
    params = Params(mu=3, lambda1=.5, lambda2=1,
                    servers_number=4,
                    fragments_numbers=[3, 2],
                    queues_capacities=[10, 30])

    print("Dependence on the arrival flow rates:")
    rate_dep = RateDependency()

    for i, lam1 in enumerate(rate_dep.lambdas):
        for j, lam2 in enumerate(rate_dep.lambdas):
            params.lambda1 = lam1
            params.lambda2 = lam2
            calculations = Calculations(params)
            calculations.calculate(strategy)

            print(f"measures for {calculations} \n{calculations.performance_measures}")

            rate_dep.response_time[i, j] = calculations.performance_measures.response_time
            rate_dep.response_time1[i, j] = calculations.performance_measures.response_time1
            rate_dep.response_time2[i, j] = calculations.performance_measures.response_time2

            rate_dep.failure_prob[i, j] = calculations.performance_measures.failure_probability
            rate_dep.failure_prob1[i, j] = calculations.performance_measures.failure_probability1
            rate_dep.failure_prob2[i, j] = calculations.performance_measures.failure_probability2

            rate_dep.avg_queue1[i, j] = calculations.performance_measures.avg_queue1
            rate_dep.avg_queue2[i, j] = calculations.performance_measures.avg_queue2

    rate_dep.save_results()
    rate_dep.draw_rt()
    rate_dep.draw_fp()

    print("Dependence on the queues capacity:")
    capacity_dep = CapacityDependency()

    for i, capacity1 in enumerate(capacity_dep.capacities):
        for j, capacity2 in enumerate(capacity_dep.capacities):
            params.queues_capacities = [capacity1, capacity2]
            calculations = Calculations(params)

            calculations.calculate(strategy)

            print(f"measures for {calculations} \n{calculations.performance_measures}")

            capacity_dep.response_time[i, j] = calculations.performance_measures.response_time
            capacity_dep.response_time1[i, j] = calculations.performance_measures.response_time1
            capacity_dep.response_time2[i, j] = calculations.performance_measures.response_time2

            capacity_dep.failure_prob[i, j] = calculations.performance_measures.failure_probability
            capacity_dep.failure_prob1[i, j] = calculations.performance_measures.failure_probability1
            capacity_dep.failure_prob2[i, j] = calculations.performance_measures.failure_probability2

            capacity_dep.avg_queue1[i, j] = calculations.performance_measures.avg_queue1
            capacity_dep.avg_queue2[i, j] = calculations.performance_measures.avg_queue2

    capacity_dep.save_results()
    print("executed")

