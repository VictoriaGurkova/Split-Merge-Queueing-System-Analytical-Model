import unittest

from states import QueueingSystem


class TestStates(unittest.TestCase):

    def test_case1(self):
        date = {"M": 4, "a": 2, "b": 3, "cap1": 5, "cap2": 5, "lam1": 1, "lam2": 1, "mu": 3}

        expected_rt = 1.7832
        expected_pf = 0.1122

        qs = QueueingSystem(date["M"], date["a"], date["b"], date["cap1"],
                            date["cap2"], date["lam1"], date["lam2"], date["mu"])
        qs.calculate()
        print(qs.data)

        self.assertAlmostEqual(qs.data.RT, expected_rt, places=4)
        self.assertAlmostEqual(qs.data.PF, expected_pf, places=4)

    def test_case2(self):
        date = {"M": 7, "a": 5, "b": 2, "cap1": 8, "cap2": 8, "lam1": 1.5, "lam2": 1.5, "mu": 3.5}

        expected_rt = 1.9517
        expected_pf = 0.0631

        qs = QueueingSystem(date["M"], date["a"], date["b"], date["cap1"],
                            date["cap2"], date["lam1"], date["lam2"], date["mu"])
        qs.calculate()
        print(qs.data)

        self.assertAlmostEqual(qs.data.RT, expected_rt, places=4)
        self.assertAlmostEqual(qs.data.PF, expected_pf, places=4)


if __name__ == '__main__':
    unittest.main()
