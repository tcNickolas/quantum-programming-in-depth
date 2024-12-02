operation QuantumZero(x : Qubit, y : Qubit) : Unit {
  // Do nothing.
}

operation QuantumOne(x : Qubit, y : Qubit) : Unit {
  X(y);
}

operation QuantumX(x : Qubit, y : Qubit) : Unit {
  CNOT(x, y);
}

operation QuantumOneMinusX(x : Qubit, y : Qubit) : Unit {
  ApplyControlledOnInt(0, X, [x], y);
}
