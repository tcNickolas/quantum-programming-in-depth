namespace AnalyzeStates.Test {
  open Microsoft.Quantum.Arithmetic;
  open Microsoft.Quantum.Arrays;
  open Microsoft.Quantum.Canon;
  open Microsoft.Quantum.Diagnostics;
  open Microsoft.Quantum.Intrinsic;
  open Microsoft.Quantum.Math;
  open Microsoft.Quantum.Preparation;
  open Microsoft.Quantum.Random;
  open AnalyzeStates;

  function CompleteAmps(n : Int, parityAmps : Double[], parity : Int) : Double[] {
    if n == 1 {
      return parity == 0 ? (parityAmps + [0.]) | ([0.] + parityAmps);
    }

    let zeroAmps = parityAmps[ ... (1 <<< (n - 2)) - 1];
    let oneAmps = parityAmps[1 <<< (n - 2) ...];
    return CompleteAmps(n - 1, zeroAmps, parity) + CompleteAmps(n - 1, oneAmps, 1 - parity);
  }

  @Test("QuantumSimulator")
  operation TestDistinguishStates() : Unit {
    for _ in 1 .. 100 {
      let n = DrawRandomInt(2, 5);
      let parity = DrawRandomInt(0, 1);
      let parityAmps = PNormalized(2., ForEach(DrawRandomDouble, [(0., 1.), size = 2 ^ (n - 1)]));
      let completeAmps = CompleteAmps(n, parityAmps, parity);

      use qs = Qubit[n];
      PrepareArbitraryStateD(completeAmps, LittleEndian(qs));
      let resParity = StateParity(qs);
      // Check that the parity is correct.
      Fact(resParity == parity, 
        $"Expected parity {parity}, got {resParity}");

      // Check that the resulting state is the same as the initial one
      // and has not been modified by the measurement.
      Adjoint PrepareArbitraryStateD(completeAmps, LittleEndian(qs));
      AssertAllZero(qs);
    }
  }
}