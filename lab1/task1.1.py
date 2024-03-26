import numpy as np
from matplotlib import pyplot as plt



def f(x):
    return 3 * x ** 3 + 1.7 * x ** 2 - 15.42 * x + 6.89



def d_f(x):  # derivative
    return 9 * x ** 2 + 3.4 * x - 15.42



def phi(x):
    return 3 / (-55.38) * x ** 3 + 1.7 / (-55.38) * x ** 2 + (- 15.42 / (-55.38) + 1) * x + 6.89 / (-55.38)


def chord_method(a, b, f, epsilon):
    dist = epsilon * 3
    i = 0
    while dist >= epsilon:
        i += 1
        x = a - (b - a) / (f(b) - f(a)) * f(a)
        print(
            round(i, 4),
            round(a, 4),
            round(b, 4),
            round(x, 4),
            round(f(a), 4),
            round(f(b), 4),
            round(f(x), 4),
            round(abs(a - b), 4),
        sep='\t')
        if x * a >= 0:
            dist = abs(a - x)
            a = x
        else:
            dist = abs(b - x)
            b = x


def graph(f):
    x = np.linspace(-4, 4, 1000)
    plt.axis([-4, 4, -4, 4])
    plt.title('My first plot')
    plt.plot(x, [f(i) for i in x])
    plt.show()


def simple_iterarion(x_0, epsilon, f, phi):
    i = 0
    x_i1 = x_0
    dist = epsilon * 3
    while dist >= epsilon:
        i += 1
        print(round(i, 3), end='\t')
        print(round(x_i1, 3), end='\t')
        x_i2 = phi(x_i1)
        print(round(x_i2, 3), end='\t')
        # print(round(phi(x_i2), 3), end='\t')
        print(round(f(x_i2), 3), end='\t')
        print(round(f(x_i2), 3), end='\t')
        dist = abs(x_i1 - x_i2)
        print(round(f(x_i2), 3))
        x_i1 = x_i2


def nuton_iterarion(x_0, epsilon, f, phi):
    i = 0
    x_i1 = x_0
    dist = epsilon * 3
    while dist >= epsilon:
        i += 1
        print(round(i, 3), end='\t')
        print(round(x_i1, 3), end='\t')
        print(round(f(x_i1), 3), end='\t')
        print(round(d_f(x_i1), 3), end='\t')
        x_i2 = phi(x_i1)
        print(round(x_i2, 3), end='\t')
        dist = abs(x_i1 - x_i2)
        print(round(f(x_i2), 5))
        x_i1 = x_i2


if __name__ == '__main__':
    # iterarion_methods(-2.5, 0.01, f, phi)
    # nuton_iterarion(0, 0.0001, f, lambda x: x - f(x) / d_f(x))
    chord_method(1.5, 2, f, 0.01)
    # graph(d_f)
