import numpy as np
import cirq

class CsMatrix(cirq.Gate):
    def __init__(self, c0, s0, c1, s1):
        super(CsMatrix, self)
        self.c0 = c0
        self.s0 = s0
        self.c1 = c1
        self.s1 = s1
        
    def _num_qubits_(self):
        return 2
    
    def _unitary_(self):
        mat1 = np.array([[1, 0, 0, 0], [0, 1, 0, 0],
                       [0, 0, self.c0, -self.s0], [0, 0, self.s0, self.c0]])
        mat2 = np.array([[self.c1, -self.s1, 0, 0], [self.s1, self.c1, 0, 0],
                        [0, 0, 1, 0], [0, 0, 0, 1]])
        return np.matmul(mat1, mat2) 
