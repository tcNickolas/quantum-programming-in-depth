from psiqworkbench import Qubits

def state_parity(reg: Qubits) -> int:
    return reg.ppm(1, 0, ~0)
