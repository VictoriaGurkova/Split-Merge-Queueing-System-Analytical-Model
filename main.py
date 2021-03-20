from calculations import Calculations
from network_params import Params

if __name__ == '__main__':
    params = Params(mu=3, lambda1=.5, lambda2=1,
                    servers_number=5,
                    fragments_numbers=[2, 3],
                    queues_capacities=[1, 1])
    calculations = Calculations(params)

    calculations.calculate()
    print(calculations.characters)

    print("executed")
