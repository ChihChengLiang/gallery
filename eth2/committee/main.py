from gallery import config
import matplotlib.pyplot as plt


SHARD_COUNT = 1024
SLOTS_PER_EPOCH = 64
TARGET_COMMITTEE_SIZE = 128


def get_committee_count(num_validator):
    a = SHARD_COUNT // SLOTS_PER_EPOCH
    b = num_validator // SLOTS_PER_EPOCH // TARGET_COMMITTEE_SIZE
    committees_per_slot = max(1, min(a, b))
    return committees_per_slot * SLOTS_PER_EPOCH


MIN_VALIDATOR = SLOTS_PER_EPOCH * TARGET_COMMITTEE_SIZE

num_validators = list(range(200000))
committee_count = list(map(get_committee_count, num_validators))
committee_size = [v//c for v, c in zip(num_validators, committee_count)]


ax = plt.subplot(211)
ax.plot(num_validators,  committee_count)
ax.vlines(MIN_VALIDATOR, ymin=0, ymax=1024, linestyles='dotted')
ax.text(MIN_VALIDATOR, 800, '  Minimum validator required\n  8192')
plt.ylabel('Committees')
ax = plt.subplot(212)
ax.plot(num_validators,  committee_size)
ax.hlines(TARGET_COMMITTEE_SIZE, xmin=1, xmax=len(
    num_validators), linestyles='dotted')
ax.text(len(num_validators)*0.8, TARGET_COMMITTEE_SIZE +
        5, 'Target Committee Size: 128')
ax.vlines(MIN_VALIDATOR, ymin=0, ymax=256, linestyles='dotted')
ax.text(MIN_VALIDATOR, 0, '  Minimum validator required\n  8192')
plt.ylabel('Validators per Committee')
plt.xlabel('Number of Total Validators')

plt.savefig('committee_count.png')
