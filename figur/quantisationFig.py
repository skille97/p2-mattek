import numpy as np
import matplotlib.pyplot as plt

N1 = 3

t = np.linspace(0, 20, 1000)
a1 = np.linspace(-2., 2., 2 ** N1)
def f1(t):
    return np.sin(np.pi*t) + np.sin(0.1*np.pi*t)

y1 = f1(t)

k1 = np.empty(len(y1))
for i in range(len(y1)):
    k1[i] = a1[a1 > y1[i]][0]

y2 = f1(t)
N2 = 5
a2 = np.linspace(-2., 2., 2 ** N2)
k2 = np.empty(len(y2))
for i in range(len(y2)):
    k2[i] = a2[a2 > y2[i]][0]

fig, axs = plt.subplots(2)
axs[0].plot(t, y1)
axs[0].plot(t, k1, drawstyle='steps-mid')
axs[0].grid()

axs[1].plot(t, y2)
axs[1].step(t, k2)
axs[1].grid()

plt.show()
#plt.savefig("quantisationFig.pdf")
