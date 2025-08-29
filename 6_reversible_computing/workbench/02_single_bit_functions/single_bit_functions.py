from math import acos
from psiqworkbench import QPU, Qubits, Units

def quantum_zero(x: Qubits, y: Qubits):
    pass

def quantum_one(x: Qubits, y: Qubits):
    y.x()

def quantum_x(x: Qubits, y: Qubits):
    y.x(cond=x)

def quantum_one_minus_x(x: Qubits, y: Qubits):
    y.x(cond=~x)


qpu = QPU()
for (quantum_op, f) in [
    (quantum_zero, "f(x) = 0"), 
    (quantum_one, "f(x) = 1"), 
    (quantum_x, "f(x) = x"),
    (quantum_one_minus_x, "f(x) = 1 - x") ]:
    qpu.reset(2)
    x = Qubits(1, "x", qpu)
    y = Qubits(1, "y", qpu)
    x.ry(2 * acos(0.6) * Units.rad)
    quantum_op(x, y)
    print(f"The effects of applying the quantum operation {f} to the state (0.6|0⟩ + 0.8|1⟩) ⨂ |0⟩:")
    qpu.print_state_vector()
