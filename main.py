from calculations import Calculations
from experiment.capacity_dependency import CapacityDependency
from experiment.intensity_dependency import IntensityDependency
from network_params import Params


if __name__ == '__main__':
    params = Params()

    print("Зависимость от интенсивностей входящего потока:")
    intensity_dep = IntensityDependency()

    for i, lam1 in enumerate(intensity_dep.lambdas):
        for j, lam2 in enumerate(intensity_dep.lambdas):
            params.lambda1 = lam1
            params.lambda2 = lam2
            calculations = Calculations(params)
            calculations.calculate()

            print(f"measures for {calculations} \n{calculations.characters}")

            intensity_dep.response_time[i, j] = calculations.characters.response_time
            intensity_dep.response_time1[i, j] = calculations.characters.response_time1
            intensity_dep.response_time2[i, j] = calculations.characters.response_time2

            intensity_dep.failure_prob[i, j] = calculations.characters.failure_prob
            intensity_dep.failure_prob1[i, j] = calculations.characters.failure_prob1
            intensity_dep.failure_prob2[i, j] = calculations.characters.failure_prob2

            intensity_dep.avg_queue1[i, j] = calculations.characters.avg_queue1
            intensity_dep.avg_queue2[i, j] = calculations.characters.avg_queue2

    intensity_dep.save_results()
    intensity_dep.draw_rt()
    intensity_dep.draw_fp()

    print("Зависимость от длины очередей:")
    capacity_dep = CapacityDependency()

    for i, capacity1 in enumerate(capacity_dep.capacities):
        for j, capacity2 in enumerate(capacity_dep.capacities):
            params.queues_capacities = [capacity1, capacity2]
            calculations = Calculations(params)

            calculations.calculate()

            print(f"measures for {calculations} \n{calculations.characters}")

            capacity_dep.response_time[i, j] = calculations.characters.response_time
            capacity_dep.response_time1[i, j] = calculations.characters.response_time1
            capacity_dep.response_time2[i, j] = calculations.characters.response_time2

            capacity_dep.failure_prob[i, j] = calculations.characters.failure_prob
            capacity_dep.failure_prob1[i, j] = calculations.characters.failure_prob1
            capacity_dep.failure_prob2[i, j] = calculations.characters.failure_prob2

            capacity_dep.avg_queue1[i, j] = calculations.characters.avg_queue1
            capacity_dep.avg_queue2[i, j] = calculations.characters.avg_queue2

    capacity_dep.save_results()
    print("executed")

