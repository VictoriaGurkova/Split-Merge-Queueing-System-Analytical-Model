import unittest

from create_states import StateSpace


class TestStates(unittest.TestCase):

    def test_case1(self):
        date = {"M": 4, "a": 2, "b": 3, "cap1": 5, "cap2": 5, "lam1": 1, "lam2": 1, "mu": 3}

        ans_rt = 1.7833
        ans_pf = 0.1122

        sp = StateSpace(date["M"], date["a"], date["b"], date["cap1"],
                        date["cap2"], date["lam1"], date["lam2"], date["mu"])
        sp.start()

        self.assertEqual(round(sp.RT, 4), ans_rt)
        self.assertEqual(round(sp.PF, 4), ans_pf)

    def test_case2(self):
        date = {"M": 7, "a": 5, "b": 2, "cap1": 8, "cap2": 8, "lam1": 1.5, "lam2": 1.5, "mu": 3.5}

        ans_rt = 1.9516
        ans_pf = 0.0631

        sp = StateSpace(date["M"], date["a"], date["b"], date["cap1"],
                        date["cap2"], date["lam1"], date["lam2"], date["mu"])
        sp.start()

        self.assertEqual(round(sp.RT, 4), ans_rt)
        self.assertEqual(round(sp.PF, 4), ans_pf)


if __name__ == '__main__':
    unittest.main()
