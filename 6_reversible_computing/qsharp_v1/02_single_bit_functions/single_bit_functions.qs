namespace ReversibleComputing {
  open Microsoft.Quantum.Diagnostics;
  open Microsoft.Quantum.Math;

  operation OracleZero(x : Qubit, y : Qubit) : Unit is Adj + Ctl {
    // Do nothing.
  }

  operation OracleOne(x : Qubit, y : Qubit) : Unit is Adj + Ctl {
    X(y);
  }

  operation OracleX(x : Qubit, y : Qubit) : Unit is Adj + Ctl {
    CNOT(x, y);
  }

  operation OracleOneMinusX(x : Qubit, y : Qubit) : Unit is Adj + Ctl {
    ApplyControlledOnInt(0, X, [x], y);
  }

  @EntryPoint()
  operation DemoSingleBitFunctions() : Unit {
    for (oracle, f) in [
      (OracleZero, "f(x) = 0"),
      (OracleOne, "f(x) = 1"),
      (OracleX, "f(x) = x"),
      (OracleOneMinusX, "f(x) = 1 - x")
    ] {
      Message($"The effects of applying the oracle {f} to the state (0.6|0⟩ + 0.8|1⟩) ⨂ |0⟩:");
      use (x, y) = (Qubit(), Qubit());
      Ry(2.0 * ArcCos(0.6), x);
      oracle(x, y);
      DumpMachine();
      ResetAll([x, y]);
    }
  }
}
