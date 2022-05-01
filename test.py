import matplotlib.pyplot as plt
T = 22
n0 = 33
t = [T * i for i in range(10)]
n = [n0 * 2 ** (-i / T) for i in t]
plt.plot(n, t)
plt.ylabel('n')
plt.xlabel('t')
plt.savefig('plot.jpg')