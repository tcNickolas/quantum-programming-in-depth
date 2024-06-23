from qiskit import QuantumCircuit
from qiskit.circuit.library.standard_gates import XGate

def oracle_multiand(n):
  circ = QuantumCircuit(n + 1)
  circ.append(XGate().control(n), range(n + 1))
  return circ


def oracle_multior(n):
  circ = QuantumCircuit(n + 1)
  circ.append(XGate().control(n, ctrl_state=0), range(n + 1))
  circ.x(n)
  return circ


def evaluate_clause(n, literals):
  circ = QuantumCircuit(n + 1)
  if len(literals) == 0:
    return circ
  
  controls = []
  for (ind, neg) in literals:
    controls.append(ind)
    if not neg:
      circ.x(ind)
  
  circ.append(oracle_multior(len(controls)), controls + [n])
  
  for (ind, neg) in literals:
    if not neg:
      circ.x(ind)
  
  return circ


def evaluate_formula(n, formula):
  n_clauses = len(formula)
  circ = QuantumCircuit(n + n_clauses + 1)
  if n_clauses == 0:
    circ.x(n)
    return circ
  
  for (ind, clause) in enumerate(formula):
    circ.append(evaluate_clause(n, clause), list(range(n)) + [n + ind])

  circ.append(oracle_multiand(n_clauses), range(n, n + n_clauses + 1))

  for (ind, clause) in enumerate(formula):
    circ.append(evaluate_clause(n, clause), list(range(n)) + [n + ind])

  return circ
