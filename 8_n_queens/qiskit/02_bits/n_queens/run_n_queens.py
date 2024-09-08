from qiskit import transpile
from n_queens import *
from time import time
from qiskit_aer import Aer


# Run Grover's search end-to-end and print the frequency of correct results
n_rows = 4
n_bits = n_rows ** 2

# Search space size = for each row, can have one of n_rows basis states -> n_rows ^ n_rows
# (does not depend on the encoding we use)
search_space_size = n_rows ** n_rows # 256

print(f"Running for board size {n_rows}, mode = Bits")

for n_iter in range(4, 10):
  n_runs = 100
  circ = grovers_search(n_rows, n_iter)
  simulator = Aer.get_backend('aer_simulator')
  circ = transpile(circ, backend=simulator)
  start_time = time()
  res_map = simulator.run(circ, shots=n_runs).result().get_counts()
  end_time = time()

  n_correct = 0
  for (bitstring, num) in res_map.items():
    # For the bits encoding, ignore that Qiskit measurement results are in reversed order compared to qubit order
    # We'll just get a mirrored result
    if check_placement_bits(n_rows, bitstring):
      n_correct += num
    
  print(f"{n_iter} iterations - success rate {n_correct / n_runs * 100}% ({round(end_time - start_time)} sec)")