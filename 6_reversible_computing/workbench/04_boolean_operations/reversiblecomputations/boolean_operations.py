from psiqworkbench import Qubits

def quantum_not(x: Qubits, y: Qubits):
    y.x(cond=x)
    y.x()

def quantum_xor(x: Qubits, y: Qubits):
    for ind in range(x.num_qubits):
        y.x(cond=x[ind])

def quantum_equal(x: Qubits, y: Qubits):
    for ind in range(x.num_qubits):
        y.x(cond=x[ind])
    y.x()

def quantum_and(x: Qubits, y: Qubits):
    y.x(cond=x)

def quantum_or(x: Qubits, y: Qubits):
    y.x(cond=~x)
    y.x()
