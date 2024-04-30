namespace ReversibleComputing.Test {
  open Microsoft.Quantum.Diagnostics;
  open Microsoft.Quantum.Math;
  open ReversibleComputing;

  @EntryPoint()
  operation DemoMarkingOracles() : Unit {
    for (oracle, f) in [
      (OracleZero, "f(x) = 0"),
      (OracleOne, "f(x) = 1"),
      (OracleX, "f(x) = x")
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