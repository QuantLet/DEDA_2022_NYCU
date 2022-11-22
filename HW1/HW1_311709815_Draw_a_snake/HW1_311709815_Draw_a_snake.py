#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 11:54:10 2022

@author: youcefnazimtahari
"""

# import matplotlib
# matplotlib.use('TKAgg')
from matplotlib import animation
from numpy import append, cos, linspace, pi, sin, zeros
import matplotlib.pyplot as plt
from IPython.display import HTML

# PLEASE NOTE IN SPYDER YOU SHOULD DISABLE THE ACTIVE SUPPORT in PREFs
# elephant parameters
parameters = [50 - 15j, 5 + 2j, -20 - 5j, -7 - 10j, 18 + 40j]


# patrick's happy spermwhale
# parameters = [30 - 10j, 20 + 20j, 40 + 10j, 20 - 50j, -40 + 10j]

# philipp's flying swan 
# parameters = [1 - 2j, 9 + 9j, 1 - 2j, 9 + 9j, 0 + 0j]

# kathrin's hungry animal 
# parameters = [50 - 50j, 30 + 10j, 5 - 2j, -5 - 6j, 20 + 20j]

# anna’s happy hippo
# parameters = [50 - 15j, 5 + 2j, -10 - 10j, -14 - 60j, 5 + 30j]

# fabio’s bird with right wing paralysis
# parameters = [50 - 15j, 5 + 2j, -1 - 5j, -14 - 60j, 18 - 40j]

# for pea shooter see code below 

def fourier(t, C):
    f = zeros(t.shape)
    for k in range(len(C)):
        f += C.real[k] * cos(k * t) + C.imag[k] * sin(k * t)
    return f


def elephant(t, p):
    npar = 6

    Cx = zeros((npar,), dtype='complex')
    Cy = zeros((npar,), dtype='complex')

    Cx[1] = p[0].real * 1j
    Cy[1] = p[3].imag + p[0].imag * 1j

    Cx[2] = p[1].real * 1j
    Cy[2] = p[1].imag * 1j

    Cx[3] = p[2].real
    Cy[3] = p[2].imag * 1j

    Cx[5] = p[3].real

    x = append(fourier(t, Cy), [p[4].real])
    y = -append(fourier(t, Cx), [-p[4].imag])

    return x, y


def init_plot():
    # draw the body of the elephant & create trunk
    x, y = elephant(linspace(2.9 * pi, 0.4 + 3.3 * pi, 1000), parameters)
    for ii in range(len(y) - 1):
        y[ii] -= sin(((x[ii] - x[0]) * pi / len(y))) * sin(float(0)) * parameters[4].real
    trunk.set_data(x, y)
    return trunk,


def move_trunk(i):
    x, y = elephant(linspace(2.9 * pi, 0.4 + 3.3 * pi, 1000), parameters)
    # move trunk to new position (but don't move eye stored at end or array)
    for ii in range(len(y) - 1):
        y[ii] -= sin(((x[ii] - x[0]) * pi / len(y))) * sin(float(i)) * parameters[4].real
    trunk.set_data(x, y)
    return trunk,


fig, ax = plt.subplots()
# initial the elephant body
x, y = elephant(t=linspace(0.4 + 1.3 * pi, 2.9 * pi, 1000), p=parameters)
plt.plot(x, y, 'b.')
plt.xlim([-75, 90])
plt.ylim([-70, 87])
plt.axis('off')
trunk, = ax.plot([], [], 'b.')  # initialize trunk

ani = animation.FuncAnimation(fig=fig,
                              func=move_trunk,
                              frames=1000,
                              init_func=init_plot,
                              interval=100,
                              blit=False,
                              repeat=True)

ani
HTML(ani.to_html5_video())
