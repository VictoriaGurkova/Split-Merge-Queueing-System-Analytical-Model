import logging

import matplotlib.pyplot as plt
import numpy as np

from network_params import Params
from states import QueueingSystem

root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
handler = logging.FileHandler('app.log', 'w', 'utf-8')  # or whatever
handler.setFormatter(logging.Formatter('%(message)s'))  # or whatever
root_logger.addHandler(handler)

if __name__ == '__main__':
    file = open('output/out.txt', 'w', encoding='utf-8')

    # test for github №3
    params = Params()
    qs = QueueingSystem(params)
    qs.calculate()

    # k = 6
    # rt = np.zeros((k, k))
    # rt1 = np.zeros((k, k))
    # rt2 = np.zeros((k, k))
    # pf = np.zeros((k, k))
    # pf1 = np.zeros((k, k))
    # pf2 = np.zeros((k, k))
    # q1 = np.zeros((k, k))
    # q2 = np.zeros((k, k))
    #
    # lambdas = list(np.linspace(0.5, 2, k))
    #
    # print("Зависимость от интенсивностей входящего потока")
    # for i, lam1 in enumerate(lambdas):
    #     for j, lam2 in enumerate(lambdas):
    #         qs = QueueingSystem(system)
    #         qs.calculate()
    #         print(f"measures for {qs} \n{qs.data}")
    #         rt[i, j] = qs.data.response_time
    #         rt1[i, j] = qs.data.response_time1
    #         rt2[i, j] = qs.data.response_time2
    #         pf[i, j] = qs.data.PF
    #         pf1[i, j] = qs.data.PF1
    #         pf2[i, j] = qs.data.PF2
    #         q1[i, j] = qs.data.demands_count1
    #         q2[i, j] = qs.data.demands_count2
    #
    # file.write('\nм.о. длительности пребывания (общее) от входящего потока')
    # file.write('\nlambda2/lambda1:\n')
    # for i, lam1 in enumerate(lambdas):
    #     for j, lam2 in enumerate(lambdas):
    #         s = "%8.4f" % (rt[i, j])
    #         file.write(s + '\t')
    #     file.write('\n')
    #
    # plt.plot(lambdas, rt[2], 'b')
    # plt.plot(lambdas, [r[2] for r in rt], 'r')
    #
    # plt.plot(lambdas, rt[2], 'b')  # график зависимости от lambda1, lambda2 = 1.1
    # plt.plot(lambdas, [r[2] for r in rt], 'r')  # график зависимости от lambda2, lambda1 = 1.1
    #
    # plt.title(f"Зависимость м.о. длит. преб. от интен. вход.")
    # plt.xlabel("lambda")
    # plt.ylabel("RT")
    # plt.grid()
    # plt.savefig('output/RT-lambda.png')
    # plt.show()
    #
    # file.write('\nм.о. длительности пребывания (для 1-класса) от входящего потока')
    # file.write('\nlambda2/lambda1:\n')
    # for i, lam1 in enumerate(lambdas):
    #     for j, lam2 in enumerate(lambdas):
    #         s = "%8.4f" % (rt1[i, j])
    #         file.write(s + '\t')
    #     file.write('\n')
    #
    # file.write('\nм.о. длительности пребывания (для 2-класса) от входящего потока')
    # file.write('\nlambda2/lambda1:\n')
    # for i, lam1 in enumerate(lambdas):
    #     for j, lam2 in enumerate(lambdas):
    #         s = "%8.4f" % (rt2[i, j])
    #         file.write(s + '\t')
    #     file.write('\n')
    #
    # file.write('\nвероятность отказа (общая) от входящего потока')
    # file.write('\nlambda2/lambda1:\n')
    # for i, lam1 in enumerate(lambdas):
    #     for j, lam2 in enumerate(lambdas):
    #         s = "%8.4f" % (pf[i, j])
    #         file.write(s + '\t')
    #     file.write('\n')
    #
    # plt.plot(lambdas, pf[2], 'b')
    # plt.plot(lambdas, [p[2] for p in pf], 'r')
    # plt.title(f"Зависимость вероятности отказа")
    # plt.xlabel("lambda")
    # plt.ylabel("PF")
    # plt.grid()
    # plt.savefig('output/pf-lambda.png')
    # plt.show()
    #
    # file.write('\nвероятность отказа (для 1-класса) от входящего потока')
    # file.write('\nlambda2/lambda1:\n')
    # for i, lam1 in enumerate(lambdas):
    #     for j, lam2 in enumerate(lambdas):
    #         s = "%8.4f" % (pf1[i, j])
    #         file.write(s + '\t')
    #     file.write('\n')
    #
    # file.write('\nвероятность отказа  (для 2-класса) от входящего потока')
    # file.write('\nlambda2/lambda1:\n')
    # for i, lam1 in enumerate(lambdas):
    #     for j, lam2 in enumerate(lambdas):
    #         s = "%8.4f" % (pf2[i, j])
    #         file.write(s + '\t')
    #     file.write('\n')
    #
    # file.write('\nм.о. числа треб. в очереди 1-класса от входящего потока')
    # file.write('\nlambda2/lambda1:\n')
    # for i, lam1 in enumerate(lambdas):
    #     for j, lam2 in enumerate(lambdas):
    #         s = "%8.4f" % (q1[i, j])
    #         file.write(s + '\t')
    #     file.write('\n')
    #
    # file.write('\nм.о. числа треб. в очереди 2-класса от входящего потока')
    # file.write('\nlambda2/lambda1:\n')
    # for i, lam1 in enumerate(lambdas):
    #     for j, lam2 in enumerate(lambdas):
    #         s = "%8.4f" % (q2[i, j])
    #         file.write(s + '\t')
    #     file.write('\n')
    #
    # # считаем теперь м.о. числа требований в очередях от размерности очередей
    # print("Зависимость от длины очередей")
    # capacities = range(5, 21, 3)
    # for i, cap1 in enumerate(capacities):
    #     for j, cap2 in enumerate(capacities):
    #         qs = QueueingSystem(system["M"], system["a"], system["b"],
    #                             cap1, cap2,
    #                             system["lam1"], system["lam2"],
    #                             system["mu"])
    #         qs.calculate()
    #         print(f"measures for {qs} \n{qs.data}")
    #         q1[i, j] = qs.data.demands_count1
    #         q2[i, j] = qs.data.demands_count2
    #
    # file.write('\nм.о. числа треб. в очереди 1-класса от расмерности очередей')
    # file.write('\ncap2/cap1:\n')
    # for i, cap1 in enumerate(lambdas):
    #     for j, cap2 in enumerate(lambdas):
    #         s = "%8.4f" % (q1[i, j])
    #         file.write(s + '\t')
    #     file.write('\n')
    #
    # file.write('\nм.о. числа треб. в очереди 2-класса от расмерности очередей')
    # file.write('\ncap2/cap1:\n')
    # for i, cap1 in enumerate(lambdas):
    #     for j, cap2 in enumerate(lambdas):
    #         s = "%8.4f" % (q2[i, j])
    #         file.write(s + '\t')
    #     file.write('\n')
    #
    # file.close()
    # print("executed")
