from random import randint, random
import pytest
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
    
@pytest.mark.parametrize("u",
    [ [[1.0, 0.0], [0.0, 1.0]],
      [[1.0, 0.0], [0.0, -1.0]],
      [[-1.0, 0.0], [0.0, 1.0]],
      [[-1.0, 0.0], [0.0, -1.0]],
      [[0.0, 1.0], [1.0, 0.0]],
      [[0.0, 1.0], [-1.0, 0.0]],
      [[0.0, -1.0], [1.0, 0.0]],
      [[0.0, -1.0], [-1.0, 0.0]] ])

def test_apply_one_qubit(u):
    assert len(u) == 2
    for row in u:
        assert len(row) == 2

    gate = OneQubitUnitary(u)
    matrix = cirq.unitary(gate)

    for actual, expected in zip(matrix, u):
        assert actual == pytest.approx(expected)
        
def random_one_qubit_unitary():
    theta = random() * 2 * pi
    sign = +1 if randint(0, 1) == 1 else -1
    return [[np.cos(theta), sign * np.sin(theta)], 
         [-np.sin(theta), sign * np.cos(theta)]]

def test_dense():
    for _ in range(1, 20):
        test_apply_one_qubit(random_one_qubit_unitary())
