from functools import partial
from psiqworkbench import Qubits
from .distinguish_unitaries import *
import pytest

def apply_x_z(reg: Qubits, ind: int) -> None:
    '''The function that applies either X or Z gate to the given qubit(s) based on the index.'''
    if ind == 0:
        reg.x()
    else:
        reg.z()

def apply_x_h(reg: Qubits, ind: int) -> None:
    '''The function that applies either X or H gate to the given qubit(s) based on the index.'''
    if ind == 0:
        reg.x()
    else:
        reg.had()

def apply_x_minusx(reg: Qubits, ind, cond: Qubits=0):
    '''The function that applies either X or -X gate to the given qubit(s) based on the index.'''
    if ind == 0:
        reg.x(cond=cond)
    else:
        reg.z(cond=cond)
        reg.x(cond=cond)
        reg.z(cond=cond)


@pytest.mark.parametrize("apply_unitaries,distinguisher",
                         [(apply_x_z, distinguish_x_z),
                          (apply_x_h, distinguish_x_h),
                          (apply_x_minusx, distinguish_x_minusx)
                         ])
def test_distinguish_unitaries(apply_unitaries, distinguisher):
    for unitary_ind in range(2):
        for _ in range(100):
            unitary = partial(apply_unitaries, ind=unitary_ind)
            result_ind = distinguisher(unitary)

            assert result_ind == unitary_ind