import Std.Diagnostics.Fact;
import Std.Random.DrawRandomInt;
import AnalyzeStates.DistinguishBellStates;

operation PrepBellState(qs : Qubit[], ind : Int) : Unit {
  H(qs[0]);
  CNOT(qs[0], qs[1]);
  if ind / 2 == 1 {
    X(qs[0]);
  }
  if ind % 2 == 1 {
    Z(qs[0]);
  }
}

operation TestDistinguishStates() : Unit {
  for _ in 1 .. 100 {
    use qs = Qubit[2];
    let stateInd = DrawRandomInt(0, 3);
    PrepBellState(qs, stateInd);
    let resState = DistinguishBellStates(qs);
    Fact(resState == stateInd, 
      $"Expected state {stateInd}, got {resState}");
  }
}
