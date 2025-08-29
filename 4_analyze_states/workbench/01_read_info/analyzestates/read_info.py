from psiqworkbench import Qubits

def read_info(reg: Qubits) -> int:
    return reg.read()