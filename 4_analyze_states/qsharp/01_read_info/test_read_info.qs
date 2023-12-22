namespace AnalyzeStates.Test {
  open Microsoft.Quantum.Diagnostics;
  open Microsoft.Quantum.Intrinsic;
  open Microsoft.Quantum.Random;
  open AnalyzeStates;

  operation RunTestReadInformation(n : Int, basisState : Int) : Unit {
    use qs = Qubit[n];
    for i in 0 .. n - 1 {
      if (basisState &&& (1 <<< i)) > 0 {
        X(qs[i]);
      }
    }
    let res = ReadInformation(qs);
    mutable resInt = 0;
    for i in n - 1 .. -1 .. 0 {
      set resInt = resInt * 2 + (res[i] == One ? 1 | 0);
    }
    Fact(resInt == basisState, $"Expected {basisState}, got {resInt}");
  }

  @Test("QuantumSimulator")
  operation TestReadInformation() : Unit {
    for _ in 1 .. 20 {
      let n = DrawRandomInt(1, 5);
      let basisState = DrawRandomInt(0, 2 ^ n - 1);
      RunTestReadInformation(n, basisState);
    }
  }
}