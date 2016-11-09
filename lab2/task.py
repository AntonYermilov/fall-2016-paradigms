import sys
from os import walk, path
from hashlib import sha1
from collections import defaultdict

def get_hash(file_path):
    with open(file_path, mode='rb') as f:
        hasher = sha1()
        while True:
            s = f.read(4096)
            if not s:
                break
            hasher.update(s)
        return hasher.digest()
        

def get_equal(top_dir):
    equal = defaultdict(list)
    for dir_path, _, files in walk(top_dir):
        for f in files:
            file_path = path.join(dir_path, f)
            if f[0] == '.' or f[0] == '~' or path.islink(file_path):
                continue
            file_hash = get_hash(file_path)
            equal[file_hash].append(path.join(path.relpath(dir_path, start=top_dir), f))
    for files in equal.values():
        if len(files) > 1:
            print(":".join(files))


def main():
    if len(sys.argv) != 2:
        print('usage: ./task.py dir_path')
        sys.exit(1)
    top_dir = sys.argv[1]
    get_equal(top_dir)

if __name__ == '__main__':
    main()
