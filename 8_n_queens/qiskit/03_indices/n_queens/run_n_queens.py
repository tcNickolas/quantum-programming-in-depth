from time import time
from qiskit import transpile
from qiskit_aer import AerSimulator
from n_queens import *

# Run Grover's search end-to-end and print the frequency of correct results
n_rows = 4

print(f"Running for board size {n_rows}, mode = Indices")
simulator = AerSimulator(method='statevector')
n_runs = 100

for n_iter in range(4, 10):
  circ = grovers_search(n_rows, n_iter)
  circ = transpile(circ, backend=simulator)

  start_time = time()
  res_map = simulator.run(circ, shots=n_runs).result().get_counts()
  end_time = time()

  n_correct = 0
  for (bitstring, num) in res_map.items():
    if check_placement_indices(n_rows, bitstring):
      n_correct += num
    
  print(f"{n_iter} iterations - success rate {n_correct / n_runs * 100}%" + 
        f"({round(end_time - start_time)} sec)")
