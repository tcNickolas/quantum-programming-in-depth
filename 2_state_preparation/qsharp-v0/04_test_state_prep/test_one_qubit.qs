namespace StatePreparation.Test {
  open Microsoft.Quantum.Diagnostics;
  open Microsoft.Quantum.Intrinsic;
  open Microsoft.Quantum.Math;

  open StatePreparation;

  operation TestPrepOneQubit(alpha : Double, beta : Double) : Unit {
    use q = Qubit();
    PrepOneQubit(q, alpha, beta);
    let amps = (Complex(alpha, 0.), Complex(beta, 0.));
    AssertQubitIsInStateWithinTolerance(amps, q, 1E-6);
    Reset(q);
  }

  @Test("QuantumSimulator")
  operation OneQubitTest() : Unit {
    TestPrepOneQubit(1., 0.);
    TestPrepOneQubit(0., 1.);

    let sq = 1./Sqrt(2.);
    TestPrepOneQubit(sq, sq);
    TestPrepOneQubit(sq, -sq);

    TestPrepOneQubit(0.6, 0.8);
    TestPrepOneQubit(0.6, -0.8);
    TestPrepOneQubit(-0.8, 0.6);
    TestPrepOneQubit(-0.8, -0.6);
  }
}
