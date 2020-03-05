import numpy as np
import matplotlib.pyplot as plt

t = np.linspace(0, 10, 10000)


def f1(t):
    return np.sin(0.9*2*np.pi*t)

def f2(t):
    return -np.sin(0.1*2*np.pi*t)

y1 = f1(t)
y2 = f2(t)

f_s = 1
T = 1/f_s

n = np.arange(0, 10*f_s, dtype=float)
s = f1(n * T)

fig, axs = plt.subplots(2)
axs[0].plot(t, y1)
axs[0].plot(n*T, s, "ro")
axs[0].grid()

axs[1].plot(t, y1)
axs[1].plot(t, y2)
axs[1].plot(n*T, s, "ro")
axs[1].grid()

#plt.show()
plt.savefig("aliasingFig.pdf")