import numpy as np

def multiply(a, b, n):
    A = a[0 : n >> 1, 0 : n >> 1]
    B = a[0 : n >> 1, n >> 1 : n]
    C = a[n >> 1 : n, 0 : n >> 1]
    D = a[n >> 1 : n, n >> 1 : n]
    E = b[0 : n >> 1, 0 : n >> 1]
    F = b[0 : n >> 1, n >> 1 : n]
    G = b[n >> 1 : n, 0 : n >> 1]
    H = b[n >> 1 : n, n >> 1 : n]
    
    P1 = A.dot(F - H)
    P2 = (A + B).dot(H)
    P3 = (C + D).dot(E)
    P4 = D.dot(G - E)
    P5 = (A + D).dot(E + H)
    P6 = (B - D).dot(G + H)
    P7 = (A - C).dot(E + F)

    c = np.array([[0] * n] * n)
    c[0 : n >> 1, 0 : n >> 1] = P5 + P4 - P2 + P6
    c[0 : n >> 1, n >> 1 : n] = P1 + P2
    c[n >> 1 : n, 0 : n >> 1] = P3 + P4
    c[n >> 1 : n, n >> 1 : n] = P1 + P5 - P3 - P7
    return c

def main():
    with open('data.in', 'r') as f:
        n, m = int(f.readline()), 1
        while m < n:
            m *= 2

        a = np.array([list(map(int, f.readline().split())) + [0] * (m - n) for i in range(n)] + [[0] * m] * (m - n))
        b = np.array([list(map(int, f.readline().split())) + [0] * (m - n) for i in range(n)] + [[0] * m] * (m - n))
        c = multiply(a, b, m)
        #print(a)
        #print(b)
        #print(a[0 : n, 0 : n].dot(b[0 : n, 0 : n]))
        print("\n".join(" ".join(str(c[i][j]) for j in range(n)) for i in range(n)))

if __name__ == '__main__':
    main()
