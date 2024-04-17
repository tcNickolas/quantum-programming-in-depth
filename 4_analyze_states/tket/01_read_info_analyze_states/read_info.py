from pytket.circuit import Circuit

def read_info(n):
  circ = Circuit(n, n)
  circ.Measure(range(n), range(n))
  return circ
