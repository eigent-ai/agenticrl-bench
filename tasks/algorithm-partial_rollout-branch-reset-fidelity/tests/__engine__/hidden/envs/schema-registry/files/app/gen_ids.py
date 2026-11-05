import random

with open('ids.txt', 'w') as f:
    f.write('\n'.join(str(random.randrange(10**6)) for _ in range(5)) + '\n')
