from qsharp import init, eval
from time import time

def check_placement_bits(n, bits):
  board = [bits[n * row:n * (row + 1)] for row in range(n)]
  # One queen per row
  for r in range(n):
    n_q = 0
    for c in range(n):
      if board[r][c]:
        n_q += 1
    if n_q != 1:
      return False
  indices = [row.index(True) for row in board]
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
n_bits = n_rows ** 2
check = check_placement_bits
oracle = f"NQueens.Oracle_Bits({n_rows}, _, _)"
prep_mean = f"NQueens.PrepareMean_Bits({n_rows}, _)"

# Search space size = for each row, can have one of n_rows basis states -> n_rows ^ n_rows
# (does not depend on the encoding we use)
search_space_size = n_rows ** n_rows # 256

print(f"Running for board size {n_rows}, mode = Bits")
init(project_root='.')
for n_iter in range(4, 10):
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