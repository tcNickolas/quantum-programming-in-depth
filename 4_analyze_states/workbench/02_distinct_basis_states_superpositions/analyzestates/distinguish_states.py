from psiqworkbench import Qubits

def distinguish_states(reg: Qubits) -> int:
    res = reg.read()
    return res if res < 4 else 7 - res