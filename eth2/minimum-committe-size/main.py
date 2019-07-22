from gallery import config
import matplotlib.pyplot as plt
from math import ceil


#
# Source: https://vitalik.ca/files/Ithaca201807_Sharding.pdf page 11
#

def fac(n):
    return n * fac(n-1) if n else 1

# If 'choose' is not efficient enough, use 'comb' from scipy
# from scipy.special import comb
# choose = comb


def choose(n, k):
    return fac(n) // fac(k) // fac(n-k)


def prob(n, k, p):
    return p**k * (1-p)**(n-k) * choose(n, k)


def probgte(n, k, p):
    return sum([prob(n, i, p) for i in range(k, n+1)])


x = []
y = []
label_1 = None
label_2 = None
for i in range(100, 300):
    two_third = ceil(i * 2/3)
    p = probgte(i, two_third, 1/3)
    x.append(i)
    y.append(p)
    if p < 2**-40 and label_1 is None:
        label_1 = (i, p)
    if p < 2**-80 and label_2 is None:
        label_2 = (i, p)

plt.yscale('log')
plt.plot(x, y)
plt.plot(*label_1, 'o')
plt.text(*label_1, r'   prob: $2^{-40}$ at size %s' % label_1[0])

plt.plot(*label_2, 'o')
plt.text(*label_2, r'   prob: $2^{-80}$ at size %s' % label_2[0])

plt.ylabel('Prob. Malicious Validators Gain a Majortiy (Log)')
plt.xlabel('Committee size')

plt.savefig('committee_size.png')
