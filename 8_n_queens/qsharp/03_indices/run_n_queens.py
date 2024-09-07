from itertools import permutations
from math import pi, sqrt
from qsharp import init, eval
from time import time


def check_placement_indices(n, bits):
  bitsize = (n - 1).bit_length()
  indices = [int("".join(["1" if b else "0" for b in bits[bitsize * row:bitsize * (row + 1)]]), 2) for row in range(n)]
  for index in indices:
    if index < 0 or index >= n:
      return False
  return check_one_queen_per_column_diagonal(n, indices)


def check_one_queen_per_column_diagonal(n, indices):
  for r1 in range(n):
    for r2 in range(r1 + 1, n):
      diff = indices[r1] - indices[r2]
      if diff == 0 or abs(diff) == r2 - r1:
        # print(f"Queens ({r1}, {indices[r1]}) and ({r2}, {indices[r2]}) on column or diagonal")
        return False
  return True


# Run Grover's search end-to-end and print the frequency of correct results
n_rows = 4
optimize = True
index_size = (n_rows - 1).bit_length()
n_bits = n_rows * index_size
check = check_placement_indices
oracle = f"NQueens.Oracle_Indices({n_rows}, _, _)"
if not optimize:
  prep_mean = f"NQueens.PrepareMean_Indices({n_rows}, _)"
  search_space_size = n_rows ** n_rows # 256
else:
  # Precompute the amplitudes of the mean and pass them to Q#
  perms = list(permutations(range(n_rows)))
  non_zero_indices = [int("".join([str(ind) for ind in perm]), 2 ** index_size) for perm in perms]
  mean_amps = [0.] * (2 ** n_bits)
  for ind in non_zero_indices:
    mean_amps[ind] = 1.
  prep_mean = f"NQueens.PrepareMean_Indices_Opt({mean_amps}, _)"
  search_space_size = len(non_zero_indices)

n_sol = 2 if n_rows == 4 else 10
opt_iter = round(pi / 4 * sqrt(search_space_size / n_sol))
print(opt_iter)

print(f"Running for board size {n_rows}, mode = Indices, optimized = {optimize}")
init(project_root='.')
for n_iter in range(1, 5) if optimize else range(4, 10):
  n_runs = 100
  n_correct = 0
  start_time = time()
  for _ in range(n_runs):
    res_bits = eval("GroversSearch.RunGroversSearch(" +
      f"{n_bits}, {oracle}, {prep_mean}, {n_iter})")
    if check(n_rows, res_bits):
      n_correct += 1
  end_time = time()
  print(f"{n_iter} iterations - success rate {n_correct / n_runs * 100}% ({round(end_time - start_time)} sec)")