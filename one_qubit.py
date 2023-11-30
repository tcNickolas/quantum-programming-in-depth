from math import atan2, pi
from pytket import Circuit

alpha, beta = 0.6, 0.8
circ = Circuit(1)           #Define a circuit with one qubit
theta = atan2(beta, alpha)  #Define the paramter for the Ry gate
circ.Ry(2 * (theta/pi), 0)       #Implement the Ry gate on qubit 0
