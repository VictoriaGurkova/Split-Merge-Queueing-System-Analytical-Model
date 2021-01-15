import unittest

from states import QueueingSystem


def get_data(params):
    system = QueueingSystem(params["M"], params["a"], params["b"], params["c1"],
                            params["c2"], params["l1"], params["l2"], params["mu"])
    system.calculate()
    print(system.data)
    return system.data


class TestStates(unittest.TestCase):

    def test_case1(self):
        test_data = {
            "params": dict(M=4, a=2, b=3, c1=5, c2=5, l1=1, l2=1, mu=3),
            "expected_rt": 1.7833,
            "expected_fp": 0.1122
        }

        self.compare_results(test_data)

    def test_case2(self):
        test_data = {
            "params": dict(M=7, a=5, b=2, c1=8, c2=8, l1=1.5, l2=1.5, mu=3.5),
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
