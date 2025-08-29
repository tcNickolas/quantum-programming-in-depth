from psiqworkbench import Qubits

def quantum_zero(x: Qubits, y: Qubits):
    pass

def quantum_one(x: Qubits, y: Qubits):
    y.x()

def quantum_x(x: Qubits, y: Qubits):
    y.x(cond=x)

def quantum_one_minus_x(x: Qubits, y: Qubits):
    y.x(cond=~x)
