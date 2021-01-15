import unittest

from states import QueueingSystem


def calculate_data(config):
    qs = QueueingSystem(config["M"], config["a"], config["b"], config["c1"],
                        config["c2"], config["l1"], config["l2"], config["mu"])
    qs.calculate()
    print(qs.data)
    return qs.data


class TestStates(unittest.TestCase):

    def test_case1(self):
        data = {
            "config": dict(M=4, a=2, b=3, c1=5, c2=5, l1=1, l2=1, mu=3),
            "expected_rt": 1.7833,
            "expected_pf": 0.1122
        }

        result = calculate_data(data["config"])
        self.assert_equals(result, data)

    def test_case2(self):
        data = {
            "config": dict(M=7, a=5, b=2, c1=8, c2=8, l1=1.5, l2=1.5, mu=3.5),
            "expected_rt": 1.9516,
            "expected_pf": 0.0631
        }

        result = calculate_data(data["config"])
        self.assert_equals(result, data)

    def assert_equals(self, result, data):
        self.assertAlmostEqual(result.RT, data["expected_rt"], places=4)
        self.assertAlmostEqual(result.PF, data["expected_pf"], places=4)


if __name__ == '__main__':
    unittest.main()
