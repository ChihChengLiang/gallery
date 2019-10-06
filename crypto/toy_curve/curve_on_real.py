import matplotlib.pyplot as plt
from py_ecc.fields.field_elements import FQ
import mpl_toolkits.axisartist as AA
import numpy as np

x = np.linspace(-25.0, 25.0, 100)
y = np.linspace(-25.0, 25.0, 100)
X, Y = np.meshgrid(x, y)
F = X**3 + 4 - Y**2

with plt.xkcd():
    fig = plt.figure(1, figsize=(4, 4), dpi=100)
    ax = AA.Subplot(fig, 111)
    fig.add_subplot(ax)
    ax.axis["right"].set_visible(False)
    ax.axis["top"].set_visible(False)
    for direction in ["left", "bottom"]:
        ax.axis[direction].set_axisline_style("-|>")

    ax.contour(X, Y, F, [0])
    ax.set_title(r'$Y^2 = X^3 + 4$ on Real Number')
plt.savefig('toy_curve_on_real.png')
