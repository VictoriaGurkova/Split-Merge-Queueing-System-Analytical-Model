from create_states import StateSpace

if __name__ == '__main__':
    M = 7
    a = 5
    b = 2
    cap1 = 8
    cap2 = 8
    lam1 = 1.5
    lam2 = 1.5
    mu = 3.5

    sp = StateSpace(M, a, b, cap1, cap2, lam1, lam2, mu)
    sp.start()

    print("RT", sp.RT)
    print("PF", sp.PF)
