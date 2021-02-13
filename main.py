from calculations import Calculations
from network_params import Params

if __name__ == '__main__':
    params = Params()
    calculations = Calculations(params)

    calculations.calculate()
    calculations.characters.show_all()

    print("executed")  # test flake8
