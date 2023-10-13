import numpy as np
from scipy.linalg import cossin
from scipy.stats import unitary_group

# x = unitary_group.rvs(8)
x = [[0, 0, 0.6, 0.8],
     [0, 0, -0.8, 0.6],
     [0, 1, 0, 0],
     [1, 0, 0, 0]]

u, cs, v = cossin(x, p=len(x) / 2, q=len(x) / 2) 

print(np.allclose(x, u @ cs @ v))

# print([[d.round(5) for d in row] for row in cs])

print(u)
print(cs)
print(v)
