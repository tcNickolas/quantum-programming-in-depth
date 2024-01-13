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
        return np.array(self.u)
    
    def _circuit_diagram_info_(self, args):
        return f"apply one qubit({self.u})" 
