from .state_parity import state_parity
from math import sqrt
from pytest import approx
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
from random import uniform

def complete_amps(n, parity_amps, parity):
  if n == 1:
    return parity_amps + [0] if parity == 0 else [0] + parity_amps
    
  zero_amps = parity_amps[ : 2 ** (n - 2)]
  one_amps = parity_amps[2 ** (n - 2) : ]    

  return complete_amps(n - 1, zero_amps, parity) + complete_amps(n - 1, one_amps, 1 - parity)

def test_state_parity():
  for n in range(2, 6):
    for parity in range(2):
      for _ in range(10):
        amps = [uniform(-1.0, 1.0) for _ in range(2 ** (n - 1))]

        # Normalize the amplitudes.
        norm = sqrt(sum(a*a for a in amps))
        a_norm = [j / norm for j in amps]

        # Reconstruct the amplitudes of basis states with the given parity 
        # into the complete amplitudes vector.
        amps = complete_amps(n, a_norm, parity)

        circ = QuantumCircuit(n + 1, 1)
        circ.initialize(amps, range(n))
        circ.append(state_parity(n), range(n + 1), [0])
        circ.save_statevector()

        simulator = Aer.get_backend('aer_simulator')
        circ = transpile(circ, backend=simulator)
        res = simulator.run(circ, shots=100).result()
        # Check that the execution result is always the same
        assert len(res.get_counts()) == 1
        # Check that the measured state matches the state that was prepared
        res_parity = int(list(res.get_counts().keys())[0], 2)

        # Check that the parity is correct.
        assert parity == res_parity

        # Check that the resulting state is the same as the initial one
        # and has not been modified by the measurement.
        state_vector = res.get_statevector().data

        # Discard the data about the last (most significant) qubit, 
        # which was measured to get the parity value and matches it.
        state_vector = state_vector[0 : 2 ** n] if parity == 0 else state_vector[2 ** n : ]

        assert state_vector == approx(amps)
