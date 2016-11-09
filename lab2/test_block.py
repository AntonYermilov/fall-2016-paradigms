import sys
from time import time
from hashlib import sha1

def main():
    start = time()
    name = sys.argv[1]
    size = int(sys.argv[2])
    block = 1024 * (size + 1)
    hasher = sha1()
    with open(name, mode='rb') as f:
        while True:
            s = f.read(block)
            if not s:
                break
            hasher.update(s)
    print(block, time() - start)

if __name__ == '__main__':
    main()
