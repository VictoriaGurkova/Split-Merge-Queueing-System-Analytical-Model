import unittest

from network_params import Params
from states import QueueingSystem


def get_data(params):
    system = QueueingSystem(params)
    system.calculate()
    print(system.data)
    return system.data


class TestStates(unittest.TestCase):

    def test_case1(self):
        params = Params(lambda1=1, lambda2=1, mu=3, devices_amount=4,
                        fragments_amounts=[2, 3], queues_capacities=[5, 5])
        test_data = {
            "params": params,
            "expected_rt": 1.7833,
            "expected_fp": 0.1122
        }

        self.compare_results(test_data)

    def test_case2(self):
        params = Params(lambda1=1.5, lambda2=1.5, mu=3.5, devices_amount=7,
                        fragments_amounts=[5, 2], queues_capacities=[8, 8])
        test_data = {
            "params": params,
            "expected_rt": 1.9517,
            "expected_fp": 0.0631
        }

        self.compare_results(test_data)

    def compare_results(self, data):
        result = get_data(data["params"])
        self.assertAlmostEqual(result.response_time, data["expected_rt"], places=4)
        self.assertAlmostEqual(result.failure_probability, data["expected_fp"], places=4)


if __name__ == '__main__':
    unittest.main()
