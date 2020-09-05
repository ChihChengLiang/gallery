from gallery import config
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection
import matplotlib.ticker as ticker

import json

GWEI = 10**9
BLOCK_SIZE = 12500000


with open("./pending.json") as f:
    j = json.load(f)
    result = []
    for addr, obj in j.items():
        for nonce, tx in obj.items():
            result.append(
                {
                    "gas": int(tx["gas"], 0),
                    "gasPrice": int(tx["gasPrice"], 0)
                }
            )
result_sorted = sorted(result, key=lambda x: -x["gasPrice"])

gas_price_max = result_sorted[0]["gasPrice"]

rectangles = []
cummulated_gas = 0
current_price = gas_price_max
left = 0

for i, item in enumerate(result_sorted):
    gas, gas_price = item["gas"], item["gasPrice"]
    if gas_price < current_price:
        rect = Rectangle((left, 0), cummulated_gas - left, current_price)
        rectangles.append(rect)
        current_price = gas_price
        left = cummulated_gas
    cummulated_gas += gas

pc = PatchCollection(rectangles)
pc2 = PatchCollection(rectangles)

@ticker.FuncFormatter
def gwei_formatter(x, pos):
    return int(x // GWEI)

@ticker.FuncFormatter
def million_formatter(x, pos):
    return int(x // 10**6)

plt.figure(0, figsize=(8, 8), dpi=100)
ax = plt.subplot(111)
plt.xlabel('Gas (Million Gas)')
plt.ylabel('Gas Price (Gwei)')
plt.title('A Snapshot of 4096 Pending Txs, Sept 5, 2020')

ax.axvline(x=BLOCK_SIZE)
ax.annotate('block gas limit', xy=(BLOCK_SIZE, 300 * GWEI), xytext=(BLOCK_SIZE * 10,  300 * GWEI),
            arrowprops=dict(facecolor='black', shrink=0.05),
            )

ax.set_xlim(0, cummulated_gas)
ax.xaxis.set_major_formatter(million_formatter)
ax.set_ylim(0, gas_price_max)
ax.yaxis.set_major_formatter(gwei_formatter)
ax.add_collection(pc)

plt.savefig('demand_4096.png')

plt.figure(1, figsize=(8, 8), dpi=100)
ax = plt.subplot(111)
plt.xlabel('Gas (Million Gas)')
plt.ylabel('Gas Price (Gwei)')
plt.title('Some Pending Txs, Sept 5, 2020')

ax.axvline(x=BLOCK_SIZE)
ax.annotate('block gas limit', xy=(BLOCK_SIZE, 300 * GWEI), xytext=(BLOCK_SIZE * 0.6,  300 * GWEI),
            arrowprops=dict(facecolor='black', shrink=0.05),
            )

ax.set_xlim(0, BLOCK_SIZE*1.25)
ax.xaxis.set_major_formatter(million_formatter)
ax.set_ylim(0, gas_price_max)
ax.yaxis.set_major_formatter(gwei_formatter)
ax.add_collection(pc2)

plt.savefig('demand_block.png')
