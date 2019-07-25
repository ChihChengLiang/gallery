from dataclasses import dataclass
from hashlib import sha256
from typing import NewType, Sequence, Union
import random
import matplotlib.pyplot as plt
from gallery import config

Hash32 = NewType('Hash32', bytes)
Gwei = NewType('Gwei', int)
ValidatorIndex = NewType('ValidatorIndex', int)
Epoch = NewType('Epoch', int)

MAX_RANDOM_BYTE = 2**8 - 1
MAX_EFFECTIVE_BALANCE = Gwei(2**5 * 10**9)

random.seed(5566)


@dataclass
class Validator:
    effective_balance: Gwei


def hash_eth2(data: Union[bytes, bytearray]) -> Hash32:
    return Hash32(sha256(data).digest())


def find_proposer_in_committee(validators: Sequence[Validator],
                               committee: Sequence[ValidatorIndex],
                               epoch: Epoch,
                               seed: Hash32) -> ValidatorIndex:
    base = int(epoch)
    i = 0
    committee_len = len(committee)
    while True:
        candidate_index = committee[(base + i) % committee_len]
        random_byte = hash_eth2(seed + (i // 32).to_bytes(8, "little"))[i % 32]
        effective_balance = validators[candidate_index].effective_balance
        if effective_balance * MAX_RANDOM_BYTE >= MAX_EFFECTIVE_BALANCE * random_byte:
            # print(effective_balance, MAX_RANDOM_BYTE,
            #       MAX_EFFECTIVE_BALANCE, random_byte)
            return candidate_index, i
        i += 1


validators = tuple(
    Validator(effective_balance=17 * 10**9)
    for i in range(128)
)
committee = range(len(validators))

observations = []
for _ in range(100000):
    candidate_index, i = find_proposer_in_committee(
        validators=validators,
        committee=committee,
        epoch=5,
        seed=random.getrandbits(8 * 32).to_bytes(32, 'little'),
    )
    observations.append(i)

expected_rounds = sum(observations) / len(observations)
print("expected_rounds:", expected_rounds)

plt.figure(0)
plt.hist(observations, bins=100, histtype='stepfilled')
plt.xlabel('Number of Rounds')
plt.ylabel('Number of Times out of 100000 Observations')
plt.title('Number of Times the Algorithm Reaches i Rounds')
plt.savefig('hist_0.png')

fig = plt.figure(1)
plt.hist(observations, bins=100, cumulative=True, density=True)
plt.xlabel('Number of Rounds')
plt.ylabel('Cumulative Probability')
plt.title('Probability that the Algorithm Ends in i Rounds')
plt.savefig('hist_1.png')


plt.figure(2)
plt.hist(observations, bins=100, log=True, density=True, cumulative=-1)
plt.xlabel('Number of Rounds')
plt.ylabel('Cumulative Probability in Log (and reversed)')
plt.title('Probability of the Algorithm Reaches i Rounds')
plt.savefig('hist_2.png')
