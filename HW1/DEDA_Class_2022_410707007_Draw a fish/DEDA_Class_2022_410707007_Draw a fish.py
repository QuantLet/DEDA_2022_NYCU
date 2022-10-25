
from matplotlib import animation
from numpy import append, cos, linspace, pi, sin, zeros
import matplotlib.pyplot as plt
from IPython.display import HTML

# PLEASE NOTE IN SPYDER YOU SHOULD DISABLE THE ACTIVE SUPPORT in PREFs
# elephant parameters
parameters = [50 - 10j, 20 + 3j, 20 - 10j, 10 - 60j, -40 - 10j]

def fourier(t, C):
    f = zeros(t.shape)
    for k in range(len(C)):
        f += C.real[k] * cos(k * t) + C.imag[k] * sin(k * t)
    return f


def fish(t, p):
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
    x, y = fish(linspace(2.9 * pi, 0.4 + 3.3 * pi, 1000), parameters)
    for ii in range(len(y) - 1):
        y[ii] -= sin(((x[ii] - x[0]) * pi / len(y))) * sin(float(0)) * parameters[4].real
    trunk.set_data(x, y)
    return trunk,


def move_trunk(i):
    x, y = fish(linspace(2.9 * pi, 0.4 + 3.3 * pi, 1000), parameters)
    # move trunk to new position (but don't move eye stored at end or array)
    for ii in range(len(y) - 1):
        y[ii] -= sin(((x[ii] - x[0]) * pi / len(y))) * sin(float(i)) * parameters[4].real
    trunk.set_data(x, y)
    return trunk,


fig, ax = plt.subplots()
# initial the elephant body
x, y = fish(t=linspace(0.4 + 1.3 * pi, 2.9 * pi, 1000), p=parameters)
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


plt.savefig('DEDA_Class_2022_410707007_Draw a fish.png')
# Video will be externally saved
Writer = animation.writers['ffmpeg']
metadata = dict(title='Wentians pea shooter')
writer = Writer(fps=30, metadata=metadata, bitrate=1800)
ani.save(filename='DEDA_Class_2022_410707007_Draw a fish.mp4', writer=writer)
plt.show()


