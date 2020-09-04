import matplotlib.pyplot as plt
import numpy as np

from states import QueueingSystem

if __name__ == '__main__':
    file = open('output/out.txt', 'w')

    _M = 4
    _a = 2
    _b = 3
    _capacity1 = 5
    _capacity2 = 5
    _lambda1 = 1
    _lambda2 = 1
    _mu = 3

    k = 6
    rt = np.zeros((k, k))
    rt1 = np.zeros((k, k))
    rt2 = np.zeros((k, k))
    pf = np.zeros((k, k))
    pf1 = np.zeros((k, k))
    pf2 = np.zeros((k, k))
    q1 = np.zeros((k, k))
    q2 = np.zeros((k, k))

    lambdas = list(np.linspace(0.5, 2, k))

    for i, lam1 in enumerate(lambdas):
        for j, lam2 in enumerate(lambdas):
            qs = QueueingSystem(_M, _a, _b, _capacity1, _capacity2,
                                lam1, lam2, _mu)
            qs.start()
            rt[i, j] = qs.data.RT
            rt1[i, j] = qs.data.RT1
            rt2[i, j] = qs.data.RT2
            pf[i, j] = qs.data.PF
            pf1[i, j] = qs.data.PF1
            pf2[i, j] = qs.data.PF2
            q1[i, j] = qs.data.Q1
            q2[i, j] = qs.data.Q2

    file.write('\nм.о. длительности пребывания (общее) от входящего потока')
    file.write('\nlambda2/lambda1:\n')
    for i, lam1 in enumerate(lambdas):
        for j, lam2 in enumerate(lambdas):
            s = "%8.4f" % (rt[i, j])
            file.write(s + '\t')
        file.write('\n')

    plt.plot(lambdas, rt[2], 'b')
    plt.plot(lambdas, [r[2] for r in rt], 'r')

    plt.plot(lambdas, rt[2], 'b')  # график зависимости от lambda1, lambda2 = 1.1
    plt.plot(lambdas, [r[2] for r in rt], 'r')  # график зависимости от lambda2, lambda1 = 1.1

    plt.title(f"Зависимость м.о. длит. преб. от интен. вход.")
    plt.xlabel("lambda")
    plt.ylabel("RT")
    plt.grid()
    plt.show()

    file.write('\nм.о. длительности пребывания (для 1-класса) от входящего потока')
    file.write('\nlambda2/lambda1:\n')
    for i, lam1 in enumerate(lambdas):
        for j, lam2 in enumerate(lambdas):
            s = "%8.4f" % (rt1[i, j])
            file.write(s + '\t')
        file.write('\n')

    file.write('\nм.о. длительности пребывания (для 2-класса) от входящего потока')
    file.write('\nlambda2/lambda1:\n')
    for i, lam1 in enumerate(lambdas):
        for j, lam2 in enumerate(lambdas):
            s = "%8.4f" % (rt2[i, j])
            file.write(s + '\t')
        file.write('\n')

    file.write('\nвероятность отказа (общая) от входящего потока')
    file.write('\nlambda2/lambda1:\n')
    for i, lam1 in enumerate(lambdas):
        for j, lam2 in enumerate(lambdas):
            s = "%8.4f" % (pf[i, j])
            file.write(s + '\t')
        file.write('\n')

    plt.plot(lambdas, pf[2], 'b')
    plt.plot(lambdas, [p[2] for p in pf], 'r')
    plt.title(f"Зависимость вероятности отказа")
    plt.xlabel("lambda")
    plt.ylabel("PF")
    plt.grid()
    plt.show()

    file.write('\nвероятность отказа (для 1-класса) от входящего потока')
    file.write('\nlambda2/lambda1:\n')
    for i, lam1 in enumerate(lambdas):
        for j, lam2 in enumerate(lambdas):
            s = "%8.4f" % (pf1[i, j])
            file.write(s + '\t')
        file.write('\n')

    file.write('\nвероятность отказа  (для 2-класса) от входящего потока')
    file.write('\nlambda2/lambda1:\n')
    for i, lam1 in enumerate(lambdas):
        for j, lam2 in enumerate(lambdas):
            s = "%8.4f" % (pf2[i, j])
            file.write(s + '\t')
        file.write('\n')

    file.write('\nм.о. числа треб. в очереди 1-класса от входящего потока')
    file.write('\nlambda2/lambda1:\n')
    for i, lam1 in enumerate(lambdas):
        for j, lam2 in enumerate(lambdas):
            s = "%8.4f" % (q1[i, j])
            file.write(s + '\t')
        file.write('\n')

    file.write('\nм.о. числа треб. в очереди 2-класса от входящего потока')
    file.write('\nlambda2/lambda1:\n')
    for i, lam1 in enumerate(lambdas):
        for j, lam2 in enumerate(lambdas):
            s = "%8.4f" % (q2[i, j])
            file.write(s + '\t')
        file.write('\n')

    # считаем теперь м.о. числа требований в очередях от размерности очередей
    capacitys = range(5, 21, 3)
    for i, cap1 in enumerate(capacitys):
        for j, cap2 in enumerate(capacitys):
            qs = QueueingSystem(_M, _a, _b, cap1, cap2, _lambda1, _lambda2, _mu)
            qs.start()
            q1[i, j] = qs.data.Q1
            q2[i, j] = qs.data.Q2

    file.write('\nм.о. числа треб. в очереди 1-класса от расмерности очередей')
    file.write('\ncap2/cap1:\n')
    for i, cap1 in enumerate(lambdas):
        for j, cap2 in enumerate(lambdas):
            s = "%8.4f" % (q1[i, j])
            file.write(s + '\t')
        file.write('\n')

    file.write('\nм.о. числа треб. в очереди 2-класса от расмерности очередей')
    file.write('\ncap2/cap1:\n')
    for i, cap1 in enumerate(lambdas):
        for j, cap2 in enumerate(lambdas):
            s = "%8.4f" % (q2[i, j])
            file.write(s + '\t')
        file.write('\n')

    file.close()
