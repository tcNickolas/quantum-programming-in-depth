# Brute force solution for the N queens puzzle that generates all solutions for the given N.
def queens(n: int, i: int, a: list, b: list, c: list):
    if i < n:
        for j in range(n):
            if j not in a and i + j not in b and i - j not in c:
                yield from queens(n, i + 1, a + [j], b + [i + j], c + [i - j])
    else:
        yield a


for solution in queens(10, 0, [], [], []):
    print(solution)