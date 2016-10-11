import time
import sys

sys.setrecursionlimit(2**16)

def timeit(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        print(time.time() - start)
        return res
    return wrapper

def memoize(func):
    dic = {}
    def wrapper(*args):
        if not args in dic:
            dic[args] = func(*args)
        return dic[args]
    return wrapper

@memoize
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)

@timeit
def count(n):
    return fib(n)


def mystaticmethod(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            return func(*(args[1:]), *kwargs)
    return wrapper

class C:
    @mystaticmethod
    def sum(arg1, arg2):
        return arg1 + arg2
