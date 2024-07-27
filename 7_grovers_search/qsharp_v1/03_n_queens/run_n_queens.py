from qsharp import init, eval
from time import time

def check_placement(n, queens):
  # One queen per row
  for r in range(n):
    n_q = 0
    for c in range(n):
      if queens[r * n + c]:
        n_q += 1
    if n_q != 1:
    #   print(f"Row {r} has {n_q} queens")
      return False
  # One queen per column
  for c in range(n):
    n_q = 0
    for r in range(n):
      if queens[r * n + c]:
        n_q += 1
    if n_q != 1:
    #   print(f"Column {c} has {n_q} queens")
      return False
  # One queen per diagonal
  for r1 in range(n):
    for r2 in range(r1 + 1, n):
      for c1 in range(n):
        for c2 in [c1 + r2 - r1, c1 - r2 + r1]:
          if c2 >= 0 and c2 < n and queens[r1 * n + c1] and queens[r2 * n + c2]:
            # print(f"Queens ({r1}, {c1}) and ({r2}, {c2}) on diagonal")
            return False
  return True

init(project_root='.')
# Run Grover's search end-to-end and print the frequency of correct results
n_rows = 4
n_bits = n_rows ** 2
# Search space size = for each row, can have one of n_rows basis states -> n_rows 
search_space_size = n_rows ** n_rows # 256

# eval(f"NQueens.Test.AssertOracleIsValid(4)")
# eval(f"NQueens.Test.AssertOracleIsValid(5)")
# exit()

for n_iter in range(6, 10):
  n_runs = 1000
  n_correct = 0
  start_time = time()
  for _ in range(n_runs):
    res_bits = eval("GroversSearch.RunGroversSearch(" +
      f"{n_bits}, NQueens.NQueensOracle({n_rows}, _, _), NQueens.PrepareMean({n_rows}, _), {n_iter})")
    if check_placement(n_rows, res_bits):
      n_correct += 1
  end_time = time()
  print(f"{n_iter} iterations - success rate {n_correct / n_runs * 100}% ({round(end_time - start_time)} sec)")