from math import sqrt
from psiqworkbench import QPU, Qubits
from random import uniform
from .state_parity import state_parity

def complete_amps(n, parity_amps, parity):
    '''Helper function to unroll non-zero amplitudes of an (n-1)-qubit state
       into amplitudes of n-qubit state of the given parity
    '''
    if n == 1:
      return parity_amps + [0] if parity == 0 else [0] + parity_amps
    
    zero_amps = parity_amps[ : 2 ** (n - 2)]
    one_amps = parity_amps[2 ** (n - 2) : ]    

    return complete_amps(n - 1, zero_amps, parity) + complete_amps(n - 1, one_amps, 1 - parity)


def test_state_parity():
    qpu = QPU()
    for n in range(2, 6):
        for parity in range(2):
            amps = [uniform(-1.0, 1.0) for _ in range(2 ** (n - 1))]
            norm = sqrt(sum(a*a for a in amps))
            a_norm = [j / norm for j in amps]
            parity_amps = complete_amps(n, a_norm, parity)

            for _ in range(100):
                qpu.reset(n)
                reg = Qubits(n, "reg", qpu)
                reg.push_state(parity_amps)

                res = state_parity(reg)
                assert res == parity
