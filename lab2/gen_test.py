import random

with open('test', 'w') as f:
    for i in range(10000000):
        f.write(str(random.randint(0, 9)))
