import sys
import numpy as np

def multiply(a, b, n, m):
    if n == 1:
        return a[0, 0] * b[0, 0]

    A = a[:m, :m]
    B = a[:m, m:n]
    C = a[m:n, :m]
    D = a[m:n, m:n]
    E = b[:m, :m]
    F = b[:m, m:n]
    G = b[m:n, :m]
    H = b[m:n, m:n]
    
    k = m >> 1
    P1 = multiply(A, F - H, m, k)
    P2 = multiply(A + B, H, m, k)
    P3 = multiply(C + D, E, m, k)
    P4 = multiply(D, G - E, m, k)
    P5 = multiply(A + D, E + H, m, k)
    P6 = multiply(B - D, G + H, m, k)
    P7 = multiply(A - C, E + F, m, k)

    c = np.empty((n, n))
    c[:m, :m] = P5 + P4 - P2 + P6
    c[:m, m:n] = P1 + P2
    c[m:n, :m] = P3 + P4
    c[m:n, m:n] = P1 + P5 - P3 - P7
    return c

def main():
    data = np.loadtxt(sys.stdin, dtype = np.int, ndmin = 2, skiprows = 1)
    n, m = len(data[0]), 1
    while m < n:
        m *= 2
    
    a = np.zeros((m, m))
    a[:n, :n] = data[:n, :n]
    b = np.zeros((m, m))
    b[:n, :n] = data[n:, :n]

    c = multiply(a, b, m, m >> 1)
    
    #print(a[:n, :n].dot(b[:n, :n]))
    print("\n".join(" ".join(str(int(c[i][j])) for j in range(n)) for i in range(n)))
    
if __name__ == '__main__':
    main()
