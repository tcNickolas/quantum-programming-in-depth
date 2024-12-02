import Std.Diagnostics.DumpMachine;
import Std.Math.ArcCos;

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


@EntryPoint()
operation DemoSingleBitFunctions() : Unit {
  for (quantumOp, f) in [
    (QuantumZero, "f(x) = 0"),
    (QuantumOne, "f(x) = 1"),
    (QuantumX, "f(x) = x"),
    (QuantumOneMinusX, "f(x) = 1 - x")
  ] {
    Message($"The effects of applying the quantum {f} to the state (0.6|0⟩ + 0.8|1⟩) ⨂ |0⟩:");
    use (x, y) = (Qubit(), Qubit());
    Ry(2.0 * ArcCos(0.6), x);
    quantumOp(x, y);
    DumpMachine();
    ResetAll([x, y]);
  }
}
