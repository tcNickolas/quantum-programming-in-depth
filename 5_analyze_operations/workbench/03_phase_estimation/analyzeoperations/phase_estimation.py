from cmath import pi, acos, sqrt
from psiqworkbench import QPU, Qubits
from workbench_algorithms import ArbitraryStatePrep

def one_bit_phase_estimation(n, eigenvector, unitary):
    '''Phase estimation with the guarantee that the eigenphase has only one binary digit'''
    qpu = QPU(num_qubits=n + 1)
    phase = Qubits(1, "phase", qpu)
    eigenstate = Qubits(n, "eigenstate", qpu)

    phase.had()

    state_prep = ArbitraryStatePrep(eigenvector)
    state_prep.compute(eigenstate)

    unitary(eigenstate, cond=phase)

    phase.had()
    res = phase.read()

    return res * 0.5


def iterative_phase_estimation(n, eigenvector, unitary):
    '''Iterative phase estimation: fixed circuit, a lot of repetitions'''
    qpu = QPU(num_qubits=n + 1)
    phase = Qubits(1, "phase", qpu)
    eigenstate = Qubits(n, "eigenstate", qpu)

    state_prep = ArbitraryStatePrep(eigenvector)
    state_prep.compute(eigenstate)

    n_trials = 10000
    n_zeros = 0
    for _ in range(n_trials):
        phase.had()

        unitary(eigenstate, cond=phase)

        phase.had()
        res = phase.read()
        n_zeros += 1 if res == 0 else 0

        if res != 0:
            phase.x()

    return acos(sqrt(n_zeros / n_trials)) / pi


def two_bit_adaptive_phase_estimation(n, eigenvector, unitary):
    '''Adaptive phase estimation: learn least significant bit, use it to learn most significant bit.
    Eigenphase is guaranteed to have at most two binary digits.
    '''
    qpu = QPU(num_qubits=n + 1)
    phase = Qubits(1, "phase", qpu)
    eigenstate = Qubits(n, "eigenstate", qpu)

    state_prep = ArbitraryStatePrep(eigenvector)
    state_prep.compute(eigenstate)

    res_bits = [0, 0]

    # Estimate the least significant bit
    phase.had()
    unitary(eigenstate, cond=phase)
    unitary(eigenstate, cond=phase)
    phase.had()
    res_bits[1] = 1 if phase.read() > 0 else 0
    if res_bits[1] > 0:
        phase.x()

    # Estimate the most significant bit
    phase.had()
    unitary(eigenstate, cond=phase)
    if res_bits[1] > 0:
        phase.s_inv()
    phase.had()
    res_bits[0] = 1 if phase.read() > 0 else 0

    return (res_bits[0] * 2 + res_bits[1]) / 4


def two_bit_quantum_phase_estimation(n, eigenvector, unitary):
    '''Quantum phase estimation (QFT-based).
    Eigenphase is guaranteed to have at most two binary digits.
    '''
    qpu = QPU(num_qubits=n + 2)
    phase = Qubits(2, "phase", qpu)
    eigenstate = Qubits(n, "eigenstate", qpu)

    phase.had()
    state_prep = ArbitraryStatePrep(eigenvector)
    state_prep.compute(eigenstate)

    unitary(eigenstate, cond=phase[1])
    unitary(eigenstate, cond=phase[1])
    unitary(eigenstate, cond=phase[0])

    phase.invQFT()

    return phase.read() / 4
