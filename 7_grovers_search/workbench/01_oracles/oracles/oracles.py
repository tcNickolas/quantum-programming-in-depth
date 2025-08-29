from psiqworkbench import Qubits

def marking_oracle(x: Qubits, y: Qubits, marked_states: list[int]) -> None:
    for state in marked_states:
        # Reverse control bit string, since controls use little endian
        y.x(cond=x[::-1] == state)


def phase_oracle(x: Qubits, marking_oracle: callable):
    aux = Qubits(1, "aux", x.qpu)
    aux.x()
    aux.had()
    marking_oracle(x, aux)
    aux.had()
    aux.x()
    aux.release()
