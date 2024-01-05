import numpy as np
from math importisclose
import cirq

class OneQubitUnitary(cirq.Gate):
    def __init__(self, u):
        super(OneQubitUnitary, self)
        self.u = u
        
    def _num_qubits_(self):
        return 1
    
    def _unitary_(self):
        if isclose(self.u[0][0], -self.u[1][1]) and isclose(self.u[1][0], self.u[0][1]):
            return np.matmul(np.array([[1, 0], [0, -1]]), self.u)       
        return np.array(self.u)
    
    def _circuit_diagram_info_(self, args):
        return f"apply one qubit({self.u})" 
