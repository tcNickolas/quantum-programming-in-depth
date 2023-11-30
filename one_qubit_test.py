from math import atan2, pi
from pytket import Circuit
from pytket.extensions.qiskit import AerStateBackend

alpha, beta = 0.6, 0.8
circ = Circuit(1)           #Define a circuit with one qubit
theta = atan2(beta, alpha)  #Define the paramter for the Ry gate

# In tket, Ry gate accepts the angle argument as a factor of pi
circ.Ry(2 * (theta/pi), 0)       #Implement the Ry gate on qubit 0
circ.get_statevector()      #save the statevector after the gate has been implemented

backend = AerStateBackend()
compiled_circ = backend.get_compiled_circuit(circ)

state_vector = backend.run_circuit(compiled_circ).get_state()
print(state_vector.round(1))