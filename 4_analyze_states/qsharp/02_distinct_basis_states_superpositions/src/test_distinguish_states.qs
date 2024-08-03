namespace AnalyzeStates.Test {
  open Microsoft.Quantum.Diagnostics;
  open Microsoft.Quantum.Random;
  open AnalyzeStates;

  operation PrepTestState(qs : Qubit[], ind : Int) : Unit {
    H(qs[0]);
    CNOT(qs[0], qs[1]);
    CNOT(qs[0], qs[2]);
    if ind != 0 {
      X(qs[ind - 1]);
    }
  }

  operation TestDistinguishStates() : Unit {
    for _ in 1 .. 100 {
      use qs = Qubit[3];
      let stateInd = DrawRandomInt(0, 3);
      PrepTestState(qs, stateInd);
      let resState = DistinguishStates(qs);
      Fact(resState == stateInd, 
        $"Expected state {stateInd}, got {resState}");
    }
  }
}