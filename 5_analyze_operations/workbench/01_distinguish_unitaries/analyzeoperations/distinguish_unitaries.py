from psiqworkbench import QPU, Qubits

def distinguish_x_z(unitary: callable) -> int:
    '''The function that sets up and runs the experiment to distinguish X and Z gates.'''
    qpu = QPU(num_qubits=1)
    reg = Qubits(1, "reg", qpu)
    unitary(reg)
    reg.x()
    return reg.read()


def distinguish_x_h(unitary: callable) -> int:
    '''The function that sets up and runs the experiment to distinguish X and H gates.'''
    qpu = QPU(num_qubits=1)
    reg = Qubits(1, "reg", qpu)
    unitary(reg)
    reg.x()
    unitary(reg)
    reg.x()
    return reg.read()


def distinguish_x_minusx(unitary: callable) -> int:
    '''The function that sets up and runs the experiment to distinguish X and -X gates.'''
    qpu = QPU(num_qubits=2)
    reg = Qubits(2, "reg", qpu)
    reg.had()
    unitary(reg[1], cond=reg[0])
    reg.had()
    return reg.read()
