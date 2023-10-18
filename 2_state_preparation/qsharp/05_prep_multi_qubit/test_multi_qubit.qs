namespace StatePreparation.Test {
  open Microsoft.Quantum.Arithmetic;
  open Microsoft.Quantum.Arrays;
  open Microsoft.Quantum.Diagnostics;
  open Microsoft.Quantum.Intrinsic;
  open Microsoft.Quantum.Math;
  open Microsoft.Quantum.Preparation;
  open Microsoft.Quantum.Random;

  open StatePreparation;

  operation TestArbitraryStatePrep(n : Int, a : Double[]) : Unit {
    use qs = Qubit[n];
    PrepArbitrary(qs, a);
    let complexA = Mapped((r -> ComplexPolar(AbsD(r), r >= 0.0 ? 0.0 | PI())), a);
    Adjoint PrepareArbitraryStateCP(complexA, LittleEndian(qs));
    AssertAllZero(qs);
  }

  @Test("QuantumSimulator")
  operation BasisStatesTest() : Unit {
    for n in 1 .. 3 {
      for basis in 0 .. 2 ^ n - 1 {
        TestArbitraryStatePrep(n, [0.0, size = 2 ^ n] w/ basis <- 1.0);
      }
    }
  }


  @Test("QuantumSimulator")
  operation EqualSuperpositionsTest() : Unit {
    TestArbitraryStatePrep(2, [0.5, 0.5, 0.5, 0.5]);
    TestArbitraryStatePrep(2, [0.5, -0.5, 0.5, 0.5]);
    TestArbitraryStatePrep(2, [0.5, 0.5, -0.5, 0.5]);
    TestArbitraryStatePrep(2, [0.5, 0.5, 0.5, -0.5]);
  }

  @Test("QuantumSimulator")
  operation BellStatesTest() : Unit {
    TestArbitraryStatePrep(2, [1.0 / Sqrt(2.0), 0.0, 0.0, 1.0 / Sqrt(2.0)]);
    TestArbitraryStatePrep(2, [1.0 / Sqrt(2.0), 0.0, 0.0, -1.0 / Sqrt(2.0)]);
    TestArbitraryStatePrep(2, [0.0, 1.0 / Sqrt(2.0), 1.0 / Sqrt(2.0), 0.0]);
    TestArbitraryStatePrep(2, [0.0, 1.0 / Sqrt(2.0), -1.0 / Sqrt(2.0), 0.0]);
  }

  @Test("QuantumSimulator")
  operation UnequalSuperpositionsTest() : Unit {
    TestArbitraryStatePrep(1, [0.6, 0.8]);
    TestArbitraryStatePrep(1, [0.6, -0.8]);
    TestArbitraryStatePrep(2, [0.36, 0.48, 0.64, -0.48]);
    TestArbitraryStatePrep(2, [1. / Sqrt(3.), -1. / Sqrt(3.), 1. / Sqrt(3.), 0.]);
  }

  @Test("QuantumSimulator")
  operation RandomUnequalSuperpositionsTest() : Unit {
    for i in 1 .. 10 {
      let n = DrawRandomInt(2, 4);
      let a = ForEach(DrawRandomDouble, [(-1.0, 1.0), size = 2 ^ n]);
      TestArbitraryStatePrep(n, a);
    }
  }
}