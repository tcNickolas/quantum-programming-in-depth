import numpy as np
from math import isclose
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


class CsMatrix_2(cirq.Gate):
    def __init__(self, c0, s0, c1, s1):
        super(CsMatrix_2, self)
        self.c0 = c0
        self.s0 = s0
        self.c1 = c1
        self.s1 = s1
        self.gate_m0 = OneQubitUnitary([[c0, -s0], [s0, c0]])
        self.gate_m1 = OneQubitUnitary([[c1, -s1], [s1, c1]])
    
    def _num_qubits_(self):
        return 2
    
    def _decompose_(self, qubits):
        control_1 = self.gate_m1.controlled().on(qubits[1], qubits[0])
        control_2 = self.gate_m0.controlled(control_values=[0]).on(qubits[1], qubits[0])
        
        yield control_2
        yield control_1 
        
    def _circuit_diagram_info_(self, args):
        return f"cs matrix with({self.c0, self.s0, self.c1, self.s1})"
