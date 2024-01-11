import numpy as np
from math import isclose
import cirq

class BlockDiagonalMatrix(cirq.Gate):
    def __init__(self, a, b):
        super(BlockDiagonalMatrix, self)
        self.a = a
        self.b = b

    def _num_qubits_(self):
        return 2

    def _unitary_(self):     
        if isclose(a[0][0], -a[1][1]) and isclose(a[1][0], a[0][1]):
            self.a = np.matmul(np.array([[1, 0], [0, -1]]), self.a)  
        if isclose(b[0][0], -b[1][1]) and isclose(b[1][0], b[0][1]):
            self.b = np.matmul(np.array([[1, 0], [0, -1]]), self.b) 
    
        return np.array([
            [self.a[0][0], self.a[0][1], 0, 0], [self.a[1][0], self.a[1][1], 0, 0], 
            [0, 0, self.b[0][0], self.b[0][1]], [0, 0, self.b[1][0], self.b[1][1]]])
    
    def _circuit_diagram_info_(self, args):
        return f"block diagonal matrix with({self.a, self.b})"
