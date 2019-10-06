import matplotlib.pyplot as plt
from py_ecc.fields.field_elements import FQ
import mpl_toolkits.axisartist as AA


q = 97


class F97(FQ):
    field_modulus = q


def curve(x):
    for i in range(q):
        y = F97(i)
        if y**2 == x**3 + 4:
            return y, -y
    return None


def gen_points():
    for i in range(q):
        x = F97(i)
        ys = curve(x)
        if ys is not None:
            y_top, y_bottom = ys
            yield int(x), int(y_top), int(y_bottom)


points = list(gen_points())
print(points)
xs, y_tops, y_bottoms = list(zip(*points))

with plt.xkcd():
    fig = plt.figure(1, figsize=(4, 4), dpi=100)
    ax = AA.Subplot(fig, 111)
    fig.add_subplot(ax)
    ticks = [16*i for i in range(7)]
    ax.set_xticks(ticks)
    ax.set_yticks(ticks)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)

    ax.axis["right"].set_visible(False)
    ax.axis["top"].set_visible(False)
    for direction in ["left", "bottom"]:
        ax.axis[direction].set_axisline_style("-|>")

    ax.scatter(xs, y_tops, marker='.', c='black')
    ax.scatter(xs, y_bottoms, marker='.', c='black')
    ax.set_title(r'$Y^2 = X^3 + 4$ (mod 97)')
plt.savefig('toy_curve_on_prime_field.png')
