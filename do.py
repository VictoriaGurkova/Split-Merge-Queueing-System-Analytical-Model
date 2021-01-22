import os

import numpy as np

from experiment.capacity_dependency import CapacityDependency
from experiment.intensity_dependency import IntensityDependency

k = 6
lambdas = list(np.linspace(0.5, 2, k))

intensity = IntensityDependency()
intensity.save_results()

capacity = CapacityDependency()
capacity.save_results()

print(os.getcwd())

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
# plt.plot(lambdas, pf[2], 'b')
# plt.plot(lambdas, [p[2] for p in pf], 'r')
# plt.title(f"Зависимость вероятности отказа")
# plt.xlabel("lambda")
# plt.ylabel("PF")
# plt.grid()
# plt.savefig('output/pf-lambda.png')
# plt.show()
