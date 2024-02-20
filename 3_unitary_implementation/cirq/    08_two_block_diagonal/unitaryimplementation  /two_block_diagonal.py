import numpy as np
from math import isclose
import cirq

class ArbitraryUnitary(cirq.Gate):
    def __init__(self, n, u):
        super(ArbitraryUnitary, self)
        self.n = n
        self.u = u
        
    def _num_qubits_(self):
        return n
    
    def _decompose_(self, qubits):
        if n == 1:
            yield OneQubitUnitary(self.u)
        
        if n == 2:
            if all(isclose(v, 0) for v in (u[0][2:] + u[1][2:] + u[2][:2] + u[3][:2]):
                   a = np.array([self.u[0][:2], self.u[1][:2]])
                   b = np.array([self.u[2][2:], self.u[3][2:]])
                   yield BlockDiagonalMatrix_2(a, b)
            raise NotImplementedError("The case of " + "arbitrary 2-qubit unitaries is not implemented yet")
        
        raise NotImplementedError("The case of 3+-qubit unitaries is not implemented yet")
                   
    def _circuit_diagram_info_(self, args):
        return f"special case of arbitrary matrix with({self.n}) qubits"
