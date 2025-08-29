from psiqworkbench import Qubits

def distinguish_bell_states(reg: Qubits) -> int:
    reg[1].x(cond=reg[0])
    reg[0].had()
    return reg.read()
