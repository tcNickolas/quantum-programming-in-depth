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
        return np.array(self.u)
    
    def _circuit_diagram_info_(self, args):
        return f"apply one qubit({self.u})" 


class BlockDiagonalMatrix_2(cirq.Gate):
    def __init__(self, a, b):
        super(BlockDiagonalMatrix_2, self)
        self.a = a
        self.b = b
        self.gate_a = OneQubitUnitary(a)
        self.gate_b = OneQubitUnitary(b)
        
    def _num_qubits_(self):
        return 2
    
    def _decompose_(self, qubits):
        control_1 = self.gate_b.controlled().on(qubits[0], qubits[1])
        control_2 = self.gate_a.controlled(control_values=[0]).on(qubits[0], qubits[1])
        
        yield control_2
        yield control_1
        
    def _circuit_diagram_info_(self, args):
        return f"block diagonal matrix with({self.a, self.b})"
