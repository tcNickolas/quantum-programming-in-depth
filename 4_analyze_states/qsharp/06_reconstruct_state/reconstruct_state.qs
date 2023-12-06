namespace AnalyzeStates {
  open Microsoft.Quantum.Convert;
  open Microsoft.Quantum.Intrinsic;
  open Microsoft.Quantum.Math;

  operation ReconstructState(statePrep : (Qubit => Unit)) : (Double, Double) {
    // Figure out the absolute values of alpha and beta
    mutable (nZero, nOne) = (0, 0);
    mutable nTrials = 200;
    for _ in 1 .. nTrials {
      use q = Qubit();
      statePrep(q);
      if M(q) == Zero {
        set nZero += 1;
      } else {
        set nOne += 1;
      }
    }
    let alpha = Sqrt(IntAsDouble(nZero) / IntAsDouble(nTrials));
    let beta = Sqrt(IntAsDouble(nOne) / IntAsDouble(nTrials));

    // Figure out whether there is a relative phase of -1
    // (distinguish alpha |0> + beta |1> from alpha |0> - beta |1>).
    // The mid-line between them would be horizontal, so we rotate by PI/4 clockwise
    set (nZero, nOne) = (0, 0);
    for _ in 1 .. 100 {
      use q = Qubit();
      statePrep(q);
      Ry(PI() / 2., q);
      if M(q) == Zero {
        set nZero += 1;
      } else {
        set nOne += 1;
      }
    }
    return nZero > nOne ? (alpha, -beta) | (alpha, beta);
  }
}
