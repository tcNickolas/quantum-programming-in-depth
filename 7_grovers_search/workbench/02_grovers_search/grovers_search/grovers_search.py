from psiqworkbench import QPU, Qubits

def marking_oracle(x: Qubits, y: Qubits, marked_states: list[int]) -> None:
    for state in marked_states:
        # Reverse control bit string, since controls use little endian
        y.x(cond=x[::-1] == state)


def run_grovers_search(n_bits: int, marking_oracle: callable, n_iter: int) -> int:
    qpu = QPU(num_qubits=n_bits + 1)
    x = Qubits(n_bits, "x", qpu)
    aux = Qubits(1, "aux", qpu)
    aux.x()
    aux.had()

    x.had()   # Simplify state preparation for this implementation

    for _ in range(n_iter):
        marking_oracle(x, aux)

        # Reflection about the mean
        x.had()
        (~x).reflect()
        x.had()

    # Reverse endianness here to get big endian result
    return x[::-1].read()