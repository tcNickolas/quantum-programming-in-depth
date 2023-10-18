from numpy import allclose
from scipy.linalg import cossin

u = [[0, 0, 0.6, 0.8],
     [0, 0, -0.8, 0.6],
     [0, 1, 0, 0],
     [1, 0, 0, 0]]

left, cs, right = cossin(u, p=len(u) // 2, q=len(u) // 2)

print(allclose(u, left @ cs @ right))

print(left)
print(cs)
print(right)
