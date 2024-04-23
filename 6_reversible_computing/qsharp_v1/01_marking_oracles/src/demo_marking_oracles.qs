namespace ReversibleComputing.Test {
  open Microsoft.Quantum.Logical;
  open Microsoft.Quantum.Convert;
  open Microsoft.Quantum.Arrays;
  open Microsoft.Quantum.Diagnostics;
  open ReversibleComputing;

  @EntryPoint()
  operation DemoMarkingOracles() : Unit {
    for (oracle, f) in [
      (OracleZero, "f(x) = 0"),
      (OracleOne, "f(x) = 1"),
      (OracleX, "f(x) = x")
    ] {
      Message($"The effects of applying the oracle {f} to the state |+⟩ ⨂ |0⟩:");
      use (x, y) = (Qubit(), Qubit());
      H(x);
      oracle(x, y);
      DumpMachine();
      ResetAll([x, y]);
    }
  }
}