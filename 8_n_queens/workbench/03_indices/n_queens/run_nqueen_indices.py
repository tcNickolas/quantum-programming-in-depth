from time import time
from n_queens import *

n_rows = 4

n_iter = 8
print(f"Running for board size {n_rows}, mode = Indices")
n_runs = 10
n_correct = 0

start_time = time()

for _ in range(n_runs):
    board = grovers_search(n_rows, n_iter)

    if check_placement_indices(n_rows, board):
        n_correct += 1

end_time = time()

print(f"{n_iter} iterations - success rate {n_correct / n_runs * 100}%" + 
    f"({round(end_time - start_time)} sec)")
