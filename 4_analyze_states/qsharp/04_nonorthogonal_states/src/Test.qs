import Std.Convert.IntAsDouble;
import Std.Math.*;
import Std.Random.*;
import AnalyzeStates.DistinguishZeroAndSup;

operation PrepInputState(q : Qubit, alpha : Double, beta : Double, ind : Int) : Unit {
  if ind == 1 {
    Ry(2. * ArcTan2(beta, alpha), q);
  }
}

operation TestDistinguishZeroAndSup() : Unit {
  for _ in 1 .. 10 {
    let angle = DrawRandomDouble(0., PI() / 2.);
    let (alpha, beta) = (Cos(angle), Sin(angle));
    mutable nCorrect = 0;
    let nTrials = 1000;
    for _ in 1 .. nTrials {
      use q = Qubit();
      let stateInd = DrawRandomInt(0, 1);
      PrepInputState(q, alpha, beta, stateInd);
      let resState = DistinguishZeroAndSup(q, alpha, beta);
      if resState == stateInd {
        set nCorrect += 1;
      }
    }
    let pSuccess = IntAsDouble(nCorrect) / IntAsDouble(nTrials);
    let pSuccessTheor = 0.5 * (1. + beta);
    Message($"Correct guesses {pSuccess}, theoretical {pSuccessTheor}");
    if pSuccess < pSuccessTheor - 0.05 {
      fail $"Expected success probability {pSuccessTheor}, got {pSuccess}, too low";
    }
    if pSuccess > pSuccessTheor + 0.05 {
      fail $"Expected success probability {pSuccessTheor}, got {pSuccess}, too high";
    }
  }
}
