namespace StatePreparation.Test {
  open Microsoft.Quantum.Arithmetic;
  open Microsoft.Quantum.Arrays;
  open Microsoft.Quantum.Diagnostics;
  open Microsoft.Quantum.Math;
  open Microsoft.Quantum.Preparation;

  open StatePreparation;

  operation TestTwoQubitStatePrep(a : Double[]) : Unit {
    use qs = Qubit[2];
    PrepTwoQubits(qs, a);
    let realAsCP = r -> ComplexPolar(AbsD(r), r >= 0. ? 0. | PI());
    let complexA = Mapped(realAsCP, a);
    Adjoint PrepareArbitraryStateCP(complexA, LittleEndian(qs));
    AssertAllZero(qs);
  }

  @Test("QuantumSimulator")
  operation BasisStatesTest() : Unit {
    TestTwoQubitStatePrep([1., 0., 0., 0.]);
    TestTwoQubitStatePrep([0., 1., 0., 0.]);
    TestTwoQubitStatePrep([0., 0., 1., 0.]);
    TestTwoQubitStatePrep([0., 0., 0., 1.]);
  }

  @Test("QuantumSimulator")
  operation EqualSuperpositionsTest() : Unit {
    TestTwoQubitStatePrep([0.5, 0.5, 0.5, 0.5]);
    TestTwoQubitStatePrep([-0.5, 0.5, 0.5, 0.5]);
    TestTwoQubitStatePrep([0.5, -0.5, 0.5, 0.5]);
    TestTwoQubitStatePrep([0.5, 0.5, -0.5, 0.5]);
    TestTwoQubitStatePrep([0.5, 0.5, 0.5, -0.5]);
  }

  @Test("QuantumSimulator")
  operation BellStatesTest() : Unit {
    TestTwoQubitStatePrep([1. / Sqrt(2.), 0., 0., 1. / Sqrt(2.)]);
    TestTwoQubitStatePrep([1. / Sqrt(2.), 0., 0., -1. / Sqrt(2.)]);
    TestTwoQubitStatePrep([0., 1. / Sqrt(2.), 1. / Sqrt(2.), 0.]);
    TestTwoQubitStatePrep([0., 1. / Sqrt(2.), -1. / Sqrt(2.), 0.]);
  }

  @Test("QuantumSimulator")
  operation UnequalSuperpositionsTest() : Unit {
    TestTwoQubitStatePrep([0.36, 0.48, 0.64, -0.48]);
    TestTwoQubitStatePrep([1. / Sqrt(3.), -1. / Sqrt(3.), 1. / Sqrt(3.), 0.]);
  }
}