from psiqworkbench import QPU, Qubits
from .distinguish_states import distinguish_bell_states

def prep_test_state(reg: Qubits, ind: int) -> None:
    amps = [[1, 0, 0, 1],
            [1, 0, 0, -1],
            [0, 1, 1, 0],
            [0, 1, -1, 0],
            ]
    reg.push_state(amps[ind])


def test_distinguish_states():
    qpu = QPU()
    for ind in range(4):
        for _ in range(100):
            qpu.reset(2)
            reg = Qubits(2, "reg", qpu)
            prep_test_state(reg, ind)
            res = distinguish_bell_states(reg)
            assert res == ind
