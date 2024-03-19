namespace AnalyzeUnitaries {
  open Microsoft.Quantum.Convert;
  open Microsoft.Quantum.Math;
  open Microsoft.Quantum.Measurement;

  operation ReconstructState(statePrep : Qubit => Unit) : (Double, Double) {
    // Figure out the absolute values of alpha and beta
    mutable nZeros = 0;
    let nTrials = 200;
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

  operation ReconstructUnitary(gate : Qubit => Unit) : Double[][] {
    // Analyze the effects of the gate on the |0> state to get the first column
    let (a, b) = ReconstructState(gate);
    // Figure out whether the second column is (b; -a) or (-b; a)
    // Prepare a state a|0> + b|1> and apply the unitary to it; 
    // in the first case, the result is always |0>, in the second case, (a^2-b^2)|0> + 2ab|1>
    let nTrials = 200;
    mutable nZeros = 0;
    for _ in 1 .. nTrials {
      use q = Qubit();
      // Prepare a state a|0> + b|1> using the unitary itself and apply the unitary to it again
      gate(q);
      gate(q);
      // Reflect about the horizontal axis to make the second coefficient positive
      if b < 0. {
        Z(q);
      }
      // Treat the result as a choice between |0> and (a^2-b^2)|0> + 2ab|1>
      // Figure out the angle of the line halfway between |0> and alpha |0> + beta |1>
      let theta = ArcTan2(2. * a * AbsD(b), a * a - b * b) / 2.;
      // Rotate so that the middle between the two angles is at the angle pi/4
      Ry(- 2. * (theta - PI() / 4.), q);
      if MResetZ(q) == Zero {
        set nZeros += 1;
      }
    }
    return 2 * nZeros > nTrials ? [[a, b], [b, -a]] | [[a, -b], [b, a]];
  }
}
