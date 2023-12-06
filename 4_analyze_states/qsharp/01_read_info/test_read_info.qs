namespace AnalyzeStates.Test {
  open Microsoft.Quantum.Diagnostics;
  open Microsoft.Quantum.Intrinsic;
  open Microsoft.Quantum.Random;
  open AnalyzeStates;

  operation RunTestReadInformation(n : Int, num : Int) : Unit {
    use qs = Qubit[n];
    for i in 0 .. n - 1 {
      if (num &&& (1 <<< i)) > 0 {
        X(qs[i]);
      }
    }
    let res = ReadInformation(qs);
    mutable resInt = 0;
    for i in n - 1 .. -1 .. 0 {
      set resInt = resInt * 2 + (res[i] == One ? 1 | 0);
    }
    Fact(resInt == num, $"Expected {num}, got {resInt}");
  }

  @Test("QuantumSimulator")
  operation TestReadInformation() : Unit {
    for _ in 1 .. 20 {
      let n = DrawRandomInt(1, 5);
      let num = DrawRandomInt(0, 2 ^ n - 1);
      RunTestReadInformation(n, num);
    }
  }
}