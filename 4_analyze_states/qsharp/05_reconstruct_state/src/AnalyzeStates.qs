﻿import Std.Convert.IntAsDouble;
import Std.Math.*;

operation ReconstructState(statePrep : Qubit => Unit) : (Double, Double) {
  // Figure out the absolute values of alpha and beta
  mutable nZeros = 0;
  let nTrials = 1000;
  for _ in 1 .. nTrials {
    use q = Qubit();
    statePrep(q);
    if MResetZ(q) == Zero {
      set nZeros += 1;
    }
  }
  let alpha = Sqrt(IntAsDouble(nZeros) / IntAsDouble(nTrials));
  let beta = Sqrt(IntAsDouble(nTrials - nZeros) / IntAsDouble(nTrials));

  // Figure out whether there is a relative phase of -1
  // (distinguish alpha |0> + beta |1> from alpha |0> - beta |1>).
  // The mid-line between them would be horizontal, so we rotate by PI/4 clockwise
  set nZeros = 0;
  for _ in 1 .. nTrials {
    use q = Qubit();
    statePrep(q);
    Ry(PI() / 2., q);
    if MResetZ(q) == Zero {
      set nZeros += 1;
    }
  }
  return 2 * nZeros > nTrials ? (alpha, -beta) | (alpha, beta);
}
